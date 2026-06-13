def level_name(streak: int, total_steps: int = 0) -> str:
    score = streak + total_steps // 3

    if score < 3:
        return "😴 Спящий"
    if score < 7:
        return "👀 Проснувшийся"
    if score < 14:
        return "🚶 Идущий"
    if score < 30:
        return "⚔️ Машина"
    return "🔥 Монстр дисциплины"
