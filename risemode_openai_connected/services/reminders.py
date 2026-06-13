from datetime import datetime


def evening_checkin_text(goal: str | None = None, streak: int = 0) -> str:
    goal_line = f"\n🎯 Цель: {goal}" if goal else ""
    return f"""
⏰ Вечерний отчет{goal_line}

🔥 Серия: {streak} дней

Ты сегодня сделал шаг
или снова отложил жизнь на потом?
"""


def job_action_text() -> str:
    return """
💼 Задача на сегодня:
откликнись минимум на 5 вакансий.

Не ищи идеал.
Ищи первый источник денег.
"""


async def send_evening_reminders(bot, get_users_func):
    now = datetime.now()
    users = get_users_func()

    for user in users:
        if int(user["enabled"]) != 1:
            continue

        if int(user["hour"]) == now.hour and int(user["minute"]) == now.minute:
            try:
                await bot.send_message(
                    chat_id=user["user_id"],
                    text=evening_checkin_text(user["goal"], int(user["streak"] or 0)),
                )
            except Exception:
                pass
