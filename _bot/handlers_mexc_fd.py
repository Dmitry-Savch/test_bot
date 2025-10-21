"""
MEXC FD Handlers

Handles the conversation flow for collecting MEXC FD transaction data.
Structure: 10 rows × 6 columns
Questions are in Ukrainian.
"""
import os
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from _bot.keyboards import get_continue_keyboard
from _bot.states import MEXCFDStates
from _modifiers_photo.mexcfd_withdraw_history import render_mexc_fd
import config

router = Router()


def get_currency_keyboard():
    """Create keyboard with currency options."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="ARS"), KeyboardButton(text="COP")],
            [KeyboardButton(text="CLP"), KeyboardButton(text="USD")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


@router.callback_query(F.data == "select_mexc_fd")
async def select_mexc_fd(callback: CallbackQuery, state: FSMContext):
    """Handle MEXC FD selection from main menu."""
    await callback.answer()

    # TEST MODE: Auto-fill all data and generate screenshot
    if config.TEST_MODE:
        await callback.message.answer("🧪 <b>TEST MODE АКТИВНИЙ</b>\nАвтоматичне заповнення даних...", parse_mode="HTML")

        # Fill all test data
        await state.update_data(**config.MEXC_FD_TEST_DATA)

        # Generate screenshot immediately
        await callback.message.answer("⏳ Генерую скріншот з 10 рядками × 6 колонками...")

        try:
            data = await state.get_data()
            os.makedirs(config.OUTPUT_DIR, exist_ok=True)
            output_path = os.path.join(config.OUTPUT_DIR, f"mexc_fd_{callback.from_user.id}.png")

            # Map currency to template filename
            currency = data["currency"]
            currency_template_map = {
                "CLP": "templates/mexc_fd/SD_CLP_MEXCFD_WITHDRAW_HISTORY.png",
                "COP": "templates/mexc_fd/SH_COP_MEXCFD_WITHDRAW_HISTORY.png",
                "ARS": "templates/mexc_fd/SR_ARS_MEXCFD_WITHDRAW_HISTORY.png",
                "USD": "templates/mexc_fd/SR_USD_MEXCFD_WITHDRAW_HISTORY.png"
            }

            if currency not in currency_template_map:
                await callback.message.answer(f"❌ Валюта {currency} не підтримується для MEXC FD")
                await state.clear()
                return

            template_path = currency_template_map[currency]

            result_path = render_mexc_fd(
                currency=data["currency"],
                lead_bank=data["lead_bank"],
                acter_bank=data["acter_bank"],
                lead_time=data["lead_time"],
                acter_time=data["acter_time"],
                fee_1=data["fee_1"],
                fee_2=data["fee_2"],
                fee_3=data["fee_3"],
                fee_4=data["fee_4"],
                lead_address=data["lead_address"],
                acter_address=data["acter_address"],
                template_path=template_path,
                output_path=output_path
            )

            photo = FSInputFile(result_path)
            await callback.message.answer_photo(
                photo,
                caption="✅ Скріншот MEXC FD готовий! (TEST MODE)\n"
                        "10 рядків × 6 колонок заповнено.",
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
        "💱 <b>MEXC FD - Transaction History</b>\n\n"
        "Структура: 10 рядків × 6 колонок\n"
        "Оберіть валюту (заповнить колонку 1, всі 10 рядків):",
        reply_markup=get_currency_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(MEXCFDStates.waiting_currency)


@router.message(MEXCFDStates.waiting_currency)
async def process_currency(message: Message, state: FSMContext):
    """Process currency selection (fills column 1, all 10 rows)."""
    currency = message.text.strip().upper()

    if currency not in ["ARS", "COP", "CLP", "USD"]:
        await message.answer(
            "❌ Невірна валюта. Будь ласка, оберіть: ARS, COP, CLP або USD",
            reply_markup=get_currency_keyboard()
        )
        return

    await state.update_data(currency=currency)
    await message.answer(
        "🏦 Введіть банк ліда (заповнить колонку 2, рядки 1-9)\n"
        "<i>Приклад: Banco Galicia, BBVA, Santander</i>",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )
    await state.set_state(MEXCFDStates.waiting_lead_bank)


@router.message(MEXCFDStates.waiting_lead_bank)
async def process_lead_bank(message: Message, state: FSMContext):
    """Process lead bank name (fills column 2, rows 1-9)."""
    await state.update_data(lead_bank=message.text.strip())
    await message.answer(
        "🏦 Введіть банк актера (заповнить колонку 2, рядок 10)\n"
        "<i>Приклад: Banco Santander</i>",
        parse_mode="HTML"
    )
    await state.set_state(MEXCFDStates.waiting_acter_bank)


@router.message(MEXCFDStates.waiting_acter_bank)
async def process_acter_bank(message: Message, state: FSMContext):
    """Process acter bank name (fills column 2, row 10)."""
    await state.update_data(acter_bank=message.text.strip())
    await message.answer(
        "📅 Введіть час відправки клієнта (заповнить колонку 3, рядки 1-9)\n"
        "<i>Приклад: Hace 2 días, Hace una semana</i>",
        parse_mode="HTML"
    )
    await state.set_state(MEXCFDStates.waiting_lead_time)


@router.message(MEXCFDStates.waiting_lead_time)
async def process_lead_time(message: Message, state: FSMContext):
    """Process lead time (fills column 3, rows 1-9)."""
    await state.update_data(lead_time=message.text.strip())
    await message.answer(
        "📅 Введіть час відправки актера (заповнить колонку 3, рядок 10)\n"
        "<i>Приклад: Hace 1 día</i>",
        parse_mode="HTML"
    )
    await state.set_state(MEXCFDStates.waiting_acter_time)


@router.message(MEXCFDStates.waiting_acter_time)
async def process_acter_time(message: Message, state: FSMContext):
    """Process acter time (fills column 3, row 10)."""
    await state.update_data(acter_time=message.text.strip())
    await message.answer(
        "💰 Введіть суму комісії #1 (заповнить колонку 5, рядки 1, 3, 5)\n"
        "<i>Приклад: 500.00</i>",
        parse_mode="HTML"
    )
    await state.set_state(MEXCFDStates.waiting_fee_1)


@router.message(MEXCFDStates.waiting_fee_1)
async def process_fee_1(message: Message, state: FSMContext):
    """Process fee 1 (fills column 5, rows 1, 3, 5)."""
    await state.update_data(fee_1=message.text.strip())
    await message.answer(
        "💰 Введіть суму комісії #2 (заповнить колонку 5, рядки 2, 8)\n"
        "<i>Приклад: 750.00</i>",
        parse_mode="HTML"
    )
    await state.set_state(MEXCFDStates.waiting_fee_2)


@router.message(MEXCFDStates.waiting_fee_2)
async def process_fee_2(message: Message, state: FSMContext):
    """Process fee 2 (fills column 5, rows 2, 8)."""
    await state.update_data(fee_2=message.text.strip())
    await message.answer(
        "💰 Введіть суму комісії #3 (заповнить колонку 5, рядки 4, 6, 7, 9)\n"
        "<i>Приклад: 1000.00</i>",
        parse_mode="HTML"
    )
    await state.set_state(MEXCFDStates.waiting_fee_3)


@router.message(MEXCFDStates.waiting_fee_3)
async def process_fee_3(message: Message, state: FSMContext):
    """Process fee 3 (fills column 5, rows 4, 6, 7, 9)."""
    await state.update_data(fee_3=message.text.strip())
    await message.answer(
        "💰 Введіть суму комісії #4 (заповнить колонку 5, рядок 10)\n"
        "<i>Приклад: 1250.00</i>",
        parse_mode="HTML"
    )
    await state.set_state(MEXCFDStates.waiting_fee_4)


@router.message(MEXCFDStates.waiting_fee_4)
async def process_fee_4(message: Message, state: FSMContext):
    """Process fee 4 (fills column 5, row 10)."""
    await state.update_data(fee_4=message.text.strip())
    await message.answer(
        "🔢 Введіть адресу виводу ліда (заповнить колонку 6, рядки 1-9)\n"
        "<i>Приклад: 3001382195******</i>",
        parse_mode="HTML"
    )
    await state.set_state(MEXCFDStates.waiting_lead_address)


@router.message(MEXCFDStates.waiting_lead_address)
async def process_lead_address(message: Message, state: FSMContext):
    """Process lead address (fills column 6, rows 1-9)."""
    await state.update_data(lead_address=message.text.strip())
    await message.answer(
        "🔢 Введіть адресу виводу актера (заповнить колонку 6, рядок 10)\n"
        "<i>Приклад: 3001234567******</i>",
        parse_mode="HTML"
    )
    await state.set_state(MEXCFDStates.waiting_acter_address)


@router.message(MEXCFDStates.waiting_acter_address)
async def process_acter_address(message: Message, state: FSMContext):
    """Process acter address and generate final screenshot."""
    await state.update_data(acter_address=message.text.strip())

    # Get all collected data
    data = await state.get_data()

    # Show summary
    await message.answer(
        "📊 <b>Зібрані дані:</b>\n\n"
        f"💱 Валюта: {data['currency']}\n"
        f"🏦 Банк ліда: {data['lead_bank']}\n"
        f"🏦 Банк актера: {data['acter_bank']}\n"
        f"📅 Час ліда: {data['lead_time']}\n"
        f"📅 Час актера: {data['acter_time']}\n"
        f"💰 Комісія #1 (рядки 1,3,5): {data['fee_1']}\n"
        f"💰 Комісія #2 (рядки 2,8): {data['fee_2']}\n"
        f"💰 Комісія #3 (рядки 4,6,7,9): {data['fee_3']}\n"
        f"💰 Комісія #4 (рядок 10): {data['fee_4']}\n"
        f"🔢 Адреса ліда: {data['lead_address']}\n"
        f"🔢 Адреса актера: {data['acter_address']}\n\n"
        "⏳ Генерую скріншот...",
        parse_mode="HTML"
    )

    try:
        # Create output directory if it doesn't exist
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(config.OUTPUT_DIR, f"mexc_fd_{message.from_user.id}.png")

        # Map currency to template filename
        currency = data["currency"]
        currency_template_map = {
            "CLP": "templates/mexc_fd/SD_CLP_MEXCFD_WITHDRAW_HISTORY.png",
            "COP": "templates/mexc_fd/SH_COP_MEXCFD_WITHDRAW_HISTORY.png",
            "ARS": "templates/mexc_fd/SR_ARS_MEXCFD_WITHDRAW_HISTORY.png",
            "USD": "templates/mexc_fd/SR_USD_MEXCFD_WITHDRAW_HISTORY.png"
        }

        if currency not in currency_template_map:
            await message.answer(
                f"❌ Валюта {currency} не підтримується для MEXC FD\n"
                f"Доступні валюти: CLP, COP, ARS, USD",
                reply_markup=get_continue_keyboard()
            )
            await state.clear()
            return

        template_path = currency_template_map[currency]

        # Generate screenshot
        result_path = render_mexc_fd(
            currency=data["currency"],
            lead_bank=data["lead_bank"],
            acter_bank=data["acter_bank"],
            lead_time=data["lead_time"],
            acter_time=data["acter_time"],
            fee_1=data["fee_1"],
            fee_2=data["fee_2"],
            fee_3=data["fee_3"],
            fee_4=data["fee_4"],
            lead_address=data["lead_address"],
            acter_address=data["acter_address"],
            template_path=template_path,
            output_path=output_path
        )

        # Send the generated screenshot
        photo = FSInputFile(result_path)
        await message.answer_photo(
            photo,
            caption=(
                "✅ <b>Скріншот MEXC FD успішно створено!</b>\n\n"
                "Структура: 10 рядків × 6 колонок\n"
                "• Колонка 1 (Cripto): валюта для всіх рядків\n"
                "• Колонка 2 (Banco): банк ліда (1-9), банк актера (10)\n"
                "• Колонка 3 (Tiempo): час ліда (1-9), час актера (10)\n"
                "• Колонка 4 (Estado): 'Retiro Exitoso' (1-9), 'Reposición' (10)\n"
                "• Колонка 5 (Monto): комісії розподілені за правилами\n"
                "• Колонка 6 (Dirección): адреса ліда (1-9), адреса актера (10)"
            ),
            reply_markup=get_continue_keyboard(),
            parse_mode="HTML"
        )

        await state.clear()

    except Exception as e:
        await message.answer(
            f"❌ Помилка при створенні скріншоту:\n{str(e)}\n\n"
            "Спробуйте ще раз або зверніться до підтримки.",
            reply_markup=get_continue_keyboard()
        )
        await state.clear()
