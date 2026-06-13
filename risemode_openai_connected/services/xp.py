def add_xp(current_xp: int, amount: int) -> int:
    return current_xp + amount

def rank_from_xp(xp: int) -> str:
    if xp < 100:
        return "😴 Спящий"
    if xp < 300:
        return "👀 Проснувшийся"
    if xp < 700:
        return "🚶 Идущий"
    if xp < 1500:
        return "⚔️ Машина"
    return "🔥 Монстр дисциплины"
