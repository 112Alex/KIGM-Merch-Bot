from os import getenv
from dotenv import find_dotenv, load_dotenv

from aiogram import types, Router
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart, Command


load_dotenv(find_dotenv())
user_private_router = Router()

def auth_buttons():
    kb_list = [[KeyboardButton(text="/login")], [KeyboardButton(text="/reg")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


@user_private_router.message(CommandStart())
async def handle_start(msg: types.Message):
    await msg.answer(text=f'Привет, {msg.from_user.full_name}')
    await msg.answer(text=getenv("HELLO_TEXT")) # Приветственный текст (хранится в переменном окружении)
    await msg.answer(text='Выбирите, что вы хотите сделать:')
    await msg.answer('Вот тебе инлайн клавиатура со ссылками!', reply_markup=auth_buttons())

# @user_private_router.message_handler(Command('/login'))
# async def handle_login(msg: types.Message):
#     await msg.answer(text='укажите логин:')