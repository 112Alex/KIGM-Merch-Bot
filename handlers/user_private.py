from aiogram import F, types, Router
from aiogram.types import CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from filters.chat_types import ChatTypeFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_events

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

#COMMENT классы состояний
class Auth(StatesGroup): 
    login_check = State()
    password_check = State()

class Reg(StatesGroup):
    registration = State()

class UserDefault(StatesGroup):
    user_state = State()

@user_private_router.callback_query(StateFilter('*'), F.data == 'auth')
async def authorization(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите логин:')
    await state.set_state(Auth.login_check)


@user_private_router.message(Auth.login_check, F.text.lower() == 'user')
async def auth_login_check(msg: types.Message, state: FSMContext):
    await state.update_data(login_check=msg.text)
    await msg.answer(text='Введите пароль:')
    await state.set_state(Auth.password_check)

@user_private_router.message(Auth.login_check)
async def auth_login_check(msg: types.Message, state: FSMContext):
    await msg.answer(text='Пользователь не найден')
    await state.set_state(Auth.login_check)


@user_private_router.message(Auth.password_check, F.text.lower() == 'password')
async def auth_password_check(msg: types.Message, state: FSMContext):
    await state.update_data(password_check=msg.text)
    await msg.answer(text='Данные корректны')
    await state.set_state(UserDefault.user_state)

@user_private_router.message(Auth.password_check)
async def auth_password_check(msg: types.Message, state: FSMContext):
    await msg.answer(text='Данные некорректны \nпопробуйте ввести пароль ещё раз')

@user_private_router.callback_query(F.data == 'show_events_user')
async def show_events(callback: CallbackQuery, session: AsyncSession):
    for event in await orm_get_events(session):
        await callback.message.answer(f'<i>{event.event_type}</i>\n<strong>{event.event_name}</strong>\n<b>{event.event_date}</b>', parse_mode='html')