"""
Test script to verify that output filenames match template names
"""
from _modifiers_photo.bybit_withdraw import render_bybit_withdraw_history

# Test data
test_templates = [
    "templates/bybit/SD_MXN_BLACK_BYBIT_WITHDRAW_HISTORY.png",
    "templates/bybit/DU_ARS_BLACK_BYBIT_WITHDRAW_HISTORY.png",
    "templates/bybit/SH_USD_BLACK_BYBIT_WITHDRAW_HISTORY.png",
    "templates/bybit/DU_CLP_BLACK_BYBIT_WITHDRAW_HISTORY.png",
]

expected_outputs = [
    "output/SD_MXN_BLACK_BYBIT_WITHDRAW_HISTORY_RESULT.png",
    "output/DU_ARS_BLACK_BYBIT_WITHDRAW_HISTORY_RESULT.png",
    "output/SH_USD_BLACK_BYBIT_WITHDRAW_HISTORY_RESULT.png",
    "output/DU_CLP_BLACK_BYBIT_WITHDRAW_HISTORY_RESULT.png",
]

currencies = [" MXN", " ARS", " $", " CLP"]

print("Testing output filename generation:\n")

for template, expected, currency in zip(test_templates, expected_outputs, currencies):
    try:
        result = render_bybit_withdraw_history(
            transaction_lead_10="1,000.00",
            transaction_lead_main="2,000.00",
            transaction_lead_11="500.00",
            total_payout="3,500.00",
            lead_bank="Test Bank",
            lead_number="1234",
            persa_number="5678",
            time_in_description="Hace un mes",
            currency=currency,
            template_path=template
        )

        status = "✅" if result == expected else "❌"
        print(f"{status} Template: {template}")
        print(f"   Expected: {expected}")
        print(f"   Got:      {result}")
        print()

    except FileNotFoundError:
        print(f"⚠️  Template not found: {template}")
        print(f"   Would generate: {expected}")
        print()
