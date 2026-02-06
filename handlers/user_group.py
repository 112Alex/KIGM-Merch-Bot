from string import punctuation
import re

from aiogram import F, types, Router

from filters.chat_types import ChatTypeFilter

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(['group', 'supergroup']))

restricted_words = {} #NOTE слова, запрещённые в группах
PUNCT_TRANSLATION_TABLE = str.maketrans('', '', punctuation)

def clean_text(text: str):
    return text.translate(PUNCT_TRANSLATION_TABLE)

@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(msg: types.Message):
    if restricted_words.intersection(clean_text(msg.text.lower()).split()):
        await msg.answer(f"{msg.from_user.username}, соблюдайте порядок в чате!")
        await msg.delete()
        # await msg.chat.ban(msg.from_user.id)