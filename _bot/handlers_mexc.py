import os
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext

from _bot.keyboards import get_continue_keyboard
from _bot.states import MEXCWithdrawStates
from _modifiers_photo.mexc_withdraw_modifier import render_mexc_withdraw
import config

router = Router()


@router.callback_query(F.data == "select_mexc")
async def select_mexc_withdraw(callback: CallbackQuery, state: FSMContext):
    """Handle MEXC withdrawal selection from main menu."""
    await callback.answer()
    await callback.message.answer("Введіть суму виведення:")
    await state.set_state(MEXCWithdrawStates.waiting_amount)


@router.message(MEXCWithdrawStates.waiting_amount)
async def process_mexc_amount(message: Message, state: FSMContext):
    """Process withdrawal amount (step 1/3)."""
    await state.update_data(amount=message.text)
    await message.answer("Введіть валюту (наприклад, USDT, ETH):")
    await state.set_state(MEXCWithdrawStates.waiting_currency)


@router.message(MEXCWithdrawStates.waiting_currency)
async def process_mexc_currency(message: Message, state: FSMContext):
    """Process currency (step 2/3)."""
    await state.update_data(currency=message.text)
    await message.answer("Введіть адресу гаманця:")
    await state.set_state(MEXCWithdrawStates.waiting_address)


@router.message(MEXCWithdrawStates.waiting_address)
async def process_mexc_address(message: Message, state: FSMContext):
    """Process wallet address (step 3/3) and generate screenshot."""
    await state.update_data(address=message.text)

    try:
        data = await state.get_data()

        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(config.OUTPUT_DIR, f"mexc_{message.from_user.id}.png")

        # Note: You'll need to create a template for MEXC
        template_path = "templates/mexc_withdraw.png"

        result_path = render_mexc_withdraw(
            amount=data["amount"],
            currency=data["currency"],
            address=data["address"],
            template_path=template_path,
            output_path=output_path
        )

        photo = FSInputFile(result_path)
        await message.answer_photo(
            photo,
            caption="✅ Скріншот MEXC виведення готовий!",
            reply_markup=get_continue_keyboard()
        )

        await state.clear()

    except FileNotFoundError:
        await message.answer(
            "❌ Шаблон MEXC не знайдено. Будь ласка, додайте шаблон templates/mexc_withdraw.png"
        )
        await state.clear()
    except Exception as e:
        await message.answer(f"❌ Помилка при створенні скріншоту: {str(e)}")
        await state.clear()
