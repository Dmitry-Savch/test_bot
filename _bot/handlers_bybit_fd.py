"""
Bybit FD (Successful) Handlers

Handles the conversation flow for collecting Bybit FD successful transaction data.
Structure: 11 rows × 6 columns
Questions are in Ukrainian.
"""
import os
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext

from _bot.keyboards import get_continue_keyboard
from _bot.states import BybitFDStates
from _modifiers_photo.white_bybitfd_withdraw_history import render_bybit_fd_successful
import config

router = Router()


def get_currency_keyboard():
    """Create keyboard with currency options."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="MXN"), KeyboardButton(text="ARS")],
            [KeyboardButton(text="$"), KeyboardButton(text="CLP")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


@router.callback_query(F.data == "select_bybit_fd")
async def select_bybit_fd(callback: CallbackQuery, state: FSMContext):
    """Handle Bybit FD selection from main menu."""
    await callback.answer()

    # TEST MODE: Auto-fill all data and generate screenshot
    if config.TEST_MODE:
        await callback.message.answer("🧪 <b>TEST MODE АКТИВНИЙ</b>\nАвтоматичне заповнення даних...", parse_mode="HTML")

        # Fill all test data
        await state.update_data(**config.BYBIT_FD_TEST_DATA)

        # Generate screenshot immediately
        await callback.message.answer("⏳ Генерую скріншот з 11 рядками × 6 колонками...")

        try:
            data = await state.get_data()
            os.makedirs(config.OUTPUT_DIR, exist_ok=True)
            output_path = os.path.join(config.OUTPUT_DIR, f"bybit_fd_{callback.from_user.id}.png")

            result_path = render_bybit_fd_successful(
                currency=data["currency"],
                bank=data["bank"],
                time_in_description=data["time_in_description"],
                status=data["status"],
                lead_payment_amount=data["lead_payment_amount"],
                acter_payment_1=data["acter_payment_1"],
                acter_payment_2=data["acter_payment_2"],
                lead_account_number=data["lead_account_number"],
                acter_account_1=data["acter_account_1"],
                acter_account_2=data["acter_account_2"],
                template_path="templates/bybit_fd/SM_MXN_WHITE_BYBITFD_WITHDRAW_HISTORY.png",
                output_path=output_path
            )

            photo = FSInputFile(result_path)
            await callback.message.answer_photo(
                photo,
                caption="✅ Скріншот Bybit FD (Successful) готовий! (TEST MODE)\n"
                        "11 рядків × 6 колонок заповнено.",
                reply_markup=get_continue_keyboard()
            )

            await state.clear()
            return

        except Exception as e:
            await callback.message.answer(f"❌ Помилка при створенні скріншоту: {str(e)}")
            await state.clear()
            return

    # NORMAL MODE: Original logic
    await callback.message.answer(
        "🏦 <b>Bybit FD - Successful Transaction</b>\n\n"
        "Структура: 11 рядків × 6 колонок\n"
        "Оберіть валюту (заповнить колонку 1, всі 11 рядків):",
        reply_markup=get_currency_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(BybitFDStates.waiting_currency)


@router.message(BybitFDStates.waiting_currency)
async def process_currency(message: Message, state: FSMContext):
    """Process currency selection (fills column 1, all 11 rows)."""
    currency = message.text.strip().upper()

    if currency not in ["MXN", "ARS", "$", "CLP"]:
        await message.answer(
            "❌ Невірна валюта. Будь ласка, оберіть: MXN, ARS, $ або CLP",
            reply_markup=get_currency_keyboard()
        )
        return

    await state.update_data(currency=currency)
    await message.answer(
        "🏦 Введіть назву банку (заповнить колонку 2, всі 11 рядків)\n"
        "<i>Приклад: BVVA, Banco Estado, Santander</i>",
        parse_mode="HTML"
    )
    await state.set_state(BybitFDStates.waiting_bank)


@router.message(BybitFDStates.waiting_bank)
async def process_bank(message: Message, state: FSMContext):
    """Process bank name (fills column 2, all 11 rows)."""
    await state.update_data(bank=message.text.strip())
    await message.answer(
        "📅 Введіть час транзакцій (заповнить колонку 3, всі 11 рядків)\n"
        "<i>Приклад: Hace un año, Hace 2 días, Hace una semana</i>",
        parse_mode="HTML"
    )
    await state.set_state(BybitFDStates.waiting_time)


@router.message(BybitFDStates.waiting_time)
async def process_time(message: Message, state: FSMContext):
    """Process transaction time (fills column 3, all 11 rows)."""
    await state.update_data(time_in_description=message.text.strip())
    await message.answer(
        "✅ Введіть статус транзакцій (заповнить колонку 4, всі 11 рядків)\n"
        "<i>Приклад: Pagado, En proceso, Pendiente</i>",
        parse_mode="HTML"
    )
    await state.set_state(BybitFDStates.waiting_status)


@router.message(BybitFDStates.waiting_status)
async def process_status(message: Message, state: FSMContext):
    """Process transaction status (fills column 4, all 11 rows)."""
    await state.update_data(status=message.text.strip())
    await message.answer(
        "💰 Введіть ОПЛАТА ЛІДА (заповнить колонку 5, перші 9 рядків)\n"
        "<i>Одне значення, яке з'явиться 9 разів. Приклад: 489.000</i>",
        parse_mode="HTML"
    )
    await state.set_state(BybitFDStates.waiting_lead_payment_amount)


@router.message(BybitFDStates.waiting_lead_payment_amount)
async def process_lead_payment_amount(message: Message, state: FSMContext):
    """Process lead payment amount (fills column 5, rows 1-9)."""
    await state.update_data(lead_payment_amount=message.text.strip())
    await message.answer(
        "💰 Введіть ОПЛАТА АКТЕРА #1 (колонка 5, рядок 10)\n"
        "<i>Приклад: 29.320.120</i>",
        parse_mode="HTML"
    )
    await state.set_state(BybitFDStates.waiting_acter_payment_1)


@router.message(BybitFDStates.waiting_acter_payment_1)
async def process_acter_payment_1(message: Message, state: FSMContext):
    """Process acter payment 1 (fills column 5, row 10 and automatically row 11 with same value)."""
    acter_payment = message.text.strip()
    # Automatically use the same value for both ACTER #1 and ACTER #2
    await state.update_data(
        acter_payment_1=acter_payment,
        acter_payment_2=acter_payment
    )
    await message.answer(
        "🔢 Введіть НОМЕР АККА ЛІДА (заповнить колонку 6, перші 9 рядків)\n"
        "Одне значення без ****, з'явиться 9 разів\n"
        "<i>Приклад: 3001382195</i>",
        parse_mode="HTML"
    )
    await state.set_state(BybitFDStates.waiting_lead_account_number)


@router.message(BybitFDStates.waiting_lead_account_number)
async def process_lead_account_number(message: Message, state: FSMContext):
    """Process lead account number (fills column 6, rows 1-9)."""
    await state.update_data(lead_account_number=message.text.strip())
    await message.answer(
        "🔢 Введіть НОМЕР АККА АКТЕРА (колонка 6, рядки 10 та 11)\n"
        "Одне значення для обох рядків, без ****\n"
        "<i>Приклад: 8805356635</i>",
        parse_mode="HTML"
    )
    await state.set_state(BybitFDStates.waiting_acter_account)


@router.message(BybitFDStates.waiting_acter_account)
async def process_acter_account(message: Message, state: FSMContext):
    """Process acter account number and generate screenshot (fills column 6, rows 10-11 with same value)."""
    acter_account = message.text.strip()
    await state.update_data(acter_account=acter_account)

    await message.answer("⏳ Генерую скріншот з 11 рядками × 6 колонками...")

    try:
        data = await state.get_data()

        # Create output directory
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(config.OUTPUT_DIR, f"bybit_fd_{message.from_user.id}.png")

        # Render using bybit_fd renderer
        # Use the same acter_account value for both rows 10 and 11
        result_path = render_bybit_fd_successful(
            currency=data["currency"],
            bank=data["bank"],
            time_in_description=data["time_in_description"],
            status=data["status"],
            lead_payment_amount=data["lead_payment_amount"],
            acter_payment_1=data["acter_payment_1"],
            acter_payment_2=data["acter_payment_2"],
            lead_account_number=data["lead_account_number"],
            acter_account_1=data["acter_account"],
            acter_account_2=data["acter_account"],
            template_path="templates/bybit_fd/successful.png",
            output_path=output_path
        )

        # Send the generated screenshot
        photo = FSInputFile(result_path)
        await message.answer_photo(
            photo,
            caption="✅ Скріншот Bybit FD (Successful) готовий!\n"
                    "11 рядків × 6 колонок заповнено.",
            reply_markup=get_continue_keyboard()
        )

        await state.clear()

    except FileNotFoundError as e:
        await message.answer(
            f"❌ Шаблон не знайдено: {str(e)}\n"
            f"Будь ласка, переконайтеся, що існує templates/bybit_fd/SM_MXN_WHITE_BYBITFD_WITHDRAW_HISTORY.png"
        )
        await state.clear()
    except Exception as e:
        await message.answer(f"❌ Помилка при створенні скріншоту: {str(e)}")
        await state.clear()
