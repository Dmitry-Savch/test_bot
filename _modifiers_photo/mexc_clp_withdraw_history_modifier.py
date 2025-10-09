"""
MEXC CLP Withdraw History Screenshot Generator

Generates withdrawal history screenshots for MEXC with CLP (Chilean Peso) currency.
Uses 4 transactions with configurable amounts, bank names, and account numbers.
"""
from PIL import Image
from _text_line_render.text_draw import execute as text_draw_execute


def render_mexc_clp_withdraw_history(
    tran_1: str,
    tran_2: str,
    tran_3: str,
    tran_4: str,
    lead_bank: str,
    lead_number: str,
    persa_number: str,
    time_in_description: str,
    template_path: str = "templates/mexc_clp_withdraw_history.png",
    output_path: str = "output/result.png"
) -> str:
    """
    Render MEXC CLP withdrawal history screenshot with 4 transactions.

    Args:
        tran_1: Transaction 1 amount (e.g., "488.323")
        tran_2: Transaction 2 amount
        tran_3: Transaction 3 amount
        tran_4: Transaction 4 amount
        lead_bank: Lead bank name
        lead_number: Lead account number without ****
        persa_number: Persa account number without ****
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

    # Y positions for 4 transactions (based on actual table layout)
    y_positions = [340, 410, 480, 550]

    # X positions for columns (based on actual table layout)
    x_time = 172        # Tiempo column
    x_account = 387     # Numero de cuenta column
    x_bank = 663        # Banco column
    x_amount_end = 1010 # Monto column (right-aligned)

    # Currency suffix for CLP
    currency = " CLP"

    # Transaction amounts
    transactions = [tran_1, tran_2, tran_3, tran_4]

    # Account numbers (first 3 use lead_number, 4th uses persa_number)
    account_numbers = [
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
