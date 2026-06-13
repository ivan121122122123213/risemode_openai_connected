def progress_bar(current: float, target: float, blocks: int = 10) -> str:
    if target <= 0:
        return "░" * blocks + " 0%"

    ratio = max(0, min(current / target, 1))
    filled = int(ratio * blocks)
    return "█" * filled + "░" * (blocks - filled) + f" {int(ratio * 100)}%"


def calculate_plan(target: float, current: float, months: int) -> dict:
    remaining = max(target - current, 0)
    months = max(months, 1)

    monthly = remaining / months
    weekly = monthly / 4
    daily = weekly / 7

    return {
        "remaining": remaining,
        "monthly": monthly,
        "weekly": weekly,
        "daily": daily,
    }


def goal_plan_text(goal: str, target: float, current: float, months: int) -> str:
    plan = calculate_plan(target, current, months)

    if plan["remaining"] <= 0:
        return f"""
🎉 Цель достигнута.

🎯 {goal}

Ты доказал себе, что можешь доводить до конца.
"""

    return f"""
🎯 Твоя цель: {goal}

💰 Нужно: {target:.0f}
💵 Уже есть: {current:.0f}
📉 Осталось: {plan["remaining"]:.0f}
⏳ Срок: {months} мес.

Чтобы дойти:
— в месяц: {plan["monthly"]:.0f}
— в неделю: {plan["weekly"]:.0f}
— в день: {plan["daily"]:.0f}

📈 Прогресс:
{progress_bar(current, target)}

Первый шаг:
сегодня сделай одно действие, которое приблизит тебя к цели.
"""
