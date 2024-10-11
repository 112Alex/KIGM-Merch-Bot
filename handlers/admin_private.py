from aiogram import F, Router, types
from aiogram.types import CallbackQuery
from aiogram.filters import Command
from filters.chat_types import ChatTypeFilter, IsAdmin

from keybds.reply import *


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

@admin_router.message(Command("admin_menu"))
async def admin_menu(msg: types.Message):
    await msg.answer(text='меню:', reply_markup=ADMIN_KB)

@admin_router.callback_query(F.data == 'add_event')
async def add_event_handle(callback: CallbackQuery):
    await callback.message.answer(text='Выберите действие:', reply_markup=ADD_EVENT_KEYBOARD)

@admin_router.message(F.text.lower() == 'волонтёрское благотворительное мероприятие в колледже')
async def vbmvk(msg: types.Message):
    await msg.answer(text="мероприятие выбрано", reply_markup=types.ReplyKeyboardRemove())
# TODO:Дописать остальные админ-функции