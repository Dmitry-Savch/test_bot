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
FONT_FAMILY = "fonts/OpenSans-Semibold.ttf"
FONT_SIZE = 30  # Smaller font for MEXC interface
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

# X positions for 5 columns (center alignment)
CRIPTO_X = 737       # "Cripto" (Currency) column - center
BANCO_X = 1036        # "Banco" (Bank) column - center
TIEMPO_X = 1414       # "Tiempo" (Time) column - center
MONTO_X = 2527        # "Monto" (Amount/Fee) column - center
DIRECCION_X = 2925   # "Dirección de Retiro" (Address) column - center

# Note: Row 10 typically has "Reposición" status and different data sources
