from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database import get_user, get_summary, count_job_applications
from services.mentor import mentor_response
from texts.messages import MENTOR_TEXT

router = Router()


class MentorForm(StatesGroup):
    problem = State()


@router.message(lambda message: message.text == "🤖 Наставник")
async def mentor_start(message: Message, state: FSMContext):
    await state.set_state(MentorForm.problem)
    await message.answer(MENTOR_TEXT)


@router.message(MentorForm.problem)
async def mentor_finish(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    summary = get_summary(message.from_user.id)
    applications_count = count_job_applications(message.from_user.id)

    try:
        answer = await mentor_response(
            user_text=message.text,
            user=user,
            summary=summary,
            applications_count=applications_count,
        )
    except Exception as e:
        answer = (
            "🤖 Наставник\n\n"
            "Сейчас AI не ответил. Проверь OPENAI_API_KEY и интернет на сервере.\n\n"
            "Но действие на сегодня простое: сделай один маленький шаг к цели за 10 минут."
        )

    await state.clear()
    await message.answer(answer)
