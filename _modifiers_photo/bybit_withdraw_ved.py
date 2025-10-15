"""
Bybit VED Withdraw History Screenshot Generator

Generates withdrawal history screenshots for Bybit with VED (Venezuelan Bolívar) currency.
Uses optimized TableRenderer for clean and efficient rendering.
"""
from PIL import Image
from _utils.table_renderer import TableRenderer, create_bybit_table_config


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
    base_img = Image.open(template_path).convert("RGBA")

    # Add **** to account numbers
    lead_number_masked = lead_number + "****"
    persa_number_masked = persa_number + "****"

    # Currency suffix for VED (displayed as Bs)
    currency = " Bs"

    # Prepare row data
    rows = [
        # Row 1
        {
            'time': time_in_description,
            'account': lead_number_masked,
            'bank': lead_bank,
            'amount': transaction_lead_10 + currency,
        },
        # Row 2
        {
            'time': time_in_description,
            'account': lead_number_masked,
            'bank': lead_bank,
            'amount': transaction_lead_main + currency,
        },
        # Row 3
        {
            'time': time_in_description,
            'account': lead_number_masked,
            'bank': lead_bank,
            'amount': transaction_lead_10 + currency,
        },
        # Row 4
        {
            'time': time_in_description,
            'account': lead_number_masked,
            'bank': lead_bank,
            'amount': transaction_lead_main + currency,
        },
        # Row 5
        {
            'time': time_in_description,
            'account': lead_number_masked,
            'bank': lead_bank,
            'amount': transaction_lead_11 + currency,
        },
        # Row 6
        {
            'time': time_in_description,
            'account': persa_number_masked,
            'bank': lead_bank,
            'amount': total_payout + currency,
        },
    ]

    # Render table using optimized renderer
    config = create_bybit_table_config()
    renderer = TableRenderer(config)
    result_img = renderer.render_table(base_img, rows)

    # Save (already resized)
    result_img.convert("RGB").save(output_path, quality=85, optimize=True)

    return output_path
