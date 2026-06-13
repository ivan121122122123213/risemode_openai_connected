def parse_amount_note(text: str) -> tuple[float, str]:
    clean = text.strip().replace(",", ".")
    parts = clean.split(maxsplit=1)

    amount = float(parts[0])
    note = parts[1] if len(parts) > 1 else ""

    return amount, note


def category_from_note(note: str) -> str:
    if not note:
        return "без категории"
    return note.split()[0].lower()


def balance_text(income: float, expense: float, current: float, target: float | None) -> str:
    net = income - expense

    text = f"""
💰 Баланс

➕ Доходы: {income:.0f}
➖ Расходы: {expense:.0f}
🧾 Разница: {net:.0f}
"""

    if target and target > 0:
        percent = min(current / target * 100, 100)
        text += f"""
🎯 В цели сейчас: {current:.0f}
📈 Выполнено: {percent:.0f}%
"""

    return text


def expense_impact(amount: float, target: float | None) -> str:
    if not target or target <= 0:
        return "Расход записан."

    percent = amount / target * 100
    return f"""
⚠️ Эта трата = {percent:.1f}% от твоей цели.

Не запрещаю тратить.
Просто показываю цену решения.
"""


def income_impact(amount: float, target: float | None) -> str:
    if not target or target <= 0:
        return "Доход записан."

    percent = amount / target * 100
    return f"""
🔥 Этот доход = {percent:.1f}% от твоей цели.

Вот так цель становится реальностью.
"""
