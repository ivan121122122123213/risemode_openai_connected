def analytics_text(rows, period_title: str = "все время") -> str:
    if not rows:
        return f"📊 За период «{period_title}» расходов пока нет."

    total = sum(float(row["total"] or 0) for row in rows)

    text = f"📊 Аналитика расходов: {period_title}\n\n"

    for row in rows:
        category = row["category"] or "без категории"
        amount = float(row["total"] or 0)
        percent = amount / total * 100 if total else 0
        text += f"— {category}: {amount:.0f} ({percent:.0f}%)\n"

    biggest = rows[0]
    biggest_category = biggest["category"] or "без категории"
    biggest_amount = float(biggest["total"] or 0)

    text += f"""
\nСамая большая категория: {biggest_category} — {biggest_amount:.0f}.

Это не запрет.
Это карта того, куда уходит твоя цель.
"""
    return text


def period_summary_text(summary, period_title: str) -> str:
    income = float(summary["income"] or 0)
    expense = float(summary["expense"] or 0)
    net = income - expense

    return f"""
📆 Финансы: {period_title}

➕ Доходы: {income:.0f}
➖ Расходы: {expense:.0f}
🧾 Остаток: {net:.0f}

Если остаток положительный — ты движешься.
Если отрицательный — цель отдаляется.
"""
