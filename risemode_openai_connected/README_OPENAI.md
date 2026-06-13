# OpenAI API подключен

AI-наставник работает через OpenAI API.

## Перед запуском

1. Переименуй `.env.example` в `.env`

2. Заполни:

```env
BOT_TOKEN=токен_от_BotFather
OPENAI_API_KEY=ключ_OpenAI_API
BOT_USERNAME=username_бота_без_@
```

3. Установи зависимости:

```bash
pip install -r requirements.txt
```

4. Запусти:

```bash
python bot.py
```

## Как работает AI-наставник

Файл:

```text
services/mentor.py
```

Он получает:
- сообщение пользователя;
- цель;
- сумму;
- прогресс;
- доходы;
- расходы;
- streak;
- наличие работы;
- число откликов.

После этого отправляет всё в OpenAI и возвращает персональный ответ.
