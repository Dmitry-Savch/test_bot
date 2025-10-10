from aiogram.fsm.state import State, StatesGroup


class BybitWithdrawStates(StatesGroup):
    """States for Bybit withdrawal history screenshot generation."""
    waiting_currency = State()
    waiting_time = State()
    waiting_bank = State()
    waiting_lead_number = State()
    waiting_persa_number = State()
    waiting_transaction_lead_10 = State()
    waiting_transaction_lead_main = State()
    waiting_transaction_lead_11 = State()
    waiting_total_payout = State()
