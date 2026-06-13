def detect_mode(streak: int, has_job: bool, inactive_days: int) -> str:
    if inactive_days >= 3:
        return "💀 Режим застоя"
    if not has_job:
        return "💼 Режим охоты"
    if streak >= 7:
        return "⚔️ Режим дисциплины"
    return "🌱 Режим восстановления"
