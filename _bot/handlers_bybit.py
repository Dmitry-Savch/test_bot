"""
Bybit Withdraw History Handlers

Handles the conversation flow for collecting Bybit withdrawal history data.
Questions are in Ukrainian.
"""
import os
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext

from _bot.keyboards import get_continue_keyboard
from _bot.states import BybitWithdrawStates
from _modifiers_photo.bybit_withdraw_clp import render_bybit_clp_withdraw_history
from _modifiers_photo.bybit_withdraw_mxn import render_bybit_mxn_withdraw_history
from _modifiers_photo.bybit_withdraw_ved import render_bybit_ved_withdraw_history
import config

router = Router()


def get_currency_keyboard():
    """Create keyboard with currency options."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="CLP"), KeyboardButton(text="MXN"), KeyboardButton(text="VED")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


@router.callback_query(F.data == "select_bybit")
async def select_bybit_withdraw(callback: CallbackQuery, state: FSMContext):
    """Handle Bybit withdrawal history selection from main menu."""
    await callback.answer()
    await callback.message.answer(
        "🏦 <b>Bybit - Історія транзакцій</b>\n\n"
        "Оберіть валюту:",
        reply_markup=get_currency_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(BybitWithdrawStates.waiting_currency)


@router.message(BybitWithdrawStates.waiting_currency)
async def process_currency(message: Message, state: FSMContext):
    """Process currency selection (step 1/9)."""
    currency = message.text.strip().upper()

    if currency not in ["CLP", "MXN", "VED"]:
        await message.answer(
            "❌ Невірна валюта. Будь ласка, оберіть: CLP, MXN або VED",
            reply_markup=get_currency_keyboard()
        )
        return

    await state.update_data(currency=currency)
    await message.answer(
        "📅 Введіть час транзакцій\n"
        "<i>Приклад: Hace un mes, Hace 2 días, Hace una semana</i>",
        parse_mode="HTML"
    )
    await state.set_state(BybitWithdrawStates.waiting_time)


@router.message(BybitWithdrawStates.waiting_time)
async def process_time(message: Message, state: FSMContext):
    """Process transaction time (step 2/9)."""
    await state.update_data(time_in_description=message.text.strip())
    await message.answer(
        "🏦 Введіть назву банку\n"
        "<i>Приклад: Falabella, Banco Estado, Santander</i>",
        parse_mode="HTML"
    )
    await state.set_state(BybitWithdrawStates.waiting_bank)


@router.message(BybitWithdrawStates.waiting_bank)
async def process_bank(message: Message, state: FSMContext):
    """Process bank name (step 3/9)."""
    await state.update_data(lead_bank=message.text.strip())
    await message.answer(
        "🔢 Введіть номер рахунку Ліда (без ****)\n"
        "<i>Приклад: 1999659</i>",
        parse_mode="HTML"
    )
    await state.set_state(BybitWithdrawStates.waiting_lead_number)


@router.message(BybitWithdrawStates.waiting_lead_number)
async def process_lead_number(message: Message, state: FSMContext):
    """Process lead account number (step 4/9)."""
    await state.update_data(lead_number=message.text.strip())
    await message.answer(
        "🔢 Введіть номер рахунку Персонажа (без ****)\n"
        "<i>Приклад: 1509208</i>",
        parse_mode="HTML"
    )
    await state.set_state(BybitWithdrawStates.waiting_persa_number)


@router.message(BybitWithdrawStates.waiting_persa_number)
async def process_persa_number(message: Message, state: FSMContext):
    """Process persa account number (step 5/9)."""
    await state.update_data(persa_number=message.text.strip())
    await message.answer(
        "💰 Введіть суму Транзакції Ліда 10\n"
        "<i>З'явиться в рядках 1 і 3. Приклад: 488.323</i>",
        parse_mode="HTML"
    )
    await state.set_state(BybitWithdrawStates.waiting_transaction_lead_10)


@router.message(BybitWithdrawStates.waiting_transaction_lead_10)
async def process_transaction_lead_10(message: Message, state: FSMContext):
    """Process transaction lead 10 amount (step 6/9)."""
    await state.update_data(transaction_lead_10=message.text.strip())
    await message.answer(
        "💰 Введіть суму Транзакції Ліда\n"
        "<i>З'явиться в рядках 2 і 4. Приклад: 241.579</i>",
        parse_mode="HTML"
    )
    await state.set_state(BybitWithdrawStates.waiting_transaction_lead_main)


@router.message(BybitWithdrawStates.waiting_transaction_lead_main)
async def process_transaction_lead_main(message: Message, state: FSMContext):
    """Process transaction lead main amount (step 7/9)."""
    await state.update_data(transaction_lead_main=message.text.strip())
    await message.answer(
        "💰 Введіть суму Транзакції Ліда 11\n"
        "<i>З'явиться в рядку 5. Приклад: 620.000</i>",
        parse_mode="HTML"
    )
    await state.set_state(BybitWithdrawStates.waiting_transaction_lead_11)


@router.message(BybitWithdrawStates.waiting_transaction_lead_11)
async def process_transaction_lead_11(message: Message, state: FSMContext):
    """Process transaction lead 11 amount (step 8/9)."""
    await state.update_data(transaction_lead_11=message.text.strip())
    await message.answer(
        "💰 Введіть загальну суму виплати\n"
        "<i>З'явиться в рядку 6. Приклад: 4.911.820</i>",
        parse_mode="HTML"
    )
    await state.set_state(BybitWithdrawStates.waiting_total_payout)


@router.message(BybitWithdrawStates.waiting_total_payout)
async def process_total_payout(message: Message, state: FSMContext):
    """Process total payout amount (step 9/9) and generate screenshot."""
    await state.update_data(total_payout=message.text.strip())

    await message.answer("⏳ Генерую скріншот...")

    try:
        data = await state.get_data()

        # Create output directory
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(config.OUTPUT_DIR, f"bybit_{message.from_user.id}.png")

        # Select the appropriate modifier based on currency
        currency = data["currency"]

        if currency == "CLP":
            template_path = "templates/bybit_clp_withdraw_history.png"
            result_path = render_bybit_clp_withdraw_history(
                transaction_lead_10=data["transaction_lead_10"],
                transaction_lead_main=data["transaction_lead_main"],
                transaction_lead_11=data["transaction_lead_11"],
                total_payout=data["total_payout"],
                lead_bank=data["lead_bank"],
                lead_number=data["lead_number"],
                persa_number=data["persa_number"],
                time_in_description=data["time_in_description"],
                template_path=template_path,
                output_path=output_path
            )
        elif currency == "MXN":
            template_path = "templates/bybit_mxn_withdraw_history.png"
            result_path = render_bybit_mxn_withdraw_history(
                transaction_lead_10=data["transaction_lead_10"],
                transaction_lead_main=data["transaction_lead_main"],
                transaction_lead_11=data["transaction_lead_11"],
                total_payout=data["total_payout"],
                lead_bank=data["lead_bank"],
                lead_number=data["lead_number"],
                persa_number=data["persa_number"],
                time_in_description=data["time_in_description"],
                template_path=template_path,
                output_path=output_path
            )
        elif currency == "VED":
            template_path = "templates/bybit_ved_withdraw_history.png"
            result_path = render_bybit_ved_withdraw_history(
                transaction_lead_10=data["transaction_lead_10"],
                transaction_lead_main=data["transaction_lead_main"],
                transaction_lead_11=data["transaction_lead_11"],
                total_payout=data["total_payout"],
                lead_bank=data["lead_bank"],
                lead_number=data["lead_number"],
                persa_number=data["persa_number"],
                time_in_description=data["time_in_description"],
                template_path=template_path,
                output_path=output_path
            )

        # Send the generated screenshot
        photo = FSInputFile(result_path)
        await message.answer_photo(
            photo,
            caption="✅ Скріншот історії виведення Bybit готовий!",
            reply_markup=get_continue_keyboard()
        )

        await state.clear()

    except FileNotFoundError as e:
        await message.answer(
            f"❌ Шаблон не знайдено: {str(e)}\n"
            f"Будь ласка, переконайтеся, що існує templates/bybit_{currency.lower()}_withdraw_history.png"
        )
        await state.clear()
    except Exception as e:
        await message.answer(f"❌ Помилка при створенні скріншоту: {str(e)}")
        await state.clear()
