from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database import create_user
from keyboards.main import main_keyboard
from texts.messages import START_TEXT

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    create_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
    )
    await message.answer(START_TEXT, reply_markup=main_keyboard)


@router.message(lambda message: message.text == "⬅️ Назад")
async def back(message: Message):
    await message.answer("Главное меню.", reply_markup=main_keyboard)
