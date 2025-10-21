"""
Test script for MEXC FD screenshot generation
"""
from _modifiers_photo.mexc_fd import render_mexc_fd

# Test data
result = render_mexc_fd(
    currency="ARS",
    lead_bank="Banco Galicia",
    acter_bank="Banco Santander",
    lead_time="Hace 2 días",
    acter_time="Hace 1 día",
    fee_1="500.00",      # Rows 1, 3, 5
    fee_2="750.00",      # Rows 2, 8
    fee_3="1000.00",     # Rows 4, 6, 7, 9
    fee_4="1250.00",     # Row 10
    lead_address="3001382195******",
    acter_address="3001234567******",
    template_path="templates/mexc_fd/SR_ARS_MEXCFD_WITHDRAW_HISTORY.png",
    output_path="output/test_mexc_fd.png"
)

print(f"Test screenshot generated: {result}")
print("Fee distribution:")
print("  - fee_1 (500.00): rows 1, 3, 5")
print("  - fee_2 (750.00): rows 2, 8")
print("  - fee_3 (1000.00): rows 4, 6, 7, 9")
print("  - fee_4 (1250.00): row 10")
