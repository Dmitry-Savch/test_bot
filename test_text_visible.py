"""
Test script to make text visible on template
"""
from PIL import Image, ImageDraw, ImageFont

# Load template
template = Image.open("templates/successful.png")
draw = ImageDraw.Draw(template)

# Load font
font = ImageFont.truetype("fonts/OpenSans-Semibold.ttf", 55)

# Draw test text in different locations to find the right spot
# Try drawing in multiple colors and positions
test_positions = [
    (100, 500, "TEST 1", (255, 0, 0)),  # Red
    (100, 800, "TEST 2", (0, 255, 0)),  # Green
    (100, 1100, "TEST 3", (0, 0, 255)), # Blue
    (500, 500, "TEST 4", (255, 0, 255)), # Magenta
    (500, 800, "TEST 5", (255, 255, 0)), # Yellow
    (500, 1100, "TEST 6", (0, 255, 255)), # Cyan
    (1000, 500, "TEST 7", (128, 0, 0)), # Dark red
    (1000, 800, "TEST 8", (0, 128, 0)), # Dark green
    (1000, 1100, "TEST 9", (0, 0, 128)), # Dark blue
]

for x, y, text, color in test_positions:
    draw.text((x, y), text, fill=color, font=font)

# Also draw black text
draw.text((100, 1400), "BLACK TEXT", fill=(0, 0, 0), font=font)
# And white text
draw.text((100, 1600), "WHITE TEXT", fill=(255, 255, 255), font=font)

# Save
output_path = "output/text_visibility_test.png"
template.save(output_path)
print(f"Test image saved to: {output_path}")
print("Check which text is visible to determine the correct color")
