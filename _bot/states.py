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


class MEXCFDStates(StatesGroup):
    """States for MEXC FD screenshot generation with 10 rows × 6 columns."""
    waiting_currency = State()          # Column 1: same for all 10 rows
    waiting_lead_bank = State()         # Column 2: rows 1-9
    waiting_acter_bank = State()        # Column 2: row 10
    waiting_lead_time = State()         # Column 3: rows 1-9
    waiting_acter_time = State()        # Column 3: row 10
    waiting_fee_1 = State()             # Column 5: rows 1, 3, 5
    waiting_fee_2 = State()             # Column 5: rows 2, 8
    waiting_fee_3 = State()             # Column 5: rows 4, 6, 7, 9
    waiting_fee_4 = State()             # Column 5: row 10
    waiting_lead_address = State()      # Column 6: rows 1-9
    waiting_acter_address = State()     # Column 6: row 10
