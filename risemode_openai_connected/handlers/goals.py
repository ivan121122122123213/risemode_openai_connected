from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database import get_user, save_goal, delete_goal, set_has_job
from keyboards.goals import goals_keyboard
from keyboards.main import main_keyboard
from keyboards.jobs import jobs_keyboard
from services.plans import goal_plan_text
from texts.messages import GOAL_INTRO_TEXT, NO_GOAL_TEXT

router = Router()


class GoalForm(StatesGroup):
    goal = State()
    target = State()
    months = State()
    current = State()
    has_job = State()


@router.message(lambda message: message.text == "🎯 Цель")
async def goals_menu(message: Message):
    await message.answer(GOAL_INTRO_TEXT, reply_markup=goals_keyboard)


@router.message(lambda message: message.text in ["➕ Создать цель", "✏️ Изменить цель"])
async def create_goal_start(message: Message, state: FSMContext):
    await state.set_state(GoalForm.goal)
    await message.answer("Что ты хочешь изменить или получить? Например: купить ноутбук, сдать на права, накопить на переезд.")


@router.message(GoalForm.goal)
async def create_goal_name(message: Message, state: FSMContext):
    await state.update_data(goal=message.text.strip())
    await state.set_state(GoalForm.target)
    await message.answer("Сколько это стоит? Напиши только число.")


@router.message(GoalForm.target)
async def create_goal_target(message: Message, state: FSMContext):
    try:
        target = float(message.text.replace(",", "."))
        if target <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Напиши число больше нуля. Например: 800")
        return

    await state.update_data(target=target)
    await state.set_state(GoalForm.months)
    await message.answer("За сколько месяцев хочешь достичь цели?")


@router.message(GoalForm.months)
async def create_goal_months(message: Message, state: FSMContext):
    try:
        months = int(message.text)
        if months <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Напиши целое число. Например: 4")
        return

    await state.update_data(months=months)
    await state.set_state(GoalForm.current)
    await message.answer("Сколько уже есть денег на эту цель? Если ничего — напиши 0.")


@router.message(GoalForm.current)
async def create_goal_current(message: Message, state: FSMContext):
    try:
        current = float(message.text.replace(",", "."))
        if current < 0:
            raise ValueError
    except ValueError:
        await message.answer("Напиши число. Например: 100 или 0")
        return

    await state.update_data(current=current)
    await state.set_state(GoalForm.has_job)
    await message.answer("У тебя есть стабильный источник дохода? Ответь: да или нет.")


@router.message(GoalForm.has_job)
async def create_goal_finish(message: Message, state: FSMContext):
    answer = message.text.lower().strip()

    if answer not in ["да", "нет"]:
        await message.answer("Ответь только: да или нет.")
        return

    data = await state.get_data()
    has_job = 1 if answer == "да" else 0

    save_goal(
        user_id=message.from_user.id,
        goal=data["goal"],
        target_amount=data["target"],
        current_amount=data["current"],
        months=data["months"],
    )
    set_has_job(message.from_user.id, has_job)

    await state.clear()

    text = "✅ Цель сохранена.\n\n" + goal_plan_text(
        data["goal"],
        data["target"],
        data["current"],
        data["months"],
    )

    if has_job:
        await message.answer(text, reply_markup=main_keyboard)
    else:
        await message.answer(
            text + "\n\nДохода нет — значит сначала ищем источник денег. Выбери тип подработки:",
            reply_markup=jobs_keyboard,
        )


@router.message(lambda message: message.text == "👀 Посмотреть цель")
async def show_goal(message: Message):
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
    )


@router.message(lambda message: message.text == "🗑 Удалить цель")
async def remove_goal(message: Message):
    delete_goal(message.from_user.id)
    await message.answer("Цель удалена. Можно создать новую.", reply_markup=goals_keyboard)
