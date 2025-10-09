from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_selection_keyboard() -> InlineKeyboardMarkup:
    """Main keyboard with all screenshot type options (for /kb command)."""
    keyboard = [
        [InlineKeyboardButton(text="🏦 Bybit Withdraw", callback_data="select_bybit")],
        # [InlineKeyboardButton(text="🏦 MEXC Withdraw", callback_data="select_mexc")],  # TODO: Update MEXC
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_input_mode_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for choosing input mode (single message or step by step)."""
    keyboard = [
        [
            InlineKeyboardButton(text="Одним повідомленням", callback_data="mode_single"),
            InlineKeyboardButton(text="По черзі", callback_data="mode_chain")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_continue_keyboard() -> InlineKeyboardMarkup:
    """Keyboard to create another screenshot."""
    keyboard = [
        [InlineKeyboardButton(text="Створити ще скріншот", callback_data="create_another")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """Keyboard to return to main menu."""
    keyboard = [
        [InlineKeyboardButton(text="⬅️ Назад до меню", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
