from aiogram import F, types, Router
from aiogram.types import CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from filters.chat_types import ChatTypeFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

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


class Auth(StatesGroup): #NOTE класс состояния регистрации
    login = State()

class Reg(StatesGroup): #NOTE класс состояния авторизации
    registration = State()

class UserState(StatesGroup): #NOTE класс обычного состояния пользователя
    user_state = State()

@user_private_router.callback_query(StateFilter('*'), F.data == 'auth')
async def authorization(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите логин:')
    await state.set_state(Auth.login)

@user_private_router.message(Auth.login, F.text.lower() == 'user')
async def auth_login_check(msg: types.Message, state: FSMContext):
    await state.update_data(login=msg.text)
    await msg.answer(text='Введите пароль:')
    await state.set_state(UserState.user_state)

@user_private_router.message(UserState.user_state, F.text.lower() == 'Z')
async def z(msg: types.Message, state: FSMContext):
    await msg.answer(text=msg.chat.username)