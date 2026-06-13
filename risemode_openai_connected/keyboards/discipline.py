from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

discipline_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Сделал шаг")],
        [KeyboardButton(text="❌ Слился")],
        [KeyboardButton(text="📝 Хочу объяснить")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)
