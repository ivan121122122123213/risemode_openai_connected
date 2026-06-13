from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database import get_user, update_current_amount
from services.plans import goal_plan_text
from texts.messages import NO_GOAL_TEXT

router = Router()


class ProgressForm(StatesGroup):
    new_current = State()


@router.message(lambda message: message.text == "📈 Прогресс")
async def progress_start(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)

    if not user or not user["goal"]:
        await message.answer(NO_GOAL_TEXT)
        return

    await message.answer(
        goal_plan_text(
            user["goal"],
            float(user["target_amount"]),
            float(user["current_amount"] or 0),
            int(user["months"] or 1),
        )
        + "\n\nНапиши, сколько денег сейчас уже есть на цель."
    )
    await state.set_state(ProgressForm.new_current)


@router.message(ProgressForm.new_current)
async def progress_finish(message: Message, state: FSMContext):
    try:
        current = float(message.text.replace(",", "."))
        if current < 0:
            raise ValueError
    except ValueError:
        await message.answer("Напиши число. Например: 350")
        return

    update_current_amount(message.from_user.id, current)
    await state.clear()

    user = get_user(message.from_user.id)

    await message.answer(
        "📈 Прогресс обновлен.\n\n"
        + goal_plan_text(
            user["goal"],
            float(user["target_amount"]),
            float(user["current_amount"] or 0),
            int(user["months"] or 1),
        )
    )
