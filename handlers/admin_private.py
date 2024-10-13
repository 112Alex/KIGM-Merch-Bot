from aiogram import F, Router, types
from aiogram.types import CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from filters.chat_types import ChatTypeFilter, IsAdmin
from keybds.reply import *


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

class AdminMenu(StatesGroup):
    set_action = State()
    set_event = State()
    zaglushka = State()

@admin_router.message(StateFilter(None), Command("admin_menu"))
async def admin_menu(msg: types.Message, state: FSMContext):
    await msg.answer(text='меню:', reply_markup=ADMIN_KB)
    await state.set_state(AdminMenu.set_action)

@admin_router.callback_query(AdminMenu.set_action, F.data == 'add_event')
async def add_event_handle(callback: CallbackQuery, state: FSMContext):
    await state.update_data(set_action = callback.message.text)
    await callback.message.answer(text='Выберите действие:', reply_markup=ADD_EVENT_KEYBOARD)
    await state.set_state(AdminMenu.set_event)

@admin_router.message(AdminMenu.set_event, F.text.lower() == 'волонтёрское благотворительное мероприятие в колледже')
async def vbmvk_handler(msg: types.Message, state: FSMContext):
    await state.update_data(set_event = msg.text)
    await msg.answer(text="мероприятие выбрано", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()


# TODO:Дописать остальные админ-функции