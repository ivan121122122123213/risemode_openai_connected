from aiogram import Router
from aiogram.types import Message

from database import mark_step_done, mark_failed
from keyboards.discipline import discipline_keyboard
from services.levels import level_name
from texts.messages import DISCIPLINE_TEXT

router = Router()


@router.message(lambda message: message.text == "⚔️ Дисциплина")
async def discipline_menu(message: Message):
    await message.answer(DISCIPLINE_TEXT, reply_markup=discipline_keyboard)


@router.message(lambda message: message.text == "✅ Сделал шаг")
async def did_step(message: Message):
    streak, best, total = mark_step_done(message.from_user.id)
    level = level_name(streak, total)

    await message.answer(f"""
✅ Шаг засчитан.

🔥 Серия: {streak} дней
🏆 Лучший результат: {best} дней
⚔️ Уровень: {level}

Вот так и меняется жизнь.
""")


@router.message(lambda message: message.text == "❌ Слился")
async def failed(message: Message):
    mark_failed(message.from_user.id)
    await message.answer("""
Серия сброшена.

Но это не конец.
Поражение — это когда ты исчез.
Завтра возвращаемся.
""")


@router.message(lambda message: message.text == "📝 Хочу объяснить")
async def explain(message: Message):
    await message.answer("Напиши объяснение, а потом нажми 🤖 Наставник. Он поможет разобрать ситуацию.")
