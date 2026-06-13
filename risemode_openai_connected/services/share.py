from config import BOT_USERNAME


def share_progress_text(goal: str | None, current: float, target: float | None, streak: int) -> str:
    bot_link = f"\n\nПопробуй тоже: https://t.me/{BOT_USERNAME}" if BOT_USERNAME else ""

    if goal and target and target > 0:
        percent = min(current / target * 100, 100)
        return f"""
🔥 Я двигаюсь к цели

🎯 Цель: {goal}
📈 Прогресс: {percent:.0f}%
🔥 Серия: {streak} дней

Я не жду мотивацию.
Я строю систему.{bot_link}
"""

    return f"""
🔥 Я не сливаюсь уже {streak} дней.

Маленькие шаги.
Каждый день.
Без исчезновений.{bot_link}
"""
