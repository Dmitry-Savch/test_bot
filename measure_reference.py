#!/usr/bin/env python3
"""
Measure coordinates from the reference screenshot to get accurate positioning.
The reference image shows the correct layout at full resolution.
"""
from PIL import Image

# Open reference (the good example)
ref = Image.open("/Users/dmitrosavcuk/Downloads/[ByBit] Macbook (1).png")
print(f"Reference image size: {ref.width} x {ref.height}")

# The reference is at FULL size (6720 x 4200)
# After 70% resize: 4704 x 2940

# Based on visual inspection of the reference screenshot:
# - Table header "Tiempo" is around y=1050
# - First data row appears around y=1330
# - Row spacing is approximately 330-340 pixels

print("\n=== MEASUREMENTS FROM REFERENCE IMAGE ===")
print("(These are approximate, measured visually)")

# Estimated Y positions for full-size template
header_y = 1050
first_row_y = 1330
row_spacing = 340

print(f"\nTable header Y: ~{header_y}")
print(f"First row Y: ~{first_row_y}")
print(f"Row spacing: ~{row_spacing}")

print("\n=== CALCULATED Y POSITIONS (for 70% resize) ===")
# Calculate for 70% size
scale = 0.7
for i in range(6):
    y = int((first_row_y + (i * row_spacing)) * scale)
    print(f"Row {i+1}: y = {y}")

print("\n=== COLUMN X POSITIONS ===")
# Estimated X positions from reference (full size)
time_x = 1000
account_x = 2320
bank_x = 3820
amount_x = 5500

print(f"Tiempo (time): ~{time_x} → {int(time_x * scale)} (70%)")
print(f"Numero de cuenta: ~{account_x} → {int(account_x * scale)} (70%)")
print(f"Banco: ~{bank_x} → {int(bank_x * scale)} (70%)")
print(f"Monto (amount, right): ~{amount_x} → {int(amount_x * scale)} (70%)")

print("\n=== FONT SIZE ESTIMATE ===")
# Reference shows text that's roughly 100-120px tall at full size
estimated_font_full = 110
print(f"Estimated font at full size: ~{estimated_font_full}px")
print(f"After 70% resize: ~{int(estimated_font_full * scale)}px")
