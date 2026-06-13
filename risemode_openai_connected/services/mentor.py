from openai import AsyncOpenAI
from config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
Ты AI-наставник Telegram-бота RiseMode.

Миссия продукта:
помочь человеку выйти из застоя через связку:
цель → деньги → работа → дисциплина → прогресс.

Стиль:
- коротко;
- прямо;
- без токсичности;
- без длинных лекций;
- без абстрактной мотивации;
- максимум конкретики;
- 1-3 действия на сегодня.

Ты НЕ психолог, НЕ врач, НЕ финансовый консультант.
Не давай медицинских, юридических или инвестиционных обещаний.
Если человек пишет про самоповреждение или суицид, мягко предложи обратиться к близким и в экстренные службы.

Всегда отвечай на русском.
"""


def build_user_context(user, summary=None, applications_count: int = 0) -> str:
    if not user:
        return "Данных о пользователе пока нет."

    goal = user["goal"] or "цель не создана"
    target = float(user["target_amount"] or 0)
    current = float(user["current_amount"] or 0)
    months = int(user["months"] or 0)
    has_job = "да" if int(user["has_job"] or 0) else "нет"
    streak = int(user["streak"] or 0)
    best_streak = int(user["best_streak"] or 0)
    total_steps = int(user["total_steps"] or 0)
    preferred_job = user["preferred_job"] or "не выбрано"
    city = user["city"] or "не указан"

    income = float(summary["income"] or 0) if summary else 0
    expense = float(summary["expense"] or 0) if summary else 0

    progress = 0
    if target > 0:
        progress = min(current / target * 100, 100)

    return f"""
Данные пользователя:
- цель: {goal}
- нужно: {target:.0f}
- уже есть: {current:.0f}
- прогресс: {progress:.0f}%
- срок: {months} месяцев
- есть источник дохода: {has_job}
- выбранная работа/подработка: {preferred_job}
- город: {city}
- streak: {streak}
- лучший streak: {best_streak}
- всего шагов: {total_steps}
- доходы: {income:.0f}
- расходы: {expense:.0f}
- отклики на работу: {applications_count}
"""


async def mentor_response(user_text: str, user=None, summary=None, applications_count: int = 0) -> str:
    user_context = build_user_context(user, summary, applications_count)

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"{user_context}\n\nСообщение пользователя:\n{user_text}",
            },
        ],
        temperature=0.7,
        max_tokens=450,
    )

    return "🤖 Наставник\n\n" + response.choices[0].message.content.strip()
