# keyboards/inline.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from texts.content import DONATE_METHODS

def main_menu_keyboard():
    """Главное меню под сообщением /start"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔬 О проекте", callback_data="about")],
        [InlineKeyboardButton(text="💰 Поддержать", callback_data="donate")],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="help")],
    ])

def donate_methods_keyboard():
    """Клавиатура выбора способа доната"""
    buttons = []
    for i, method in enumerate(DONATE_METHODS):
        buttons.append([
            InlineKeyboardButton(
                text=method["name"],
                callback_data=f"donate_method_{i}"
            )
        ])
    buttons.append([
        InlineKeyboardButton(text="✅ Я перевёл", callback_data="donate_confirm")
    ])
    buttons.append([
        InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def back_to_main_keyboard():
    """Кнопка возврата в главное меню"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_main")]
    ])
