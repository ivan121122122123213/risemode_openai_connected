from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

jobs_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚴 Курьер"), KeyboardButton(text="🍔 Кафе")],
        [KeyboardButton(text="📦 Склад"), KeyboardButton(text="💻 Онлайн")],
        [KeyboardButton(text="🧹 Разовая подработка")],
        [KeyboardButton(text="✅ Я откликнулся")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)
