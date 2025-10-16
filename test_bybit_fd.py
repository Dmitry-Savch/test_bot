"""
Test script for Bybit FD (Successful) renderer
"""
from _modifiers_photo.bybit_fd import render_bybit_fd_successful

# Test data based on the screenshot
test_data = {
    "currency": " CLP",
    "time_in_description": "Hace un año",
    "status": "Pagado",
    "bank": "Banco Estado",
    "transaction_1": "489.000",
    "transaction_2": "1.200.000",
    "transaction_3": "489.000",
    "transaction_4": "5.210.530",
    "transaction_5": "489.000",
    "transaction_6": "5.210.530",
    "transaction_7": "1.200.000",
    "transaction_8": "5.210.530",
    "transaction_9": "1.150.000",
    "lead_account_number": "3001382195",
    "ater_payment": "29.320.120",
    "lead_payment": "29.320.120",
    "lead_account_full": "88053566635",
    "acter_account_full": "88053566635",
    "template_path": "templates/successful.png",
    "output_path": "output/test_bybit_fd.png"
}

if __name__ == "__main__":
    print("Testing Bybit FD renderer...")
    try:
        result_path = render_bybit_fd_successful(**test_data)
        print(f"✅ Success! Screenshot saved to: {result_path}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
