"""
Bybit FD (Successful) Screenshot Generator

Generates successful transaction screenshots for Bybit FD.
Uses the "successful.png" template with 11 transaction rows plus additional bottom fields.
Uses optimized TableRenderer for clean and efficient rendering.
"""
from PIL import Image
from _utils.table_renderer import TableRenderer, create_bybit_fd_table_config


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
    template_path: str = "templates/SM_MXN_WHITE_BYBITFD_WITHDRAW_HISTORY.png",
    output_path: str = "output/SM_MXN_WHITE_BYBITFD_WITHDRAW_HISTORY_RESULT.png"
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
    # Load template (no resizing - use original size)
    base_img = Image.open(template_path).convert("RGBA")

    # Add **** to account numbers
    lead_account_masked = f"{lead_account_number}******"
    acter_account_1_masked = f"{acter_account_1}*****"
    acter_account_2_masked = f"{acter_account_2}*****"

    # Prepare row data - 11 rows with 6 columns each
    rows = [
        # Row 1
        {
            'currency': currency,
            'bank': bank,
            'time': time_in_description,
            'status': status,
            'amount': lead_payment_amount,
            'account': lead_account_masked,
        },
        # Row 2
        {
            'currency': currency,
            'bank': bank,
            'time': time_in_description,
            'status': status,
            'amount': lead_payment_amount,
            'account': lead_account_masked,
        },
        # Row 3
        {
            'currency': currency,
            'bank': bank,
            'time': time_in_description,
            'status': status,
            'amount': lead_payment_amount,
            'account': lead_account_masked,
        },
        # Row 4
        {
            'currency': currency,
            'bank': bank,
            'time': time_in_description,
            'status': status,
            'amount': lead_payment_amount,
            'account': lead_account_masked,
        },
        # Row 5
        {
            'currency': currency,
            'bank': bank,
            'time': time_in_description,
            'status': status,
            'amount': lead_payment_amount,
            'account': lead_account_masked,
        },
        # Row 6
        {
            'currency': currency,
            'bank': bank,
            'time': time_in_description,
            'status': status,
            'amount': lead_payment_amount,
            'account': lead_account_masked,
        },
        # Row 7
        {
            'currency': currency,
            'bank': bank,
            'time': time_in_description,
            'status': status,
            'amount': lead_payment_amount,
            'account': lead_account_masked,
        },
        # Row 8
        {
            'currency': currency,
            'bank': bank,
            'time': time_in_description,
            'status': status,
            'amount': lead_payment_amount,
            'account': lead_account_masked,
        },
        # Row 9
        {
            'currency': currency,
            'bank': bank,
            'time': time_in_description,
            'status': status,
            'amount': lead_payment_amount,
            'account': lead_account_masked,
        },
        # Row 10
        {
            'currency': currency,
            'bank': bank,
            'time': time_in_description,
            'status': status,
            'amount': acter_payment_1,
            'account': acter_account_1_masked,
        },
        # Row 11
        {
            'currency': currency,
            'bank': bank,
            'time': time_in_description,
            'status': status,
            'amount': acter_payment_2,
            'account': acter_account_2_masked,
        },
    ]

    # Render table using optimized renderer
    config = create_bybit_fd_table_config()
    renderer = TableRenderer(config)
    result_img = renderer.render_table(base_img, rows)

    # Save result
    result_img.convert("RGB").save(output_path, quality=85, optimize=True)

    return output_path
