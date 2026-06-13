from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database import save_job_preference, add_job_application, count_job_applications
from keyboards.jobs import jobs_keyboard
from keyboards.inline import links_keyboard
from services.vacancies import vacancy_links
from services.reminders import job_action_text

router = Router()


class JobsForm(StatesGroup):
    city = State()


JOB_TYPES = {
    "🚴 Курьер": "курьер",
    "🍔 Кафе": "кафе",
    "📦 Склад": "склад",
    "💻 Онлайн": "онлайн",
    "🧹 Разовая подработка": "разовая подработка",
}


@router.message(lambda message: message.text == "💼 Работа")
async def jobs_menu(message: Message):
    await message.answer(
        "💼 Если цель требует денег — ищем источник денег. Выбери сферу:",
        reply_markup=jobs_keyboard,
    )


@router.message(lambda message: message.text in JOB_TYPES)
async def jobs_choose(message: Message, state: FSMContext):
    await state.update_data(job_type=JOB_TYPES[message.text])
    await state.set_state(JobsForm.city)
    await message.answer("В каком городе искать? Например: Москва, СПб, Берлин.")


@router.message(JobsForm.city)
async def jobs_finish(message: Message, state: FSMContext):
    city = message.text.strip()
    data = await state.get_data()
    job_type = data["job_type"]

    save_job_preference(message.from_user.id, job_type, city)
    links = vacancy_links(job_type, city)

    await state.clear()

    await message.answer(
        f"💼 Подборка: {job_type} / {city}\n\n"
        + job_action_text()
        + "\n\nКогда откликнешься — нажми ✅ Я откликнулся.",
        reply_markup=links_keyboard(links),
    )


@router.message(lambda message: message.text == "✅ Я откликнулся")
async def job_applied(message: Message):
    add_job_application(message.from_user.id)
    count = count_job_applications(message.from_user.id)

    await message.answer(f"""
✅ Отклик засчитан.

Всего откликов: {count}

Твоя цель — не один идеальный отклик.
Твоя цель — поток возможностей.
""", reply_markup=jobs_keyboard)
