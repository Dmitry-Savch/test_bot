"""
Configuration constants for Bybit FD (Successful) table rendering.

All coordinates are for templates at 3840 x 2712 px.
This is for the "successful.png" template.
"""

# Font settings
FONT_FAMILY = "fonts/OpenSans-Semibold.ttf"
FONT_SIZE = 38  # Reduced font size for better fit
TEXT_COLOR = (0, 0, 0)  # Black text
KERNING = 0.8  # Tighter letter spacing

# Template actual size: 3840 x 2712
# Scale factor from 3360x2100: 3840/3360 = 1.143 (width), 2712/2100 = 1.291 (height)

# Base coordinates from existing bybit template (3360x2100):
# Y_POSITIONS = [788, 948, 1108, 1268, 1428, 1588]
# TIEMPO_X = 414, NUMERO_CUENTA_X = 940, BANCO_X = 1555, MONTO_X = 2200

# Y positions for 11 rows total
# Підняті на 500 пікселів вгору (зменшуємо всі Y на 500)
Y_POSITIONS = [
    517,   # Row 1 (1017 - 500)
    724,   # Row 2 (1224 - 500)
    931,   # Row 3 (1431 - 500)
    1138,  # Row 4 (1638 - 500)
    1345,  # Row 5 (1845 - 500)
    1552,  # Row 6 (2052 - 500)
    1759,  # Row 7 (2259 - 500)
    1966,  # Row 8 (2466 - 500)
    2173,  # Row 9 (2673 - 500)
    2380,  # Row 10 (2880 - 500) - first bottom row
    2587,  # Row 11 (3087 - 500) - second bottom row
]

# X positions for 6 columns (зсунуті праворуч на 600 пікселів)
MONEDA_X = 680                    # "Moneda" (Currency) column (80 + 600)
BANCO_X = 860                     # "Banco" (Bank) column (260 + 600)
TIEMPO_X = 1080                   # "Tiempo" column (480 + 600)
ESTADO_X = 1350                   # "Estado" column (750 + 600) - колонка 4
MONTO_X = 1800                    # "Monto" column (1000 + 600 + 200) - колонка 5, збільшено відступ на +200
NUMERO_CUENTA_X = 2150            # "Numero de cuenta" column (1350 + 600 + 200) - колонка 6, зсунуто на +200

# Note: Rows 10 and 11 (Y_POSITIONS[9] and Y_POSITIONS[10]) are used for bottom data
# They use the same columns as rows 1-9, just with different data sources
