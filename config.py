import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN", "your_token_here")
TEMPLATE_PATH = "templates/sat_form.png"
OUTPUT_DIR = "output"
FONTS_DIR = "fonts"

# Actor names mapping by currency and platform
# Format: "{CURRENCY}_{PLATFORM}_BOTS": "Actor Name"
ACTOR_NAMES = {
    # Standard Bybit (Black theme)
    "ECU_BYBIT_BOTS": "Sebastian Hernandez",
    "ARS_BYBIT_BOTS": "Diego Ugarte",
    "MXN_BYBIT_BOTS": "Santiago Diaz",
    "CLP_BYBIT_BOTS": "Sebastian Hernandez",
    "VED_BYBIT_BOTS": "Sebastian Hernandez",
    "COP_BYBIT_BOTS": "Sebastian Ramos",

    # MEXC
    "COP_MEXC_BOTS": "Santiago Sánchez",
    "MXN_MEXC_BOTS": "Sebastian Martines",
    "ARS_MEXC_BOTS": "Héctor Lopez",
    "ECU_MEXC_BOTS": "Santiago Ramos",
    "CLP_MEXC_BOTS": "Santiago Diaz",
    "VED_MEXC_BOTS": "Santiago Ramos",
    "SOL_MEXC_BOTS": "Santiago Diaz",

    # Bybit FD (White theme)
    "ECU_WHITE_BYBIT_BOTS": "Diego Martines",
    "ARS_WHITE_BYBIT_BOTS": "Santiago Hernandez",
    "MXN_WHITE_BYBIT_BOTS": "Diego Hernandez",
    "COP_WHITE_BYBIT_BOTS": "Diego Martines",
}


def get_actor_name(currency: str, platform: str) -> str:
    """
    Get actor name based on currency and platform.

    Args:
        currency: Currency code (e.g., "MXN", "ARS", "CLP")
        platform: Platform identifier (e.g., "BYBIT_BOTS", "MEXC_BOTS", "WHITE_BYBIT_BOTS")

    Returns:
        Actor name or "Unknown Actor" if not found

    Examples:
        >>> get_actor_name("MXN", "BYBIT_BOTS")
        'Santiago Diaz'
        >>> get_actor_name("ARS", "MEXC_BOTS")
        'Héctor Lopez'
    """
    key = f"{currency}_{platform}"
    return ACTOR_NAMES.get(key, "Unknown Actor")


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

# Test data for MEXC FD
# Supported currencies: CLP, COP, ARS, USD
MEXC_FD_TEST_DATA = {
    "currency": "ARS",  # Available: CLP, COP, ARS, USD
    "lead_bank": "Banco Galicia",
    "acter_bank": "Banco Santander",
    "lead_time": "Hace 2 días",
    "acter_time": "Hace 1 día",
    "fee_1": "500.00",      # Rows 1, 3, 5
    "fee_2": "750.00",      # Rows 2, 8
    "fee_3": "1000.00",     # Rows 4, 6, 7, 9
    "fee_4": "1250.00",     # Row 10
    "lead_address": "3001382195******",
    "acter_address": "3001234567******"
}
