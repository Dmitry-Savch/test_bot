"""
Analyze the reference screenshot with colored frames to understand table structure
"""
from PIL import Image

# Load the reference screenshot with frames
ref_path = "/var/folders/w6/d2qw7g4x7bqd_h483v7f6s_h0000gn/T/TemporaryItems/NSIRD_screencaptureui_4g4gjt/Знімок екрана 2025-10-16 о 15.46.54.png"

try:
    img = Image.open(ref_path)
    print(f"Reference image size: {img.size}")
    print(f"Width: {img.width}, Height: {img.height}")

    # Based on the visual analysis from the reference screenshot:
    # The table appears to be in the center of the screen
    # Purple column (left) - amounts
    # Blue column (right) - account numbers
    # Below the table - two rows with additional info

    print("\nBased on visual inspection of the reference image:")
    print("The data is shown in a vertical layout with:")
    print("- Left column: Transaction amounts")
    print("- Right column: Account numbers")
    print("- Bottom section: Two payment fields and two account number fields")

except Exception as e:
    print(f"Error loading reference: {e}")
    print("\nUsing template dimensions instead...")
    template = Image.open("templates/successful.png")
    print(f"Template size: {template.size}")
