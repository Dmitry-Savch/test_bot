"""
Configuration constants for Bybit withdrawal history table rendering.

All coordinates are for templates at 3360 x 2100 px.
"""

# Font settings
FONT_FAMILY = "fonts/BlinkMacSystemFont-Regular.otf"
FONT_SIZE = 53
TEXT_COLOR = (255, 255, 255)  # White
KERNING = 1.4

# Y positions for 6 rows (vertical positioning)
Y_POSITIONS = [
    848, 
    1013, 
    1177, 
    1341, 
    1505, 
    1669
]

# X positions for columns (horizontal positioning)
TIEMPO_X = 414         # "Tiempo" column (left aligned)
NUMERO_CUENTA_X = 1160   # "Numero de cuenta" column (center aligned)
BANCO_X = 1680        # "Banco" column (center aligned)
MONTO_X = 2200     # "Monto" column (center aligned)
