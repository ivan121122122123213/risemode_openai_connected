from aiogram import Router
from aiogram.types import Message

from database import get_user, get_summary
from services.levels import level_name
from services.plans import progress_bar

router = Router()


@router.message(lambda message: message.text == "👤 Профиль")
async def profile(message: Message):
    user = get_user(message.from_user.id)

    if not user:
        await message.answer("Профиль не найден. Нажми /start")
        return

    goal = user["goal"] or "не создана"
    target = float(user["target_amount"] or 0)
    current = float(user["current_amount"] or 0)
    streak = int(user["streak"] or 0)
    best = int(user["best_streak"] or 0)
    total = int(user["total_steps"] or 0)
    has_job = "да" if int(user["has_job"] or 0) else "нет"
    level = level_name(streak, total)

    summary = get_summary(message.from_user.id)

    await message.answer(f"""
👤 Профиль

🎯 Цель: {goal}
📈 Прогресс: {progress_bar(current, target)}

💰 Доходы: {float(summary["income"]):.0f}
💸 Расходы: {float(summary["expense"]):.0f}
💼 Источник дохода: {has_job}

🔥 Серия: {streak} дней
🏆 Лучший streak: {best} дней
✅ Всего шагов: {total}
⚔️ Уровень: {level}
""")
