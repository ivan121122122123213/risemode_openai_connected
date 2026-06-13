from aiogram import Router
from aiogram.types import Message

from database import get_user
from services.streaks import streak_message

router = Router()


@router.message(lambda message: message.text == "🔥 Серия")
async def streak(message: Message):
    user = get_user(message.from_user.id)

    streak_value = int(user["streak"] or 0) if user else 0
    best = int(user["best_streak"] or 0) if user else 0

    await message.answer(streak_message(streak_value, best))
