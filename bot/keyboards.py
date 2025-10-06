from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_input_mode_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Одним повідомленням", callback_data="mode_single"),
            InlineKeyboardButton(text="По черзі", callback_data="mode_chain")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="Створити скріншот", callback_data="create_screenshot")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
