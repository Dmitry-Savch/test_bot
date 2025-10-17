"""
Bybit Withdraw History Screenshot Generator

Unified generator for withdrawal history screenshots across all currencies.
Uses optimized TableRenderer for clean and efficient rendering.
"""
from PIL import Image
from _utils.table_renderer import TableRenderer, create_bybit_table_config


def render_bybit_withdraw_history(
    transaction_lead_10: str,
    transaction_lead_main: str,
    transaction_lead_11: str,
    total_payout: str,
    lead_bank: str,
    lead_number: str,
    persa_number: str,
    time_in_description: str,
    currency: str,
    template_path: str,
    output_path: str = "output/result.png"
) -> str:
    """
    Render Bybit withdrawal history screenshot with 6 transactions.

    This is a unified function that works with any currency and template.
    It replaces the separate functions for MXN, VED, and CLP.

    Args:
        transaction_lead_10: Transaction Lead 10 amount (appears in rows 1 and 3)
        transaction_lead_main: Transaction Lead amount (appears in rows 2 and 4)
        transaction_lead_11: Transaction Lead 11 amount (appears in row 5)
        total_payout: Total payout amount (appears in row 6)
        lead_bank: Lead bank name (used for all 6 rows)
        lead_number: Lead account number without **** (used for rows 1-5)
        persa_number: Persa account number without **** (used for row 6)
        time_in_description: Transaction time (e.g., "Hace un mes")
        currency: Currency suffix to append to amounts (e.g., " MXN", " Bs", " CLP")
        template_path: Path to template image
        output_path: Path to save result

    Returns:
        Path to the generated screenshot

    Examples:
        # For MXN
        render_bybit_withdraw_history(..., currency=" MXN", template_path="templates/mxn.png")

        # For VED (Venezuelan Bolívar)
        render_bybit_withdraw_history(..., currency=" Bs", template_path="templates/ved.png")

        # For CLP
        render_bybit_withdraw_history(..., currency=" CLP", template_path="templates/clp.png")
    """
    # Load template (no resizing - use original size)
    base_img = Image.open(template_path).convert("RGBA")

    # Add **** to account numbers
    lead_number_masked = f"{lead_number}****"
    persa_number_masked = f"{persa_number}****"

    # Prepare row data
    rows = [
        # Row 1
        {
            'time': time_in_description,
            'account': lead_number_masked,
            'bank': lead_bank,
            'amount': f"{transaction_lead_10}{currency}",
        },
        # Row 2
        {
            'time': time_in_description,
            'account': lead_number_masked,
            'bank': lead_bank,
            'amount': f"{transaction_lead_main}{currency}",
        },
        # Row 3
        {
            'time': time_in_description,
            'account': lead_number_masked,
            'bank': lead_bank,
            'amount': f"{transaction_lead_10}{currency}",
        },
        # Row 4
        {
            'time': time_in_description,
            'account': lead_number_masked,
            'bank': lead_bank,
            'amount': f"{transaction_lead_main}{currency}",
        },
        # Row 5
        {
            'time': time_in_description,
            'account': lead_number_masked,
            'bank': lead_bank,
            'amount': f"{transaction_lead_11}{currency}",
        },
        # Row 6
        {
            'time': time_in_description,
            'account': persa_number_masked,
            'bank': lead_bank,
            'amount': f"{total_payout}{currency}",
        },
    ]

    # Render table using optimized renderer
    config = create_bybit_table_config()
    renderer = TableRenderer(config)
    result_img = renderer.render_table(base_img, rows)

    # Save result
    result_img.convert("RGB").save(output_path, quality=85, optimize=True)

    return output_path
