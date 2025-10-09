"""
Utility to help measure and calculate correct table coordinates.
This script analyzes the template and reference images to determine proper positioning.
"""
from PIL import Image

def analyze_template():
    """Analyze template image dimensions."""
    template = Image.open('templates/bybit_mxn_withdraw_history.png')
    print(f"Template dimensions: {template.width} x {template.height}")

    # Expected reference image (from user's screenshot)
    reference = Image.open('/Users/dmitrosavcuk/Downloads/[ByBit] Macbook (1).png')
    print(f"Reference dimensions: {reference.width} x {reference.height}")

    # Current problematic output
    output = Image.open('output/bybit_788632197.png')
    print(f"Current output dimensions: {output.width} x {output.height}")

    print("\n--- Analysis ---")
    print(f"Template is resized to 70% in the code")
    print(f"Final size should be: {int(template.width * 0.7)} x {int(template.height * 0.7)}")

    # Based on the reference image, let's estimate table coordinates
    # The table header appears to be around y=156 in the reference
    # First row starts around y=197
    # Row height is approximately 39-40 pixels

    print("\n--- Recommended coordinates (for 70% scaled image) ---")
    # These are measured from the reference image
    base_y = 197  # First row baseline
    row_height = 39

    for i in range(6):
        y = base_y + (i * row_height)
        print(f"Row {i+1}: y = {y}")

    print("\n--- Column X positions (for 70% scaled image) ---")
    print("Tiempo: x = 120 (left aligned)")
    print("Numero de cuenta: x = 277 (left aligned)")
    print("Banco: x = 400 (left aligned)")
    print("Monto: x = 645 (right aligned)")

if __name__ == "__main__":
    try:
        analyze_template()
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: Make sure PIL/Pillow is installed: pip install Pillow")
