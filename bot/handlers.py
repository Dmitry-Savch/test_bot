import os
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from bot.keyboards import get_input_mode_keyboard, get_main_menu_keyboard
from bot.states import FormStates
from modifiers.sat_form_modifier import render_sat_form
import config

router = Router()
user_preferences = {}


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Вітаю! Оберіть режим введення даних:",
        reply_markup=get_input_mode_keyboard()
    )
    await state.set_state(FormStates.choosing_input_mode)


@router.callback_query(F.data == "mode_single", FormStates.choosing_input_mode)
async def process_mode_single(callback: CallbackQuery, state: FSMContext):
    user_preferences[callback.from_user.id] = {"input_mode": "single"}
    await callback.answer()
    await callback.message.answer(
        "Надішліть дані у форматі:\n"
        "Beneficiario | NumCuenta | Importe | Valor\n\n"
        "Приклад: Juan Perez | 1234567890 | 150.50 | 150.50"
    )
    await state.set_state(FormStates.waiting_all_params)


@router.callback_query(F.data == "mode_chain", FormStates.choosing_input_mode)
async def process_mode_chain(callback: CallbackQuery, state: FSMContext):
    user_preferences[callback.from_user.id] = {"input_mode": "chain"}
    await callback.answer()
    await callback.message.answer("Введіть NOMBRE DEL BENEFICIARIO:")
    await state.set_state(FormStates.waiting_beneficiario)


@router.callback_query(F.data == "create_screenshot")
async def process_create_screenshot(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    user_mode = user_preferences.get(callback.from_user.id, {}).get("input_mode")

    if user_mode == "single":
        await callback.message.answer(
            "Надішліть дані у форматі:\n"
            "Beneficiario | NumCuenta | Importe | Valor\n\n"
            "Приклад: Juan Perez | 1234567890 | 150.50 | 150.50"
        )
        await state.set_state(FormStates.waiting_all_params)
    elif user_mode == "chain":
        await callback.message.answer("Введіть NOMBRE DEL BENEFICIARIO:")
        await state.set_state(FormStates.waiting_beneficiario)
    else:
        await callback.message.answer(
            "Оберіть режим введення даних:",
            reply_markup=get_input_mode_keyboard()
        )
        await state.set_state(FormStates.choosing_input_mode)


@router.message(FormStates.waiting_all_params)
async def process_all_params(message: Message, state: FSMContext):
    try:
        parts = [p.strip() for p in message.text.split("|")]
        if len(parts) != 4:
            await message.answer(
                "Помилка формату! Потрібно 4 параметри через '|'.\n"
                "Приклад: Juan Perez | 1234567890 | 150.50 | 150.50"
            )
            return

        beneficiario, numero, importe, valor = parts

        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(config.OUTPUT_DIR, f"sat_{message.from_user.id}.png")

        result_path = render_sat_form(
            beneficiario=beneficiario,
            numero_cuenta=numero,
            importe=importe,
            valor_enviado=valor,
            template_path=config.TEMPLATE_PATH,
            output_path=output_path
        )

        photo = FSInputFile(result_path)
        await message.answer_photo(
            photo,
            caption="Скріншот SAT форми готовий!",
            reply_markup=get_main_menu_keyboard()
        )

        await state.clear()

    except Exception as e:
        await message.answer(f"Помилка при створенні скріншоту: {str(e)}")


@router.message(FormStates.waiting_beneficiario)
async def process_beneficiario(message: Message, state: FSMContext):
    await state.update_data(beneficiario=message.text)
    await message.answer("Введіть NUMERO DE CUENTA:")
    await state.set_state(FormStates.waiting_numero)


@router.message(FormStates.waiting_numero)
async def process_numero(message: Message, state: FSMContext):
    await state.update_data(numero=message.text)
    await message.answer("Введіть IMPORTE DEL IMPUESTO:")
    await state.set_state(FormStates.waiting_importe)


@router.message(FormStates.waiting_importe)
async def process_importe(message: Message, state: FSMContext):
    await state.update_data(importe=message.text)
    await message.answer("Введіть VALOR ENVIADO:")
    await state.set_state(FormStates.waiting_valor)


@router.message(FormStates.waiting_valor)
async def process_valor(message: Message, state: FSMContext):
    await state.update_data(valor=message.text)

    try:
        data = await state.get_data()

        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(config.OUTPUT_DIR, f"sat_{message.from_user.id}.png")

        result_path = render_sat_form(
            beneficiario=data["beneficiario"],
            numero_cuenta=data["numero"],
            importe=data["importe"],
            valor_enviado=data["valor"],
            template_path=config.TEMPLATE_PATH,
            output_path=output_path
        )

        photo = FSInputFile(result_path)
        await message.answer_photo(
            photo,
            caption="Скріншот SAT форми готовий!",
            reply_markup=get_main_menu_keyboard()
        )

        await state.clear()

    except Exception as e:
        await message.answer(f"Помилка при створенні скріншоту: {str(e)}")
