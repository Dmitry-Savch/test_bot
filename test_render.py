"""Quick test script to verify table rendering"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from _modifiers_photo.bybit_withdraw_mxn import render_bybit_mxn_withdraw_history

def main():
    template_path = "templates/bybit_mxn_withdraw_history.png"
    output_path = "output/test_render_result.png"

    if not os.path.exists(template_path):
        print(f"❌ Template not found: {template_path}")
        return

    print("🔄 Rendering table with test data...")

    result = render_bybit_mxn_withdraw_history(
        transaction_lead_10="15.700",
        transaction_lead_main="10.200",
        transaction_lead_11="20.4500",
        total_payout="323.258",
        lead_bank="BBVA",
        lead_number="121587",
        persa_number="150920",
        time_in_description="Ayer",
        template_path=template_path,
        output_path=output_path
    )

    if os.path.exists(result):
        print(f"✅ Image generated successfully: {result}")
        print(f"📏 Check the output to verify text fits within table cells")
    else:
        print(f"❌ Failed to generate image")

if __name__ == "__main__":
    main()
