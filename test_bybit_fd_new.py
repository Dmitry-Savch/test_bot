"""
Test script for updated Bybit FD (Successful) renderer
Structure: 11 rows × 6 columns
"""
from _modifiers_photo.bybit_fd import render_bybit_fd_successful

# Test data based on your structure
test_data = {
    "currency": "MXN",  # Column 1: all 11 rows
    "bank": "BVVA",  # Column 2: all 11 rows
    "time_in_description": "Hace un año",  # Column 3: all 11 rows
    "status": "Pagado",  # Column 4: all 11 rows
    "lead_payment_amount": "489.000",  # Column 5: rows 1-9
    "acter_payment_1": "29.320.120",  # Column 5: row 10
    "acter_payment_2": "29.320.120",  # Column 5: row 11
    "lead_account_number": "3001382195",  # Column 6: rows 1-9 (will add ******)
    "acter_account_1": "8805356635",  # Column 6: row 10 (will add *****) - same as row 11
    "acter_account_2": "8805356635",  # Column 6: row 11 (will add *****) - same as row 10
    "template_path": "templates/successful.png",
    "output_path": "output/test_bybit_fd_new.png"
}

if __name__ == "__main__":
    print("Testing updated Bybit FD renderer with 11 rows × 6 columns...")
    try:
        result_path = render_bybit_fd_successful(**test_data)
        print(f"✅ Success! Screenshot saved to: {result_path}")
        print("\nData structure:")
        print(f"- Currency (column 1, all 11 rows): {test_data['currency']}")
        print(f"- Bank (column 2, all 11 rows): {test_data['bank']}")
        print(f"- Time (column 3, all 11 rows): {test_data['time_in_description']}")
        print(f"- Status (column 4, all 11 rows): {test_data['status']}")
        print(f"- Lead payment (column 5, rows 1-9): {test_data['lead_payment_amount']}")
        print(f"- Acter payment 1 (column 5, row 10): {test_data['acter_payment_1']}")
        print(f"- Acter payment 2 (column 5, row 11): {test_data['acter_payment_2']}")
        print(f"- Lead account (column 6, rows 1-9): {test_data['lead_account_number']}******")
        print(f"- Acter account 1 (column 6, row 10): {test_data['acter_account_1']}*****")
        print(f"- Acter account 2 (column 6, row 11): {test_data['acter_account_2']}*****")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
