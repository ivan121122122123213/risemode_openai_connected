from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database import (
    get_user,
    add_transaction,
    get_summary,
    get_expenses_by_category,
    get_recent_transactions,
)
from keyboards.money import money_keyboard
from services.money import (
    parse_amount_note,
    category_from_note,
    balance_text,
    expense_impact,
    income_impact,
)
from services.analytics import analytics_text, period_summary_text

router = Router()


class MoneyForm(StatesGroup):
    income = State()
    expense = State()


@router.message(lambda message: message.text == "💰 Деньги")
async def money_menu(message: Message):
    await message.answer(
        "💰 Деньги — это топливо твоей цели. Записывай доходы и расходы.",
        reply_markup=money_keyboard,
    )


@router.message(lambda message: message.text == "➕ Добавить доход")
async def income_start(message: Message, state: FSMContext):
    await state.set_state(MoneyForm.income)
    await message.answer("Напиши доход. Формат: 500 зарплата или 50 подработка")


@router.message(MoneyForm.income)
async def income_finish(message: Message, state: FSMContext):
    try:
        amount, note = parse_amount_note(message.text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Неверный формат. Пример: 500 зарплата")
        return

    add_transaction(
        user_id=message.from_user.id,
        tx_type="income",
        amount=amount,
        category="доход",
        note=note,
    )

    user = get_user(message.from_user.id)
    target = float(user["target_amount"] or 0) if user else 0

    await state.clear()
    await message.answer(f"➕ Доход записан: {amount:.0f}\n" + income_impact(amount, target))


@router.message(lambda message: message.text == "➖ Добавить расход")
async def expense_start(message: Message, state: FSMContext):
    await state.set_state(MoneyForm.expense)
    await message.answer("Напиши расход. Формат: 20 еда или 10 такси")


@router.message(MoneyForm.expense)
async def expense_finish(message: Message, state: FSMContext):
    try:
        amount, note = parse_amount_note(message.text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Неверный формат. Пример: 20 еда")
        return

    category = category_from_note(note)

    add_transaction(
        user_id=message.from_user.id,
        tx_type="expense",
        amount=amount,
        category=category,
        note=note,
    )

    user = get_user(message.from_user.id)
    target = float(user["target_amount"] or 0) if user else 0

    await state.clear()
    await message.answer(f"➖ Расход записан: {amount:.0f}\n" + expense_impact(amount, target))


@router.message(lambda message: message.text == "💰 Баланс")
async def balance(message: Message):
    user = get_user(message.from_user.id)
    summary = get_summary(message.from_user.id)

    current = float(user["current_amount"] or 0) if user else 0
    target = float(user["target_amount"] or 0) if user else 0

    await message.answer(
        balance_text(
            income=float(summary["income"]),
            expense=float(summary["expense"]),
            current=current,
            target=target,
        )
    )


@router.message(lambda message: message.text == "📊 Аналитика")
async def analytics(message: Message):
    rows = get_expenses_by_category(message.from_user.id)
    await message.answer(analytics_text(rows, "все время"))


@router.message(lambda message: message.text == "📆 Неделя")
async def week_summary(message: Message):
    summary = get_summary(message.from_user.id, "week")
    rows = get_expenses_by_category(message.from_user.id, "week")
    await message.answer(period_summary_text(summary, "7 дней") + "\n" + analytics_text(rows, "7 дней"))


@router.message(lambda message: message.text == "🗓 Месяц")
async def month_summary(message: Message):
    summary = get_summary(message.from_user.id, "month")
    rows = get_expenses_by_category(message.from_user.id, "month")
    await message.answer(period_summary_text(summary, "30 дней") + "\n" + analytics_text(rows, "30 дней"))


@router.message(lambda message: message.text == "🧾 История операций")
async def history(message: Message):
    rows = get_recent_transactions(message.from_user.id)

    if not rows:
        await message.answer("Операций пока нет.")
        return

    text = "🧾 Последние операции:\n\n"
    for row in rows:
        sign = "➕" if row["type"] == "income" else "➖"
        text += f"{sign} {row['amount']:.0f} — {row['note'] or row['category']}\n"

    await message.answer(text)
