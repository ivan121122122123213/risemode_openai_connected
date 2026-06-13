# RiseMode GoalBot v2

В этой версии добавлено:

- автоматические вечерние напоминания через APScheduler;
- таблица reminder_settings;
- OpenAI-наставник при наличии OPENAI_API_KEY;
- fallback-наставник без OpenAI;
- учет откликов на вакансии;
- недельная и месячная финансовая аналитика;
- BOT_USERNAME для share-ссылок.

## Запуск

```bash
pip install -r requirements.txt
```

Переименуй `.env.example` в `.env`:

```env
BOT_TOKEN=твой_telegram_token
OPENAI_API_KEY=
BOT_USERNAME=username_бота_без_@
```

Запуск:

```bash
python bot.py
```

## Важно

Если не добавить OPENAI_API_KEY, наставник всё равно работает по шаблонам.
