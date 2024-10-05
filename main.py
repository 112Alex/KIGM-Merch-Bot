from os import getenv
import asyncio
import logging
from dotenv import find_dotenv, load_dotenv

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, WebAppInfo, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart, Command
#TODO разобраться с импортами

load_dotenv(find_dotenv())
bot = Bot(token=getenv("BOT_TOKEN"))
dp = Dispatcher()

def auth_buttons():
    kb_list = [[KeyboardButton(text="авторизироваться")], [KeyboardButton(text="зарегистрироваться")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard
#TODO вынести функции кнопок в отдельный файл


@dp.message(CommandStart())
async def handle_start(msg: types.Message):
    await msg.answer(text=f'Привет, {msg.from_user.full_name}')
    await msg.answer(text=getenv("HELLO_TEXT")) # Приветственный текст (хранится в переменном окружении)
    await msg.answer(text='Выбирите, что вы хотите сделать:')
    await msg.answer('Вот тебе инлайн клавиатура со ссылками!', reply_markup=auth_buttons())
    # TODO: дописать авторизацию


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())