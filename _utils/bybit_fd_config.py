"""
Configuration constants for Bybit FD (Successful) table rendering.

All coordinates are for templates at 3840 x 2712 px.
This is for the "successful.png" template.
"""

# Font settings
FONT_FAMILY = "fonts/OpenSans-Semibold.ttf"
FONT_SIZE = 37  # Reduced font size for better fit
TEXT_COLOR = (0, 0, 0)  # Black text
STATUS_COLOR = (11, 185, 115)  # Green color for status column (#0BB973)
KERNING = 0.8  # Tighter letter spacing

# Template actual size: 3840 x 2712
# Scale factor from 3360x2100: 3840/3360 = 1.143 (width), 2712/2100 = 1.291 (height)

# Base coordinates from existing bybit template (3360x2100):
# Y_POSITIONS = [788, 948, 1108, 1268, 1428, 1588]
# TIEMPO_X = 414, NUMERO_CUENTA_X = 940, BANCO_X = 1555, MONTO_X = 2200

# Y positions for 11 rows total
# Підняті на 500 пікселів вгору (зменшуємо всі Y на 500)
Y_POSITIONS = [
    640,   # Row 1
    835,   # Row 2
    1030,   # Row 3
    1225,   # Row 4
    1420,   # Row 5
    1615,   # Row 6
    1810,  # Row 7
    2005,  # Row 8
    2220,  # Row 9
    2395,  # Row 10 - first actor row
    2590,  # Row 11 - second actor row
]

# X positions for 6 columns (центри колонок для center alignment)
MONEDA_X = 555                   # "Moneda" (Currency) column - center
BANCO_X = 860                     # "Banco" (Bank) column - center
TIEMPO_X = 1225                    # "Tiempo" (Time) column - center
ESTADO_X = 1625                    # "Estado" (Status) column - center
MONTO_X = 2370                     # "Monto" (Amount) column - center
# "Numero de cuenta" (Account) column - center
NUMERO_CUENTA_X = 2750

# Note: Rows 10 and 11 (Y_POSITIONS[9] and Y_POSITIONS[10]) are used for bottom data
# They use the same columns as rows 1-9, just with different data sources
