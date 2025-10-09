#!/usr/bin/env python3
"""Debug script to analyze image dimensions and coordinate calculations"""
import sys
from pathlib import Path

try:
    from PIL import Image

    print("=== TEMPLATE IMAGE ANALYSIS ===\n")

    # Check template
    template_path = "templates/bybit_mxn_withdraw_history.png"
    if Path(template_path).exists():
        template = Image.open(template_path)
        print(f"Original template size: {template.width} x {template.height}")
        print(f"After 70% resize: {int(template.width * 0.7)} x {int(template.height * 0.7)}")
    else:
        print(f"❌ Template not found: {template_path}")

    print("\n=== REFERENCE IMAGE ANALYSIS ===\n")

    # Check reference (good example)
    ref_path = "/Users/dmitrosavcuk/Downloads/[ByBit] Macbook (1).png"
    if Path(ref_path).exists():
        ref = Image.open(ref_path)
        print(f"Reference (good) size: {ref.width} x {ref.height}")
    else:
        print(f"⚠️  Reference not found: {ref_path}")

    print("\n=== CURRENT OUTPUT ANALYSIS ===\n")

    # Check current output
    output_path = "output/bybit_788632197.png"
    if Path(output_path).exists():
        output = Image.open(output_path)
        print(f"Current output size: {output.width} x {output.height}")
    else:
        print(f"⚠️  Output not found: {output_path}")

    print("\n=== COORDINATE CALCULATIONS ===\n")

    # Current config values
    print("Current config in table_renderer.py:")
    print("  font_size: 24")
    print("  y_positions: [197, 236, 275, 314, 353, 392]")
    print("  columns:")
    print("    time: x=120")
    print("    account: x=277")
    print("    bank: x=400")
    print("    amount: x=645 (right aligned)")

    print("\n=== RECOMMENDATIONS ===\n")

    if Path(template_path).exists() and Path(ref_path).exists():
        template = Image.open(template_path)
        ref = Image.open(ref_path)

        # Calculate what the coordinates SHOULD be based on reference
        scale = ref.width / template.width
        print(f"Scale factor from template to reference: {scale:.3f}")

        if abs(scale - 0.7) < 0.05:
            print("✓ Reference matches expected 70% scale")
        else:
            print(f"⚠️  Scale mismatch! Expected ~0.7, got {scale:.3f}")
            print(f"   Consider using scale factor: {scale:.3f}")

            # Suggest new coordinates
            print("\n   Suggested coordinates for actual scale:")
            original_coords = [340, 410, 480, 550, 620, 690]
            for i, y in enumerate(original_coords):
                scaled_y = int(y * scale)
                print(f"     Row {i+1}: y = {scaled_y}")

except ImportError:
    print("❌ PIL/Pillow not installed")
    print("Install with: python3 -m pip install --user --break-system-packages Pillow")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
