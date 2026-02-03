from aiogram import F, Router, types
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, FSInputFile
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from pydantic import ValidationError # Import ValidationError

from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter, IsAdmin
from keybds.inline import *
from keybds.reply import *
from database.orm_query import *
from utils.excel_generator import generate_bought_goods_excel
from database.orm_query import orm_get_formatted_bought_goods_data
from schemas import EventSchema # Import EventSchema


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


#COMMENT код ниже для FSM
class EventAdd(StatesGroup):
    set_event_type = State()
    set_event_name = State()
    set_event_date = State()
    event_confirmation = State()

    texts = {
        'EventAdd:set_event_type': 'Выберите тип мероприятия',
        'EventAdd:set_event_name': 'Введите название мероприятия',
        'EventAdd:set_event_date': 'Введите дату мероприятия (в формате ДД.ММ.ГГГГ)',
    }

class UserScore(StatesGroup):
    score = State()
    submission_id = State()
    user_id = State()

@admin_router.message(Command("admin_menu"))
async def admin_menu(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer('вы вошли как админ', reply_markup=types.ReplyKeyboardRemove())
    await msg.answer(text='меню:', reply_markup=ADMIN_KB)


@admin_router.callback_query(StateFilter(None), F.data == 'add_event')
async def add_event_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Выберите тип мероприятия:', reply_markup=ADD_EVENT_KEYBOARD)
    await state.set_state(EventAdd.set_event_type)

@admin_router.message(F.data)
async def add_event_handler(msg: types.Message, state: FSMContext):
    await msg.answer(text='Вы ввели некорректные данные. Выберите действие:')


#COMMENT отменить действие (сбросить состояние)
@admin_router.message(StateFilter('*'), Command("отмена"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Действия отменены", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Выберите действие:", reply_markup=ADMIN_KB)

#COMMENT вернуться на шаг назад (на предыдущее состояние)
@admin_router.message(StateFilter('*'), Command("назад"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()

    if current_state == EventAdd.set_event_type:
        await message.answer('Предыдущего шага нет, или укажите тип мероприятия или напишите "отмена"', reply_markup=ADD_EVENT_KEYBOARD)
        return
    
    previous = None
    for step in EventAdd.__all_states__:
        if step.state == current_state:
            await state.set_state(previous) 
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n {EventAdd.texts[previous.state]}")
            return
        previous = step


#COMMENT ВЫБОР МЕРОПРИЯТИЯ
@admin_router.message(EventAdd.set_event_type, lambda message: message.text in events)
async def event_type_handler(msg: types.Message, state: FSMContext):
    await state.update_data(set_event_type = msg.text)
    await msg.answer(text=f"тип мероприятия выбран\n({msg.text})\nТеперь введите название мероприятия", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(EventAdd.set_event_name)

@admin_router.message(EventAdd.set_event_type)
async def event_type_handler(msg: types.Message, state: FSMContext):
    await msg.answer(text="вы ввели некорректное значение")

#COMMENT Ловим данные для состояния set_event_name и меняем состояние на set_event_date
@admin_router.message(EventAdd.set_event_name, or_f(F.text, F.text == '.'))
async def event_date_handler(msg: types.Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    event_for_change_id = data.get('event_for_change_id')
    event_for_change = None
    if event_for_change_id:
        event_for_change = await orm_get_event(session, event_for_change_id)

    if msg.text == '.':
        if event_for_change:
            await state.update_data(set_event_name = event_for_change.event_name)
        else:
            await msg.answer("Не удалось найти изменяемое мероприятие. Введите название мероприятия.", reply_markup=types.ReplyKeyboardRemove())
            return
    else:
        await state.update_data(set_event_name = msg.text)
    await msg.answer(
        text=f"название мероприятия выбрано\n({data.get('set_event_name') or msg.text})\nТеперь введите дату мероприятия\n в формате - ДД.ММ.ГГГГ",
        reply_markup=types.ReplyKeyboardRemove()
        )
    await state.set_state(EventAdd.set_event_date)

@admin_router.message(EventAdd.set_event_date)
async def event_info(msg: types.Message, state: FSMContext):
    await state.update_data(set_event_date = msg.text)
    data = await state.get_data()

    try:
        validated_event = EventSchema(
            set_event_type=data['set_event_type'],
            set_event_name=data['set_event_name'],
            set_event_date=data['set_event_date']
        )
        # Store the validated date back into FSMContext as a datetime.date object
        await state.update_data(set_event_date=validated_event.set_event_date)
        
        await msg.answer(text=f"мероприятие добавлено\nТип: {validated_event.set_event_type}\nНазвание: {validated_event.set_event_name}\nДата: {validated_event.set_event_date.strftime('%d.%m.%Y')}")
        await msg.answer(text='Всё верно?', reply_markup=YES_NO_KB)
        await state.set_state(EventAdd.event_confirmation)
    except ValidationError as e:
        await msg.answer(f"Ошибка валидации данных мероприятия: {e.errors()[0]['msg']}\nВведите дату мероприятия заново в формате ДД.ММ.ГГГГ")
        return

#COMMENT Подтверждение добавления мероприятия
@admin_router.callback_query(EventAdd.event_confirmation, F.data == 'yes')
async def event_confirmation(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.update_data(event_confirmation = F.data)
    data = await state.get_data()
    event_for_change_id = data.get('event_for_change_id') # Retrieve event_for_change_id from state
    try:
        # Create a new dictionary with the data to ensure it's clean and contains only schema fields
        event_data_for_orm = {
            "set_event_type": data['set_event_type'],
            "set_event_name": data['set_event_name'],
            "set_event_date": data['set_event_date'] # This is already a datetime.date object
        }

        if event_for_change_id: # Use event_for_change_id from state
            await orm_update_event(session, event_for_change_id, event_data_for_orm)
        else:
            await orm_add_event(session, event_data_for_orm)
        await callback.answer()
        await callback.message.answer("Действие подтверждено\nМероприятие добавлено")
        await state.clear()
        await callback.message.answer("Выберите действие:", reply_markup=ADMIN_KB)
    except Exception as e:
        await callback.message.answer(
            f"Ошибка: \n{str(e)}\n Обратитесь к разработчику", reply_markup=ADMIN_KB)
        await state.clear()

@admin_router.callback_query(EventAdd.event_confirmation, F.data == 'no')
async def event_confirmation(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Действия отменены')
    await state.clear()
    await callback.message.answer("Выберите действие:", reply_markup=ADMIN_KB)

#COMMENT Показать все мероприятия
@admin_router.callback_query(StateFilter(None), F.data == 'show_events')
async def show_events(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    for event in await orm_get_events(session):
        await callback.message.answer(
            f'<i>{event.event_type}</i>\n<strong>{event.event_name}</strong>\n\n<code>{event.event_date}</code>',
            parse_mode='html',
            reply_markup=get_callback_btns(btns={
                'Удалить': f'delete_{event.id}',
                'Изменить': f'change_{event.id}'
            })
        )
    await callback.answer()

#COMMENT Удалить мероприятие
@admin_router.callback_query(F.data.startswith('delete_'))
async def delete_event(callback: CallbackQuery, session: AsyncSession):

    event_id = callback.data.split("_")[-1]
    await orm_delete_event(session, int(event_id))
    await callback.message.delete()

    await callback.answer('Мероприятие удалено')

#COMMENT Изменение мероприятий
@admin_router.callback_query(StateFilter(None), F.data.startswith('change_'))
async def edit_event(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    event_id = callback.data.split("_")[-1]
    await state.update_data(event_for_change_id=int(event_id)) # Store event_id in FSMContext

    await callback.answer()
    await callback.message.answer(
        "Введите тип мероприятия", reply_markup=ADD_EVENT_KEYBOARD
    )
    await state.set_state(EventAdd.set_event_type)

#COMMENT ПРОСМОТР ЗАЯВОК ВОЛОНТЁРОВ
@admin_router.callback_query(StateFilter(None), F.data == 'show_applications')
async def show_all_submissions(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.answer()
    for subm in await orm_get_submissions(session):
        user_id = subm.user_id
        user = await find_by_user_id(session, user_id)
        event = await orm_get_event(session, subm.event_id)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="начислить баллы", callback_data=f"score:{user_id}:{subm.id}")],
        ])
        await callback.message.answer(
            f'<strong>{user.first_name} {user.last_name} {user.group}</strong>\n<i>{subm.subm_text}</i>\n\n{event.event_name}\nДата:{subm.subm_date}',
            parse_mode='html',
            reply_markup=keyboard
        )
    await state.set_state(UserScore.user_id)

#COMMENT ВЫДАЧА БАЛЛОВ
@admin_router.callback_query(UserScore.user_id, F.data.startswith('score:'))
async def add_score1(callback: CallbackQuery, state: FSMContext):
    user_id = callback.data.split(":")[1]
    await state.update_data(user_id = user_id)

    await state.set_state(UserScore.submission_id)
    subm_id = callback.data.split(":")[2]
    await state.update_data(submission_id = subm_id)

    await callback.message.delete()
    await callback.answer()
    await callback.message.answer('Введите, сколько баллов вы хотите начислить (только число):')

    await state.set_state(UserScore.score)

@admin_router.message(UserScore.score)
async def add_score2(msg: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(score = msg.text)

    data = await state.get_data()
    score = int(data['score'])
    user_id = int(data['user_id'])
    subm_id = int(data['submission_id'])
    await orm_delete_subm(session, subm_id)

    await orm_add_score(session, user_id, score)
    await msg.answer('Баллы зачислены!')
    await state.clear()

#COMMENT ПРОСМОТР КУПЛЕННОГО МЕРЧА
@admin_router.callback_query(StateFilter(None), F.data == 'show_bought_goods')
async def show_bought_goods(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    for good in await orm_get_bought_goods(session):
        item = await orm_get_good(session, int(good[0]))
        await callback.message.answer(f'{item.name}: {good[1]}')

#COMMENT СКАЧАТЬ XCEL-ФАЙЛ С КУПЛЕННЫМИ ТОВАРАМИ
@admin_router.callback_query(StateFilter(None), F.data == 'get_excel')
async def send_file_with_bought_goods(callback: types.CallbackQuery, session: AsyncSession):
    await callback.answer("Генерирую Excel файл...")
    data_for_excel = await orm_get_formatted_bought_goods_data(session)
    excel_io = await generate_bought_goods_excel(data_for_excel)
    if excel_io:
        input_file = types.BufferedInputFile(excel_io.getvalue(), filename="bought_goods.xlsx")
        await callback.message.answer_document(input_file)
    else:
        await callback.message.answer("Не удалось сгенерировать файл Excel.")
    # Всегда отвечаем на callback
    await callback.answer()


# Универсальный хендлер для неотловленных callback-кнопок (debug)
@admin_router.callback_query()
async def unknown_callback(callback: CallbackQuery):
    await callback.answer("Неизвестная кнопка или действие!", show_alert=True)



