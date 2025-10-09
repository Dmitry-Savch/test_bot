from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from _bot.keyboards import get_main_selection_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Handle /start command."""
    await state.clear()
    await message.answer(
        "👋 Вітаю! Я бот для створення скріншотів.\n\n"
        "Використовуйте команду /kb для вибору типу скріншота.",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command."""
    await message.answer(
        "ℹ️ Доступні команди:\n\n"
        "/start - Почати роботу з ботом\n"
        "/kb - Показати клавіатуру вибору\n"
        "/help - Показати цю довідку\n\n"
        "Виберіть тип скріншота та слідуйте інструкціям."
    )


@router.message(Command("kb"))
async def cmd_keyboard(message: Message, state: FSMContext):
    """Handle /kb command - show main selection keyboard."""
    await state.clear()
    # Remove old reply keyboard first
    await message.answer(
        "Оберіть тип скріншота:",
        reply_markup=ReplyKeyboardRemove()
    )
    # Then show inline keyboard
    await message.answer(
        "Оберіть тип скріншота:",
        reply_markup=get_main_selection_keyboard()
    )


@router.callback_query(F.data == "back_to_menu")
async def process_back_to_menu(callback: CallbackQuery, state: FSMContext):
    """Handle back to menu button."""
    await state.clear()
    await callback.answer()
    await callback.message.answer(
        "Оберіть тип скріншота:",
        reply_markup=get_main_selection_keyboard()
    )


@router.callback_query(F.data == "create_another")
async def process_create_another(callback: CallbackQuery, state: FSMContext):
    """Handle create another screenshot button."""
    await state.clear()
    await callback.answer()
    await callback.message.answer(
        "Оберіть тип скріншота:",
        reply_markup=get_main_selection_keyboard()
    )
