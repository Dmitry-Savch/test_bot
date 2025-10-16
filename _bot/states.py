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


class BybitFDStates(StatesGroup):
    """States for Bybit FD (Successful) screenshot generation with 11 rows × 6 columns."""
    waiting_currency = State()              # Column 1: same for all 11 rows
    waiting_bank = State()                  # Column 2: same for all 11 rows
    waiting_time = State()                  # Column 3: same for all 11 rows
    waiting_status = State()                # Column 4: same for all 11 rows
    waiting_lead_payment_amount = State()   # Column 5: rows 1-9
    waiting_acter_payment_1 = State()       # Column 5: rows 10-11 (same value)
    waiting_lead_account_number = State()   # Column 6: rows 1-9
    waiting_acter_account = State()         # Column 6: rows 10-11 (same value)
