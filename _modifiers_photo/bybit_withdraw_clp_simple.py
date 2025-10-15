"""
Bybit CLP Withdraw History Screenshot Generator (Simple Array-Based Approach)

Generates withdrawal history screenshots for Bybit with CLP (Chilean Peso) currency.
Uses simple array-based rendering for clear and maintainable code.
"""
from PIL import Image
from _utils.text_draw import draw_text_with_kerning
from _utils.bybit_config import (
    FONT_FAMILY, FONT_SIZE, TEXT_COLOR, KERNING, Y_POSITIONS,
    TIEMPO_X, NUMERO_CUENTA_X, BANCO_X, MONTO_X
)


def render_bybit_clp_withdraw_history(
    transaction_lead_10: str,
    transaction_lead_main: str,
    transaction_lead_11: str,
    total_payout: str,
    lead_bank: str,
    lead_number: str,
    persa_number: str,
    time_in_description: str,
    template_path: str = "templates/SD_MXN_BLACK_BYBIT_WITHDRAW_HISTORY.png",
    output_path: str = "output/result.png"
) -> str:
    """
    Render Bybit CLP withdrawal history screenshot with 6 transactions.

    Args:
        transaction_lead_10: Transaction Lead 10 amount (appears in rows 1 and 3)
        transaction_lead_main: Transaction Lead amount (appears in rows 2 and 4)
        transaction_lead_11: Transaction Lead 11 amount (appears in row 5)
        total_payout: Total payout amount (appears in row 6)
        lead_bank: Lead bank name (used for all 6 rows)
        lead_number: Lead account number without **** (used for rows 1-5)
        persa_number: Persa account number without **** (used for row 6)
        time_in_description: Transaction time (e.g., "Hace un mes")
        template_path: Path to template image
        output_path: Path to save result

    Returns:
        Path to the generated screenshot
    """
    # Load template (no resizing - use original size)
    result_img = Image.open(template_path).convert("RGBA")

    # Prepare data
    lead_number_masked = lead_number + "****"
    persa_number_masked = persa_number + "****"
    currency = " CLP"

    # Column 1: Tiempo (Time) - 6 identical values
    tiempo_values = [time_in_description] * 6
    for y, text_value in zip(Y_POSITIONS, tiempo_values):
        result_img = draw_text_with_kerning(
            result_img,
            FONT_SIZE,
            text_value,
            position=(TIEMPO_X, y),
            font_family=FONT_FAMILY,
            text_color=TEXT_COLOR,
            alignment="left",
            kerning=KERNING
        )

    # Column 2: Numero de cuenta (Account Number)
    account_values = [
        lead_number_masked,  # Row 1
        lead_number_masked,  # Row 2
        lead_number_masked,  # Row 3
        lead_number_masked,  # Row 4
        lead_number_masked,  # Row 5
        persa_number_masked  # Row 6
    ]
    for y, text_value in zip(Y_POSITIONS, account_values):
        result_img = draw_text_with_kerning(
            result_img,
            FONT_SIZE,
            text_value,
            position=(NUMERO_CUENTA_X, y),
            font_family=FONT_FAMILY,
            text_color=TEXT_COLOR,
            alignment="left",
            kerning=KERNING
        )

    # Column 3: Banco (Bank) - 6 identical values
    banco_values = [lead_bank] * 6
    for y, text_value in zip(Y_POSITIONS, banco_values):
        result_img = draw_text_with_kerning(
            result_img,
            FONT_SIZE,
            text_value,
            position=(BANCO_X, y),
            font_family=FONT_FAMILY,
            text_color=TEXT_COLOR,
            alignment="left",
            kerning=KERNING
        )

    # Column 4: Monto (Amount) - right aligned
    monto_values = [
        transaction_lead_10 + currency,   # Row 1
        transaction_lead_main + currency,  # Row 2
        transaction_lead_10 + currency,   # Row 3
        transaction_lead_main + currency,  # Row 4
        transaction_lead_11 + currency,   # Row 5
        total_payout + currency           # Row 6
    ]
    for y, text_value in zip(Y_POSITIONS, monto_values):
        result_img = draw_text_with_kerning(
            result_img,
            FONT_SIZE,
            text_value,
            position=(MONTO_X, y),
            font_family=FONT_FAMILY,
            text_color=TEXT_COLOR,
            alignment="right",  # Right aligned for amounts
            kerning=KERNING
        )

    # Save result
    result_img.convert("RGB").save(output_path, quality=85, optimize=True)

    return output_path
