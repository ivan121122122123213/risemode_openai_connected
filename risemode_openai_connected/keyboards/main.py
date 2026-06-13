from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎯 Цель"), KeyboardButton(text="📈 Прогресс")],
        [KeyboardButton(text="💰 Деньги"), KeyboardButton(text="💼 Работа")],
        [KeyboardButton(text="🔥 Серия"), KeyboardButton(text="⚔️ Дисциплина")],
        [KeyboardButton(text="🤖 Наставник"), KeyboardButton(text="👤 Профиль")],
        [KeyboardButton(text="📤 Поделиться"), KeyboardButton(text="👥 Комьюнити")]
    ],
    resize_keyboard=True
)
