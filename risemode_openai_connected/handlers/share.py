from aiogram import Router
from aiogram.types import Message

from database import get_user
from services.share import share_progress_text

router = Router()


@router.message(lambda message: message.text == "📤 Поделиться")
async def share(message: Message):
    user = get_user(message.from_user.id)

    if not user:
        await message.answer("Нажми /start")
        return

    await message.answer(
        "Скопируй этот текст и отправь другу или в сторис:\n\n"
        + share_progress_text(
            goal=user["goal"],
            current=float(user["current_amount"] or 0),
            target=float(user["target_amount"] or 0) if user["target_amount"] else None,
            streak=int(user["streak"] or 0),
        )
    )
