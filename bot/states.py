from aiogram.fsm.state import State, StatesGroup


class FormStates(StatesGroup):
    choosing_input_mode = State()
    waiting_all_params = State()
    waiting_beneficiario = State()
    waiting_numero = State()
    waiting_importe = State()
    waiting_valor = State()
