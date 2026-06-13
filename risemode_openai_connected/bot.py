import asyncio

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN
from database import init_db, get_all_users_with_reminders

from handlers.start import router as start_router
from handlers.goals import router as goals_router
from handlers.progress import router as progress_router
from handlers.money import router as money_router
from handlers.jobs import router as jobs_router
from handlers.discipline import router as discipline_router
from handlers.streaks import router as streaks_router
from handlers.profile import router as profile_router
from handlers.mentor import router as mentor_router
from handlers.share import router as share_router
from services.reminders import send_evening_reminders


async def main():
    init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(goals_router)
    dp.include_router(progress_router)
    dp.include_router(money_router)
    dp.include_router(jobs_router)
    dp.include_router(discipline_router)
    dp.include_router(streaks_router)
    dp.include_router(profile_router)
    dp.include_router(mentor_router)
    dp.include_router(share_router)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_evening_reminders,
        "interval",
        minutes=1,
        args=[bot, get_all_users_with_reminders],
    )
    scheduler.start()

    print("🔥 RiseMode bot v2 запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
