"""
Configuration constants for Bybit withdrawal history table rendering.

All coordinates are for templates at 3360 x 2100 px.
"""

# Font settings
FONT_FAMILY = "fonts/OpenSans-Semibold.ttf"
FONT_SIZE = 55
TEXT_COLOR = (255, 255, 255)  # White
KERNING = 1.4

# Y positions for 6 rows (vertical positioning)
Y_POSITIONS = [788, 948, 1108, 1268, 1428, 1588]

# X positions for columns (horizontal positioning)
TIEMPO_X = 414         # "Tiempo" column (left aligned)
NUMERO_CUENTA_X = 940   # "Numero de cuenta" column (left aligned)
BANCO_X = 1620          # "Banco" column (left aligned)
MONTO_X = 2270     # "Monto" column (right aligned)
