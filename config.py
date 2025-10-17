import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN", "your_token_here")
TEMPLATE_PATH = "templates/sat_form.png"
OUTPUT_DIR = "output"
FONTS_DIR = "fonts"

# Test mode for auto-filling form data during coordinate testing
# Set TEST_MODE=true in environment or uncomment the line below
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"
# TEST_MODE = True  # Uncomment to enable test mode without environment variable

# Test data for Bybit Withdraw
BYBIT_TEST_DATA = {
    "currency": "MXN",
    "time_in_description": "Hace un mes",
    "lead_bank": "BVVA",
    "lead_number": "1999659",
    "persa_number": "1509208",
    "transaction_lead_10": "488.323",
    "transaction_lead_main": "241.579",
    "transaction_lead_11": "620.000",
    "total_payout": "4.911.820"
}

# Test data for Bybit FD (Successful)
BYBIT_FD_TEST_DATA = {
    "currency": "MXN",
    "bank": "BVVA",
    "time_in_description": "Hace un año",
    "status": "Pagado",
    "lead_payment_amount": "500.00",
    "acter_payment_1": "250.00",
    "acter_payment_2": "250.00",
    "lead_account_number": "1999659",
    "acter_account_1": "1509208",
    "acter_account_2": "1509208"
}
