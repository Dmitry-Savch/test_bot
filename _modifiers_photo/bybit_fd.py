"""
Bybit FD (Successful) Screenshot Generator

Generates successful transaction screenshots for Bybit FD.
Uses the "successful.png" template with 11 transaction rows plus additional bottom fields.
"""
from PIL import Image, ImageDraw, ImageFont
from _utils.bybit_fd_config import (
    FONT_FAMILY, FONT_SIZE, TEXT_COLOR, KERNING,
    Y_POSITIONS, MONEDA_X, BANCO_X, TIEMPO_X, ESTADO_X, MONTO_X, NUMERO_CUENTA_X
)


def draw_text_with_kerning(draw, position, text, font, fill, kerning=1.0):
    """
    Draw text with custom kerning (letter spacing).

    Args:
        draw: PIL ImageDraw object
        position: (x, y) tuple for text position
        text: Text to draw
        font: PIL ImageFont object
        fill: Text color
        kerning: Multiplier for letter spacing (1.0 = normal, >1.0 = wider spacing)
    """
    x, y = position
    for char in text:
        draw.text((x, y), char, font=font, fill=fill)
        char_width = draw.textbbox((0, 0), char, font=font)[2]
        x += char_width * kerning


def render_bybit_fd_successful(
    currency: str,
    bank: str,
    time_in_description: str,
    status: str,
    lead_payment_amount: str,
    acter_payment_1: str,
    acter_payment_2: str,
    lead_account_number: str,
    acter_account_1: str,
    acter_account_2: str,
    template_path: str = "templates/successful.png",
    output_path: str = "output/bybit_fd_result.png"
) -> str:
    """
    Render Bybit FD successful transaction screenshot with 11 rows and 6 columns.

    Table structure (11 rows × 6 columns):
    - Column 1 (MONEDA): Currency - same value for all 11 rows
    - Column 2 (BANCO): Bank - same value for all 11 rows
    - Column 3 (TIEMPO): Time - same value for all 11 rows
    - Column 4 (ESTADO): Status - same value for all 11 rows
    - Column 5 (MONTO): Amount - rows 1-9 use lead_payment_amount, rows 10-11 use acter payments
    - Column 6 (NUMERO): Account - rows 1-9 use lead_account_number, rows 10-11 use acter accounts

    Args:
        currency: Currency (e.g., "MXN", "CLP") - fills column 1, all 11 rows
        bank: Bank name (e.g., "BVVA") - fills column 2, all 11 rows
        time_in_description: Time (e.g., "Hace un año") - fills column 3, all 11 rows
        status: Status (e.g., "Pagado") - fills column 4, all 11 rows
        lead_payment_amount: Payment amount for lead - fills column 5, rows 1-9
        acter_payment_1: First acter payment - fills column 5, row 10
        acter_payment_2: Second acter payment - fills column 5, row 11
        lead_account_number: Lead account number (without ****) - fills column 6, rows 1-9
        acter_account_1: First acter account (without ****) - fills column 6, row 10
        acter_account_2: Second acter account (without ****) - fills column 6, row 11
        template_path: Path to template image
        output_path: Path to save result

    Returns:
        Path to the generated screenshot
    """
    # Load template
    base_img = Image.open(template_path).convert("RGBA")
    draw = ImageDraw.Draw(base_img)

    # Load font
    font = ImageFont.truetype(FONT_FAMILY, FONT_SIZE)

    # Add **** to account numbers
    lead_account_masked = lead_account_number + "******"
    acter_account_1_masked = acter_account_1 + "*****"
    acter_account_2_masked = acter_account_2 + "*****"

    # Render all 11 rows (6 columns each)
    for row_index in range(11):
        y_pos = Y_POSITIONS[row_index]

        # Column 1: MONEDA (Currency) - same for all rows
        draw_text_with_kerning(
            draw, (MONEDA_X, y_pos), currency,
            font, TEXT_COLOR, KERNING
        )

        # Column 2: BANCO (Bank) - same for all rows
        draw_text_with_kerning(
            draw, (BANCO_X, y_pos), bank,
            font, TEXT_COLOR, KERNING
        )

        # Column 3: TIEMPO (Time) - same for all rows
        draw_text_with_kerning(
            draw, (TIEMPO_X, y_pos), time_in_description,
            font, TEXT_COLOR, KERNING
        )

        # Column 4: ESTADO (Status) - same for all rows
        draw_text_with_kerning(
            draw, (ESTADO_X, y_pos), status,
            font, TEXT_COLOR, KERNING
        )

        # Column 5: MONTO (Amount)
        # Rows 1-9 (index 0-8): lead payment amount
        # Row 10 (index 9): acter payment 1
        # Row 11 (index 10): acter payment 2
        if row_index < 9:
            amount_text = lead_payment_amount
        elif row_index == 9:
            amount_text = acter_payment_1
        else:  # row_index == 10
            amount_text = acter_payment_2

        draw_text_with_kerning(
            draw, (MONTO_X, y_pos), amount_text,
            font, TEXT_COLOR, KERNING
        )

        # Column 6: NUMERO DE CUENTA (Account Number)
        # Rows 1-9 (index 0-8): lead account number
        # Row 10 (index 9): acter account 1
        # Row 11 (index 10): acter account 2
        if row_index < 9:
            account_text = lead_account_masked
        elif row_index == 9:
            account_text = acter_account_1_masked
        else:  # row_index == 10
            account_text = acter_account_2_masked

        draw_text_with_kerning(
            draw, (NUMERO_CUENTA_X, y_pos), account_text,
            font, TEXT_COLOR, KERNING
        )

    # Save result
    base_img.convert("RGB").save(output_path, quality=85, optimize=True)

    return output_path
