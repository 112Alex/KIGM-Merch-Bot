from aiogram import F, types, Router
from aiogram.types import CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from filters.chat_types import ChatTypeFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import (
    orm_add_submission, orm_add_user, orm_check_score, orm_check_user_goods,
    orm_get_events, orm_get_goods,
    orm_show_score, find_by_user_id,
    orm_get_good, orm_add_bought_good
    )

from keybds.reply import *
from keybds.inline import *
from common.variables import *


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private', 'group']))


#COMMENT ОБРАБОТКА КОМАНДЫ /start
@user_private_router.message(StateFilter(None), CommandStart())
async def handle_start(msg: types.Message, session: AsyncSession, state: FSMContext):
    user_id = msg.from_user.id
    result = await find_by_user_id(session, user_id)
    #Проверка на существование пользователя в БД
    if result == None:
        await msg.answer(text=f'Привет, {msg.from_user.full_name}')
        await msg.answer(text=HELLO_TEXT) # Приветственный текст (хранится в переменном окружении)
        await msg.answer(text='Пожалуйста, зарегестрируйтесь', reply_markup=AUTH_BTN)
    elif result != None:
        await msg.answer('вы авторизованы', reply_markup=SHOW_MENU_KB)
        await state.set_state(Authorized.zaglushka)

#NOTE УЗНАТЬ TELEGRAM-ID ЧЕРЕЗ БОТА (НЕ ИСПОЛЬЗУЕТСЯ)
# @user_private_router.message(Command('id'))
# async def chek_id(msg: types.Message):
#     await msg.answer(text=f'Ваш ID: {msg.from_user.id}')
#     print(f'/id call! ==> id:{msg.from_user.id} ник: @{msg.from_user.username} имя: {msg.from_user.first_name} {msg.from_user.last_name} ')
    

#COMMENT КЛАССЫ МАШИНЫ СОСТОЯНИЙ FSM
class Authorized(StatesGroup):
    zaglushka = State()

class Reg(StatesGroup):
    first_name = State()
    last_name = State()
    group = State()
    age = State()
    reg_confirmation = State()

class Subm(StatesGroup):
    event_id = State()
    name = State()
    subm_date = State()
    confirmation = State()

class Good_buying(StatesGroup):
    good_choice = State()
    confirmation = State()
    price = State()


@user_private_router.callback_query(StateFilter(None), F.data == 'reg')
async def add_user_firstname(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.message.answer("Введите своё имя")
    await state.set_state(Reg.first_name)

@user_private_router.message(Reg.first_name)
async def add_user_secondname(msg: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(first_name = msg.text)
    await msg.answer("Введите свою фамилию:")
    await state.set_state(Reg.last_name)

@user_private_router.message(Reg.last_name)
async def add_user_group(msg: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(last_name = msg.text)
    await msg.answer("Введите свою группу:\nПример: '21ИС' (без кавычек)")
    await state.set_state(Reg.group)

@user_private_router.message(Reg.group)
async def add_user_age(msg: types.Message, state: FSMContext, session: AsyncSession):
    if len(msg.text) <= 5:
        await state.update_data(group = msg.text)
        await state.set_state(Reg.age)
        await msg.answer("Введите свой возраст (только число):")
    else:
        await msg.answer('Ввведено некорректное значение. Попробуйте ввести название группы снова')
        return
    

@user_private_router.message(Reg.age)
async def user_info(msg: types.Message, state: FSMContext, session: AsyncSession):
    try:
        if int(msg.text) > 14 and int(msg.text) < 99:
            await state.update_data(age = msg.text)
            data = await state.get_data()
            data_arr = []
            for item in data:
                data_arr.append(str(data.get(item)))
            await msg.answer(
                text=f'Имя: {data_arr[0]}\nФамилия: {data_arr[1]}\nГруппа: {data_arr[2]}\nВозраст: {data_arr[3]}')
            await msg.answer(text='Всё верно?', reply_markup=YES_NO_KB)
            await state.set_state(Reg.reg_confirmation)
        else:
            await msg.answer('Введено некорректное значение. Попробуйте снова')
            return
    except ValueError:
        await msg.answer('Введено некорректное значение. Попробуйте снова')
        return

#COMMENT ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯ
@user_private_router.callback_query(Reg.reg_confirmation, F.data == 'yes')
async def add_user_confirmation(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    user = callback.from_user
    await state.update_data(reg_confirmation = F.data)
    data = await state.get_data()

    await orm_add_user(
        session,
        user_id=user.id,
        first_name=data['first_name'],
        last_name=data['last_name'],
        group=data['group'],
        age=int(data['age']),
    )

    await callback.answer()
    await callback.message.answer(f"Действие подтверждено\nВы зарегистрировались!", reply_markup=SHOW_MENU_KB)
    await state.set_state(Authorized.zaglushka)

# перезапуск функции добавления пользователя
@user_private_router.callback_query(Reg.reg_confirmation, F.data == 'no')
async def add_user_confirmation(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.answer('Действия отменены!')
    await state.clear()
    await callback.message.answer('Начните регистрацию заново', reply_markup=AUTH_BTN)

#COMMENT ПОКАЗАТЬ МЕРОПРИЯТИЯ
@user_private_router.message(StateFilter(Authorized), F.text.lower() == 'получить баллы')
async def show_events(msg: types.Message, session: AsyncSession):
    events = await orm_get_events(session)
    await msg.answer('Вот список мероприятий:')
    for event in events:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="отметить участие", callback_data=f"request:{event.id}")],
        ])
        
        await msg.answer(
            text=SHOW_EVENT_TEXT(event.event_type, event.event_name, event.event_date),
            parse_mode='html', reply_markup=keyboard
        )
            

#COMMENT УЗНАТЬ КОЛ-ВО БАЛЛОВ
@user_private_router.message(StateFilter(Authorized), F.text.lower() == 'узнать количество баллов')
async def show_score(msg: types.Message, session: AsyncSession):
    result = await orm_show_score(session, int(msg.from_user.id))
    await msg.answer(f'Ваше количество накопленных баллов:\n{result}')

#COMMENT ВЫБРАТЬ МЕРОПРИЯТИЕ ДЛЯ ЗАЯВКИ
@user_private_router.callback_query(StateFilter(Authorized), F.data.startswith('request:'))
async def submit_application(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Subm.event_id)
    event_id = callback.data.split(':')[1]
    await state.update_data(event_id = event_id)
    await callback.message.answer(f"Подробно и достоверно опишите, что вы делали на данном мероприятии:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Subm.name)

@user_private_router.message(Subm.name)
async def submit_app_text(msg: types.Message, state: FSMContext):
    await state.update_data(name = msg.text)
    await msg.answer('Теперь введите дату или промежуток времени, когда вы принимали участие в мероприятии')
    await state.set_state(Subm.subm_date)

@user_private_router.message(Subm.subm_date)
async def submit_app_date(msg: types.Message, state: FSMContext):
    await state.update_data(subm_date = msg.text)
    data = await state.get_data()
    await msg.answer(f'{data['name']}\n{data['subm_date']}\nВсё верно?', reply_markup=YES_NO_KB)
    await state.set_state(Subm.confirmation)

@user_private_router.callback_query(Subm.confirmation, F.data == 'yes')
async def subm_confirm_yes(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    event_id = int(data['event_id'])
    text = data['name']
    sdate = data['subm_date']
    user_id = int(callback.from_user.id)
    await orm_add_submission(session, text, sdate, event_id, user_id)
    await callback.answer()
    await callback.message.answer('Действия подтверждены', reply_markup=SHOW_MENU_KB)
    await state.set_state(Authorized.zaglushka)

@user_private_router.callback_query(Subm.confirmation, F.data == 'no')
async def subm_confirm_no(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Действия отменены')
    await callback.message.answer('Действия отменены')
    await state.set_state(Authorized.zaglushka)


#COMMENT ПРОСМОТР АССОРТИМЕНТА
@user_private_router.message(StateFilter(Authorized), F.text.lower() == 'купить мерч')
async def show_goods(msg: types.Message, state: FSMContext, session: AsyncSession):
    await msg.answer('Вот список товаров:', reply_markup=types.ReplyKeyboardRemove())
    goods = await orm_get_goods(session)

    for good in goods:
        keyboard_good = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="купить", callback_data=f"good:{good.id}:{good.price}")],
        ])
        await msg.answer(f'{good.name}\nСтоимость: {good.price}', parse_mode='html', reply_markup=keyboard_good)
    
    await state.set_state(Good_buying.good_choice)

@user_private_router.callback_query(Good_buying.good_choice, F.data.startswith('good:'))
async def show_confirm(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    good_id = callback.data.split(':')[1]
    good_price = callback.data.split(':')[2]
    user_id = callback.from_user.id

    await state.update_data(good_choice=good_id)
    await state.set_state(Good_buying.price)
    await state.update_data(price = good_price)

    good = await orm_get_good(session, int(good_id))  # Получаем товар по ID, а не по имени
    await callback.answer()
    
    if await orm_check_score(session, float(good_price), int(user_id)) == True:
        if await orm_check_user_goods(session, int(user_id), int(good_id)) == False:
            await callback.message.answer(f'Вы действительно хотите купить {good.name} за {good.price}?', reply_markup=YES_NO_KB)
            await state.set_state(Good_buying.confirmation)
        else:
            await callback.message.answer('Вы уже покупали этот товар!', reply_markup=SHOW_MENU_KB)
            await state.set_state(Authorized.zaglushka)
            return
    else:
        await callback.message.answer('У вас не хватает баллов!', reply_markup=SHOW_MENU_KB)
        await state.set_state(Authorized.zaglushka)
    

# ДА
@user_private_router.callback_query(Good_buying.confirmation, F.data == 'yes')
async def show_confirm(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    user_id = int(callback.from_user.id)
    good_id = int(data['good_choice'])
    good_price = float(data['price'])

    await orm_add_bought_good(session, good_id, user_id, good_price)

    await callback.answer()
    await callback.message.answer('Действия подтверждены', reply_markup=SHOW_MENU_KB)
    await state.set_state(Authorized.zaglushka)
# НЕТ
@user_private_router.callback_query(Good_buying.confirmation, F.data == 'no')
async def show_confirm(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Authorized.zaglushka)
    await callback.message.answer('Действия отменены', reply_markup=SHOW_MENU_KB)


