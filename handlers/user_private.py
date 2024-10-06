from os import getenv
from dotenv import find_dotenv, load_dotenv

from aiogram import F, types, Router
from aiogram.types import KeyboardButton, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder
# from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart, Command
from filters.chat_types import ChatTypeFilter

from keybds.reply import get_keyboard


load_dotenv(find_dotenv())
user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private', 'group']))


AUTH_BTN = get_keyboard(
    "Аторизироватсья",
    "Зарегистрироваться",
    placeholder="Выберите действие",
    sizes=(2, 1, 1),
)

@user_private_router.message(CommandStart())
async def handle_start(msg: types.Message):
    await msg.answer(text=f'Привет, {msg.from_user.full_name}')
    await msg.answer(text=getenv("HELLO_TEXT")) # Приветственный текст (хранится в переменном окружении)
    await msg.answer(text='Выбирите, что вы хотите сделать:', reply_markup=AUTH_BTN)

#TODO: сделать авторизацию и регистрацию
@user_private_router.callback_query(F.data == 'auth')
async def authorization(callback: CallbackQuery):
    await callback.message.answer('Введите логин:')

@user_private_router.message(F.text.lower() == 'admin')
async def auth_login_check(msg: types.Message):
    await msg.answer(text='Введите паороль:')