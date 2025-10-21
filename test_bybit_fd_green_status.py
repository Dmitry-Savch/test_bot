"""
Test script for Bybit FD with green status text
"""
from _modifiers_photo.bybit_fd import render_bybit_fd_successful

# Test data
result = render_bybit_fd_successful(
    currency="MXN",
    bank="BBVA",
    time_in_description="Hace un año",
    status="Pagado",
    lead_payment_amount="$3,000.00",
    acter_payment_1="$1,500.00",
    acter_payment_2="$2,000.00",
    lead_account_number="1234",
    acter_account_1="5678",
    acter_account_2="9012",
    template_path="templates/bybit_fd/successful.png",
    output_path="output/test_bybit_fd_green_status.png"
)

print(f"Test screenshot generated: {result}")
print("Status text should be displayed in green color")
