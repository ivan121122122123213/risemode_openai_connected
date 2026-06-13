from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

goals_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Создать цель")],
        [KeyboardButton(text="👀 Посмотреть цель"), KeyboardButton(text="✏️ Изменить цель")],
        [KeyboardButton(text="🗑 Удалить цель")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)
