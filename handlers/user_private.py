from aiogram import F, types, Router
from aiogram.types import CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from filters.chat_types import ChatTypeFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_events

from keybds.reply import *
from keybds.inline import *
from common.variables import *
from aiogram.methods.send_contact import SendContact


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
    first_name = State()
    second_name = State()
    group = State()
    age = State()
    reg_confirmation = State()

@user_private_router.callback_query(StateFilter(None), F.data == 'reg')
async def add_user_firstname(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.message.answer("Введите своё имя")
    await state.set_state(Reg.first_name)

@user_private_router.message(Reg.first_name)
async def add_user_secondname(msg: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(first_name = msg.text)
    await msg.answer("Введите свою фамилию:")
    await state.set_state(Reg.second_name)

@user_private_router.message(Reg.second_name)
async def add_user_group(msg: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(second_name = msg.text)
    await msg.answer("Введите свою группу:\nПример: '21ИС' (без кавычек)")
    await state.set_state(Reg.group)

@user_private_router.message(Reg.group)
async def add_user_age(msg: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(group = msg.text)
    await msg.answer("Введите свой возраст (только число):")
    await state.set_state(Reg.age)

@user_private_router.message(Reg.age)
async def user_info(msg: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(age = msg.text)
    data = await state.get_data()
    data_arr = []
    for item in data:
        data_arr.append(str(data.get(item)))
    await msg.answer(
        text=f'Имя: {data_arr[0]}\nФамилия: {data_arr[1]}\nГруппа: {data_arr[2]}\nВозраст: {data_arr[3]}')
    await msg.answer(text='Всё верно?', reply_markup=YES_NO_KB)
    await state.set_state(Reg.reg_confirmation)

@user_private_router.callback_query(Reg.reg_confirmation, F.data == 'yes')
async def add_user_confirmation(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.update_data(reg_confirmation = F.data)
    data = await state.get_data()
    await callback.answer()
    await callback.message.answer("Действие подтверждено\nВы зарегистрировались!")
    await state.clear()

@user_private_router.callback_query(Reg.reg_confirmation, F.data == 'no')
async def add_user_confirmation(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.answer('Начнит регистрацию заново')
    await state.clear()
    await callback.message.answer('Выберите, что хотите сделать:', reply_markup=AUTH_BTN)

#TODO добавить результаты добавления пользователя в БД

#COMMENT Показать волонтёрские мероприятия
@user_private_router.callback_query(F.data == 'show_events_user')
async def show_events(callback: CallbackQuery, session: AsyncSession):
    for event in await orm_get_events(session):
        await callback.message.answer(
            f'<i>{event.event_type}</i>\n<strong>{event.event_name}</strong>\n\n<code>{event.event_date}</code>', parse_mode='html')