from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

money_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Добавить доход"), KeyboardButton(text="➖ Добавить расход")],
        [KeyboardButton(text="💰 Баланс"), KeyboardButton(text="📊 Аналитика")],
        [KeyboardButton(text="📆 Неделя"), KeyboardButton(text="🗓 Месяц")],
        [KeyboardButton(text="🧾 История операций")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)
