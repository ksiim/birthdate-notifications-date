import asyncio

from bot import dp, bot

import logging

import handlers
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from models.databases import create_database

from utils.tasks import send_birthday_reminders


logging.basicConfig(level=logging.INFO)


async def main():
    await create_database()
    await initialize_scheduler()
    await dp.start_polling(bot)


async def initialize_scheduler():
    scheduler = AsyncIOScheduler()
    # scheduler.add_job(send_birthday_reminders, trigger="interval", seconds=2)
    scheduler.add_job(send_birthday_reminders, trigger="cron", hour=7)
    scheduler.start()

if __name__ == "__main__":
    asyncio.run(main())
