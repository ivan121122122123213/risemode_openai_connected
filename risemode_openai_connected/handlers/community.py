from aiogram import Router
from aiogram.types import Message
from services.community import community_text

router = Router()

@router.message(lambda m: m.text == "👥 Комьюнити")
async def community(message: Message):
    await message.answer(
        community_text(
            done_today=128,
            failed_today=23
        )
    )
