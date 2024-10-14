from aiogram import F, types, Router
from aiogram.types import CallbackQuery
from aiogram.filters import CommandStart, Command
from filters.chat_types import ChatTypeFilter
from aiogram.fsm.state import StatesGroup, State

from keybds.reply import *
from common.variables import *


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private', 'group']))


@user_private_router.message(CommandStart())
async def handle_start(msg: types.Message):
    await msg.answer(text=f'Привет, {msg.from_user.full_name}')
    await msg.answer(text=HELLO_TEXT) # Приветственный текст (хранится в переменном окружении)
    await msg.answer(text='Выбирите, что вы хотите сделать:', reply_markup=AUTH_BTN)

@user_private_router.message(Command('id'))
async def chek_id(msg: types.Message):
    await msg.answer(text=f'Ваш ID: {msg.from_user.id}')
    print(f'/id call! ==> id:{msg.from_user.id} ник: @{msg.from_user.username} имя: {msg.from_user.first_name} {msg.from_user.last_name} ')

@user_private_router.message(Command('menu'))
async def menu(msg: types.Message):
    await msg.answer(text='выберите действие:', reply_markup=MENU_KEYBOARD)

#TODO сделать авторизацию и регистрацию 
#[x] FSM 

@user_private_router.callback_query(F.data == 'auth')
async def authorization(callback: CallbackQuery):
    await callback.message.answer('Введите логин:')


class auth(StatesGroup): # FSM для регистрации
    authorization = State()

class reg(StatesGroup): # FSM для авторизации
    registration = State()


@user_private_router.message(F.text.lower() == 'user')
async def auth_login_check(msg: types.Message):
    await msg.answer(text='Введите пароль:')