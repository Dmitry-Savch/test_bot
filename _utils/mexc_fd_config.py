"""
Configuration constants for MEXC FD table rendering.

All coordinates are for templates at 3840 x 2880 px.
Structure: 10 rows × 5 columns
- Cripto (Currency)
- Banco (Bank)
- Tiempo (Time)
- Estado (Status) - показує "Retiro Exitoso" або "Reposición"
- Monto (Amount/Fee)
- Dirección de Retiro (Withdrawal Address) - останній стовпець
"""

# Font settings
FONT_FAMILY = "fonts/BlinkMacSystemFont-Regular.otf"
FONT_SIZE = 31  # Smaller font for MEXC interface
TEXT_COLOR = (255, 255, 255)  # White text on dark background
STATUS_COLOR = (0, 255, 163)  # Green color for "Retiro Exitoso" (#00FFA3)
REPOSITION_COLOR = (0, 255, 163)  # Green color for "Reposición"
KERNING = 0.8  # Tighter letter spacing

# Template actual size: 3840 x 2880
# Y positions for 10 rows
# Приблизні координати, потребують точного налаштування
Y_POSITIONS = [
    828,    # Row 1
    1023,    # Row 2
    1217,    # Row 3
    1409,    # Row 4
    1604,    # Row 5
    1794,   # Row 6
    1992,   # Row 7
    2187,   # Row 8
    2381,   # Row 9
    2575,   # Row 10
]

# X positions for 5 columns (left alignment)
CRIPTO_X = 695       # "Cripto" (Currency) column - left
BANCO_X = 996        # "Banco" (Bank) column - left
TIEMPO_X = 1305       # "Tiempo" (Time) column - left
MONTO_X = 2480        # "Monto" (Amount/Fee) column - left
DIRECCION_X = 2800   # "Dirección de Retiro" (Address) column - left

# Note: Row 10 typically has "Reposición" status and different data sources
