"""
Bybit VED Withdraw History Screenshot Generator

Generates withdrawal history screenshots for Bybit with VED (Venezuelan Bolívar) currency.
Uses 6 transactions with configurable amounts, bank names, and account numbers.
VED is converted to "Bs" for display (business logic preserved).
"""
from PIL import Image
from _text_line_render.text_draw import execute as text_draw_execute


def render_bybit_ved_withdraw_history(
    transaction_lead_10: str,
    transaction_lead_main: str,
    transaction_lead_11: str,
    total_payout: str,
    lead_bank: str,
    lead_number: str,
    persa_number: str,
    time_in_description: str,
    template_path: str = "templates/bybit_ved_withdraw_history.png",
    output_path: str = "output/result.png"
) -> str:
    """
    Render Bybit VED withdrawal history screenshot with 6 transactions.

    Args:
        transaction_lead_10: Transaction Lead 10 amount (appears in rows 1 and 3, e.g., "488.323")
        transaction_lead_main: Transaction Lead amount (appears in rows 2 and 4, e.g., "241.579")
        transaction_lead_11: Transaction Lead 11 amount (appears in row 5, e.g., "620.000")
        total_payout: Total payout amount (appears in row 6, e.g., "4.911.820")
        lead_bank: Lead bank name (used for all 6 rows)
        lead_number: Lead account number without **** (used for rows 1-5)
        persa_number: Persa account number without **** (used for row 6)
        time_in_description: Transaction time (e.g., "Hace un mes")
        template_path: Path to template image
        output_path: Path to save result

    Returns:
        Path to the generated screenshot
    """
    base_img = Image.open(template_path).convert("RGBA")

    # Configuration - optimized for table layout
    font_family = "fonts/OpenSans-Semibold.ttf"
    white_color = (255, 255, 255)  # Pure white
    fs = 50  # Font size to fit in table rows
    kr_default = 1.0

    # Add **** to account numbers (business logic preserved)
    lead_number_masked = lead_number + "****"
    persa_number_masked = persa_number + "****"

    # Y positions for 6 transactions (based on actual table layout)
    y_positions = [340, 410, 480, 550, 620, 690]

    # X positions for columns (based on actual table layout)
    x_time = 172        # Tiempo column
    x_account = 387     # Numero de cuenta column
    x_bank = 663        # Banco column
    x_amount_end = 1010 # Monto column (right-aligned)

    # Currency suffix for VED (business logic: VED → "Bs" conversion)
    currency = " Bs"

    # Transaction amounts (mapping based on BOT_QUESTIONS_STRUCTURE.md)
    # Row 1: transaction_lead_10
    # Row 2: transaction_lead_main
    # Row 3: transaction_lead_10
    # Row 4: transaction_lead_main
    # Row 5: transaction_lead_11
    # Row 6: total_payout
    transactions = [
        transaction_lead_10,
        transaction_lead_main,
        transaction_lead_10,
        transaction_lead_main,
        transaction_lead_11,
        total_payout
    ]

    # Account numbers (first 5 use lead_number, 6th uses persa_number)
    account_numbers = [
        lead_number_masked,
        lead_number_masked,
        lead_number_masked,
        lead_number_masked,
        lead_number_masked,
        persa_number_masked
    ]

    # Render each transaction row
    for y_pos, amount, account_num in zip(y_positions, transactions, account_numbers):
        # Calculate Y position - preserved logic: "845 - fs / 2"
        y_centered = y_pos - fs // 2

        # Time column
        base_img = text_draw_execute(
            base_image=base_img,
            font_sz=fs,
            text=time_in_description,
            position=(x_time, y_centered),
            alignment='left',
            font_family=font_family,
            text_color=white_color,
            kerning=kr_default
        )

        # Account number column
        base_img = text_draw_execute(
            base_image=base_img,
            font_sz=fs,
            text=account_num,
            position=(x_account, y_centered),
            alignment='left',
            font_family=font_family,
            text_color=white_color,
            kerning=kr_default
        )

        # Bank name column
        base_img = text_draw_execute(
            base_image=base_img,
            font_sz=fs,
            text=lead_bank,
            position=(x_bank, y_centered),
            alignment='left',
            font_family=font_family,
            text_color=white_color,
            kerning=kr_default
        )

        # Amount column (right-aligned with currency)
        amount_text = amount + currency
        base_img = text_draw_execute(
            base_image=base_img,
            font_sz=fs,
            text=amount_text,
            position=(x_amount_end, y_centered),
            alignment='right',
            font_family=font_family,
            text_color=white_color,
            kerning=kr_default
        )

    # Resize and save (following sat_form_modifier.py pattern)
    width, height = base_img.size
    new_size = (int(width * 0.7), int(height * 0.7))
    base_img_resized = base_img.resize(new_size, Image.LANCZOS)
    base_img_resized.convert("RGB").save(output_path, quality=85, optimize=True)

    return output_path
