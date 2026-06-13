from urllib.parse import quote_plus


def vacancy_links(job_type: str, city: str) -> dict[str, str]:
    query = quote_plus(f"{job_type} {city}")

    if job_type == "онлайн":
        return {
            "💻 Kwork": "https://kwork.ru",
            "💻 FL.ru": "https://www.fl.ru",
            "💻 Upwork": "https://www.upwork.com",
        }

    return {
        "🔎 HH.ru": f"https://hh.ru/search/vacancy?text={query}",
        "🔎 Avito": f"https://www.avito.ru/all/vakansii?q={query}",
        "🔎 Rabota.ru": f"https://www.rabota.ru/vacancy/?query={query}",
    }
