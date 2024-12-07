from aiogram import F, Router, types
from aiogram.types import CallbackQuery
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter, IsAdmin
from keybds.inline import *
from keybds.reply import *
from database.orm_query import *


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


#COMMENT код ниже для FSM
class EventAdd(StatesGroup):
    set_event_type = State()
    set_event_name = State()
    set_event_date = State()
    event_confirmation = State()

    event_for_change = None

    texts = {
        'EventAdd:set_event_type': 'Выберите действие',
    }


@admin_router.message(StateFilter(None), Command("admin_menu"))
async def admin_menu(msg: types.Message):
    await msg.answer(text='меню:', reply_markup=ADMIN_KB)


@admin_router.callback_query(StateFilter(None), F.data == 'add_event')
async def add_event_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Выберите действие:', reply_markup=ADD_EVENT_KEYBOARD)
    await state.set_state(EventAdd.set_event_type)

@admin_router.message(F.data)
async def add_event_handler(msg: types.Message, state: FSMContext):
    await msg.answer(text='Вы ввели некорректные данные. Выберите действие:')


#COMMENT отменить действие (сбросить состояние)
@admin_router.message(StateFilter('*'), Command("отмена"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return
    if EventAdd.event_for_change:
        EventAdd.event_for_change = None

    await state.clear()
    await message.answer("Действия отменены", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Выберите действие:", reply_markup=ADMIN_KB)

#COMMENT вернуться на шаг назад (на предыдущее состояние)
@admin_router.message(StateFilter('*'), Command("назад"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()

    if current_state == EventAdd.set_event_type:
        await message.answer('Предыдущего шага нет, или укажите тип мероприятия или напишите "отмена"', reply_markup=ADD_EVENT_KEYBOARD)
        return
    
    previous = None
    for step in EventAdd.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n {EventAdd.texts[previous.state]}")
            return
        previous = step


#COMMENT ВЫБОР МЕРОПРИЯТИЯ
@admin_router.message(EventAdd.set_event_type, lambda message: message.text in events)
async def event_type_handler(msg: types.Message, state: FSMContext):
    await state.update_data(set_event_type = msg.text)
    await msg.answer(text=f"тип мероприятия выбран\n({msg.text})\nТеперь введите название мероприятия", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(EventAdd.set_event_name)

#---#COMMENT----ПРЕДЫДУЩИЙ ВАРИАНТ ФУНКЦИИ ПРОВЕРКИ ВВОДА---------------
# @admin_router.message(EventAdd.set_event, F.text.lower() == events[0].lower())
# async def set_event_type(msg: types.Message, state: FSMContext):
#     await state.update_data(set_event = msg.text)
#     await msg.answer(text=f"мероприятие выбрано \n({msg.text})", reply_markup=types.ReplyKeyboardRemove())
#     await state.set_state(EventAdd.zaglushka)

@admin_router.message(EventAdd.set_event_type)
async def event_type_handler(msg: types.Message, state: FSMContext):
    await msg.answer(text="вы ввели некорректное значение")


#COMMENT Ловим данные для состояния set_event_name и меняем состояние на set_event_date
@admin_router.message(EventAdd.set_event_name, or_f(F.text, F.text == '.'))
async def event_date_handler(msg: types.Message, state: FSMContext):
    if msg.text == '.':
        await state.update_data(set_event_name = EventAdd.event_for_change.event_name)
    else:
        if len(msg.text) > 150:
            await msg.answer("Название мероприятия не должно превышать 150 символов\nВведите заново")
            return
        await state.update_data(set_event_name = msg.text)
    await msg.answer(
        text=f"название мероприятия выбрано\n({msg.text})\nТеперь укажите дату мероприятия",
        reply_markup=types.ReplyKeyboardRemove()
        )
    await state.set_state(EventAdd.set_event_date)

@admin_router.message(EventAdd.set_event_date)
async def event_info(msg: types.Message, state: FSMContext):
    await state.update_data(set_event_date = msg.text)
    data = await state.get_data()
    data_arr = []
    for item in data:
        data_arr.append(str(data.get(item)))
    await msg.answer(text=f'мероприятие добавлено\nТип: {data_arr[0]}\nНазвание: {data_arr[1]}\nДата: {data_arr[2]}')
    await msg.answer(text='Всё верно?', reply_markup=YES_NO_KB)
    await state.set_state(EventAdd.event_confirmation)

#COMMENT Подтверждение добавления мероприятия
@admin_router.callback_query(EventAdd.event_confirmation, F.data == 'yes')
async def event_confirmation(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.update_data(event_confirmation = F.data)
    data = await state.get_data()
    try:
        if EventAdd.event_for_change:
            await orm_update_event(session, EventAdd.event_for_change.id, data)
        else:
            await orm_add_event(session, data)
        await callback.answer()
        await callback.message.answer("Действие подтверждено\nМероприятие добавлено")
        await state.clear()
        await callback.message.answer("Выберите действие:", reply_markup=ADMIN_KB)
    except Exception as e:
        await callback.message.answer(
            f"Ошибка: \n{str(e)}\n Обратитесь к разработчику", reply_markup=ADMIN_KB)
        await state.clear()
    
    EventAdd.event_for_change = None

@admin_router.callback_query(EventAdd.event_confirmation, F.data == 'no')
async def event_confirmation(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Действия отменены')
    await state.clear()
    await callback.message.answer("Выберите действие:", reply_markup=ADMIN_KB)

#COMMENT Показать все мероприятия
@admin_router.callback_query(StateFilter(None), F.data == 'show_events')
async def show_events(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    for event in await orm_get_events(session):
        await callback.message.answer(
            f'<i>{event.event_type}</i>\n<strong>{event.event_name}</strong>\n\n<code>{event.event_date}</code>',
            parse_mode='html',
            reply_markup=get_callback_btns(btns={
                'Удалить': f'delete_{event.id}',
                'Изменить': f'change_{event.id}'
            })
        )
    await callback.answer()

#COMMENT Удалить мероприятие
@admin_router.callback_query(F.data.startswith('delete_'))
async def delete_event(callback: CallbackQuery, session: AsyncSession):

    event_id = callback.data.split("_")[-1]
    await orm_delete_event(session, int(event_id))
    await callback.message.delete()

    await callback.answer('Мероприятие удалено')

#COMMENT Изменение мероприятий
@admin_router.callback_query(StateFilter(None), F.data.startswith('change_'))
async def edit_event(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    event_id = callback.data.split("_")[-1]
    event_for_change = await orm_get_event(session, int(event_id))

    EventAdd.event_for_change = event_for_change
    await callback.answer()
    await callback.message.answer(
        "Введите тип мероприятия", reply_markup=ADD_EVENT_KEYBOARD
    )
    await state.set_state(EventAdd.set_event_type)





#TODO Дописать остальные админ-функции