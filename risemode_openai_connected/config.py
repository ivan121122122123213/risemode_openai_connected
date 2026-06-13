import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BOT_USERNAME = os.getenv("BOT_USERNAME", "")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден. Создай .env и добавь BOT_TOKEN=твой_токен")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY не найден. Добавь ключ OpenAI в .env")
