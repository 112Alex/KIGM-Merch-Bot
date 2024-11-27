from aiogram import F, Router, types
from aiogram.types import CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from filters.chat_types import ChatTypeFilter, IsAdmin
from keybds.reply import *


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

#COMMENT код ниже для FSM
class AdminMenu(StatesGroup):
    menu = State()
    set_event_type = State()
    set_event_name = State()
    set_event_date = State()

    texts = {
        'AdminMenu:menu': 'Выберите действие',
    }

#COMMENT отменить действие (сбросить состояние)
#NOTE работает
@admin_router.message(StateFilter('*'), Command("отмена"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.set_state(AdminMenu.menu)
    await message.answer("Действия отменены", reply_markup=ADMIN_KB,)

#COMMENT вернуться на шаг назад (на предыдущее состояние)
#BUG меню не хэндлится. (Вероятно из-за того, что прописано только одно состояние для создания мероприятий)
@admin_router.message(StateFilter('*'), Command("назад"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()

    if current_state == AdminMenu.menu: #[ ] проверить
        await message.answer('Предыдущего шага нет, или введите название товара или напишите "отмена"')
        return
    
    previous = None
    for step in AdminMenu.__all_states__: #[ ] проверить
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n {AdminMenu.texts[previous.state]}")
            return
        previous = step


@admin_router.message(StateFilter('*'), Command("admin_menu"))
async def admin_menu(msg: types.Message, state: FSMContext):
    await msg.answer(text='меню:', reply_markup=ADMIN_KB)
    await state.set_state(AdminMenu.menu)


@admin_router.callback_query(AdminMenu.menu, F.data == 'add_event')
async def add_event_handle(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Выберите действие:', reply_markup=ADD_EVENT_KEYBOARD)
    await state.set_state(AdminMenu.set_event_type)

@admin_router.message(AdminMenu.menu)
async def add_event_handle(msg: types.Message, state: FSMContext):
    await msg.answer(text='Вы ввели некорректные данные. Выберите действие:')

#COMMENT ВЫБОР МЕРОПРИЯТИЯ

@admin_router.message(AdminMenu.set_event_type, lambda message: message.text in events)
async def event_type_handler(msg: types.Message, state: FSMContext):
    await state.update_data(set_event_type = msg.text)
    await msg.answer(text=f"мероприятие выбрано \n({msg.text})", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AdminMenu.set_event_name)

#---------------ПРЕДЫДУЩИЙ ВАРИАНТ ФУНКЦИИ ПРОВЕРКИ ВВОДА---------------
# @admin_router.message(AdminMenu.set_event, F.text.lower() == events[0].lower())
# async def set_event_type(msg: types.Message, state: FSMContext):
#     await state.update_data(set_event = msg.text)
#     await msg.answer(text=f"мероприятие выбрано \n({msg.text})", reply_markup=types.ReplyKeyboardRemove())
#     await state.set_state(AdminMenu.zaglushka)

@admin_router.message(AdminMenu.set_event_type)
async def event_type_handler(msg: types.Message, state: FSMContext):
    await msg.answer(text="вы ввели некорректное значение")


@admin_router.message(AdminMenu.set_event_name)
async def event_date_handler(msg: types.Message, state: FSMContext):
    await state.update_data(set_event_name = msg.text)
    await msg.answer(text=f"название мероприятия выбрано\n({msg.text})\nТеперь укажите дату мероприятия")
    await state.set_state(AdminMenu.set_event_date)

@admin_router.message(AdminMenu.set_event_date)
async def event_date_handler(msg: types.Message, state: FSMContext):
    await state.update_data(set_event_date = msg.text)
    t = ''
    for item in state.get_data:
        t += f'{item}\n'
    data = await state.get_data()
    await msg.answer(t)
    await msg.answer(str(data))
    await state.clear()




#TODO Дописать остальные админ-функции