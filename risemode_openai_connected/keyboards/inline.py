from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def links_keyboard(links: dict[str, str]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, url=url)]
            for name, url in links.items()
        ]
    )
