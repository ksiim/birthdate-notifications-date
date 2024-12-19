import datetime
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from bot import bot

from .callbacks import *


async def generate_start_text(message):
    return f"Привет, {message.from_user.full_name}! ✌️ Я - бот, призванный напоминать вам о Днях рождения ваших партнеров, коллег и друзей!"


async def generate_full_birthday_text(fio: str, post: str, company: str, birthdate: datetime.date):
    years_old = datetime.datetime.now().year - birthdate.year
    return f'''Сегодня празднует День рождения {fio}, {post.lower()} компании {company}. Исполнилось {await get_year_word_form(years_old)}!'''

async def generate_short_birthday_text(fio: str):
    return f'''Сегодня празднует День рождения {fio}!'''

async def send_message(chat_id, message_text):
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=message_text,
        )
    except Exception as e:
        print(e)

async def get_year_word_form(years_old: int):
    if years_old % 10 == 1 and years_old % 100 != 11:
        return f"{years_old} год"
    elif 1 < years_old % 10 < 5 and not 11 < years_old % 100 < 15:
        return f"{years_old} года"
    else:
        return f"{years_old} лет"
