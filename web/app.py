from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin, ModelView

from database.engine import engine
from database.models import User, Good, Event, Submission, BoughtGood

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.user_id, User.first_name, User.last_name, User.age, User.group, User.score, User.role]
    column_searchable_list = [User.last_name]
    column_filters = []
    can_create = False  # Users are created by the bot
    can_edit = True
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

    form_edit_columns = [User.score, User.role]

class GoodAdmin(ModelView, model=Good):
    column_list = [Good.id, Good.name, Good.price]
    name = "Товар"
    name_plural = "Товары"
    icon = "fa-solid fa-gem"

class EventAdmin(ModelView, model=Event):
    column_list = [Event.id, Event.event_name, Event.event_date, Event.event_type]
    name = "Мероприятие"
    name_plural = "Мероприятия"
    icon = "fa-solid fa-calendar-days"

class SubmissionAdmin(ModelView, model=Submission):
    column_list = [Submission.id, Submission.subm_text, Submission.subm_date, Submission.event, Submission.user]
    name = "Заявка"
    name_plural = "Заявки"
    icon = "fa-solid fa-file-lines"

class BoughtGoodAdmin(ModelView, model=BoughtGood):
    column_list = [BoughtGood.id, BoughtGood.user, BoughtGood.good, BoughtGood.price_at_purchase, BoughtGood.created_at]
    name = "Купленный товар"
    name_plural = "Купленные товары"
    icon = "fa-solid fa-bag-shopping"


# Add admin
admin = Admin(app, engine)

admin.add_view(UserAdmin)
admin.add_view(GoodAdmin)
admin.add_view(EventAdmin)
admin.add_view(SubmissionAdmin)
admin.add_view(BoughtGoodAdmin)

@app.on_event("startup")
async def on_startup():
    print("FastAPI app started and SQLAdmin initialized.")

@app.get("/")
async def root():
    return {"message": "Welcome to the KIGM Merch Bot Admin Panel!"}

