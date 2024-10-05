from os import getenv
from dotenv import find_dotenv, load_dotenv

from aiogram import F, types, Router
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, KeyboardButton, CallbackQuery
# from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart, Command


load_dotenv(find_dotenv())
user_private_router = Router()

#TODO: сделать рекомпозицию keyboards
def auth_buttons():
    regauth = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='регистрация', callback_data='reg')],
        [InlineKeyboardButton(text='авторизация', callback_data='auth')]
    ])
    return regauth

@user_private_router.message(CommandStart())
async def handle_start(msg: types.Message):
    await msg.answer(text=f'Привет, {msg.from_user.full_name}')
    await msg.answer(text=getenv("HELLO_TEXT")) # Приветственный текст (хранится в переменном окружении)
    await msg.answer(text='Выбирите, что вы хотите сделать:', reply_markup=auth_buttons())
#TODO: сделать авторизацию и регистрацию
@user_private_router.callback_query(F.data == 'auth')
async def authorization(callback: CallbackQuery):
    await callback.message.answer('Введите логин:')

@user_private_router.message(F.text == 'admin')
async def auth_login_check(msg: types.Message):
    await msg.answer(text='Введите паороль:')