"""
Script to measure and test coordinates for Bybit FD template
This will help identify the correct positions for text placement
"""
from PIL import Image, ImageDraw, ImageFont

# Load the template
template_path = "templates/successful.png"
img = Image.open(template_path)

print(f"Template size: {img.size}")
print(f"Width: {img.width}, Height: {img.height}")

# Create a test image with markers
draw = ImageDraw.Draw(img)

# Try to load font
try:
    font = ImageFont.truetype("fonts/OpenSans-Semibold.ttf", 40)
except:
    font = ImageFont.load_default()

# Draw test markers at different positions to find the table
# Test horizontal positions
test_x_positions = [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200]
# Test vertical positions (looking for table rows)
test_y_positions = [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200]

# Draw vertical lines to show X positions
for x in test_x_positions:
    draw.line([(x, 0), (x, img.height)], fill=(255, 0, 0, 128), width=2)
    draw.text((x, 50), f"X:{x}", fill=(255, 0, 0), font=font)

# Draw horizontal lines to show Y positions
for y in test_y_positions:
    draw.line([(0, y), (img.width, y)], fill=(0, 255, 0, 128), width=2)
    draw.text((50, y), f"Y:{y}", fill=(0, 255, 0), font=font)

# Save the test image
output_path = "output/coordinate_test.png"
img.save(output_path)
print(f"Test image saved to: {output_path}")
print("\nPlease check the image to identify where the table should be located.")
