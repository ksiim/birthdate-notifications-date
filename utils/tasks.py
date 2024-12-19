import asyncio
import datetime
from handlers.markups import generate_full_birthday_text, generate_short_birthday_text, send_message
from models.dbs.orm import Orm
from utils.table_parser import Parser


async def send_birthday_reminders():
    full_parser = Parser('tables/full.xlsx')
    full_data = await full_parser.parse()
    await full_parser.close()

    short_parser = Parser('tables/short.xlsx')
    short_data = await short_parser.parse()
    await short_parser.close()
    
    message_texts = []

    await generate_full_birthday_messages(full_data, message_texts)

    await generate_short_birthday_messages(short_data, message_texts)
    
    await send_messages_to_users(message_texts, 30)

async def generate_short_birthday_messages(short_data, message_texts):
    for row in short_data:
        fio, birthdate = row[:2]
        if await today_is_birth_day(birthdate.date(), datetime.datetime.now().date()):
            text = await generate_short_birthday_text(fio)
            message_texts.append(text)

async def generate_full_birthday_messages(full_data, message_texts):
    for row in full_data:
        fio, post, birthdate, company = row[:4]
        if await today_is_birth_day(birthdate.date(), datetime.datetime.now().date()):
            text = await generate_full_birthday_text(fio, post, company, birthdate)
            message_texts.append(text)


async def today_is_birth_day(birthdate: datetime.date, today: datetime.date):
    return birthdate.day == today.day and birthdate.month == today.month


async def send_messages_to_users(message_texts, chunk_size=30):
    users = await Orm.get_all_users()
    
    tasks = []
    
    for user in users:
        for message_text in message_texts:
            tasks.append(send_message(user.telegram_id, message_text))
            
    for i in range(0, len(tasks), chunk_size):
        await asyncio.gather(*tasks[i:i + chunk_size])

