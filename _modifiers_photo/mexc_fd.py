"""
MEXC FD Screenshot Generator

Generates transaction screenshots for MEXC FD.
Structure: 10 rows × 6 columns (Cripto, Banco, Tiempo, Estado, Monto, Dirección)
Uses optimized TableRenderer for clean and efficient rendering.
"""
from PIL import Image
from _utils.table_renderer import TableRenderer, create_mexc_fd_table_config


def render_mexc_fd(
    currency: str,
    lead_bank: str,
    acter_bank: str,
    lead_time: str,
    acter_time: str,
    fee_1: str,
    fee_2: str,
    fee_3: str,
    fee_4: str,
    lead_address: str,
    acter_address: str,
    template_path: str = "templates/mexc_fd/SR_ARS_MEXCFD_WITHDRAW_HISTORY.png",
    output_path: str = "output/SR_ARS_MEXCFD_WITHDRAW_HISTORY_RESULT.png"
) -> str:
    """
    Render MEXC FD transaction screenshot with 10 rows and 5 columns.

    Table structure (10 rows × 5 columns to draw):
    - Column 1 (CRIPTO): Currency - same value for all 10 rows
    - Column 2 (BANCO): Bank - rows 1-9 use lead_bank, row 10 uses acter_bank
    - Column 3 (TIEMPO): Time - rows 1-9 use lead_time, row 10 uses acter_time
    - Column 4 (ESTADO): Status - NOT DRAWN (already on template)
    - Column 5 (MONTO): Fee/Amount - distributed as per specification
    - Column 6 (DIRECCION): Address - rows 1-9 use lead_address, row 10 uses acter_address

    Fee distribution:
    - fee_1: rows 1, 3, 5
    - fee_2: rows 2, 8
    - fee_3: rows 4, 6, 9
    - fee_4: row 10

    Args:
        currency: Currency (e.g., "ARS", "MXN") - fills all 10 rows
        lead_bank: Lead bank name - fills rows 1-9
        acter_bank: Acter bank name - fills row 10
        lead_time: Lead time (e.g., "Hace 2 días") - fills rows 1-9
        acter_time: Acter time - fills row 10
        fee_1: Fee amount for rows 1, 3, 5
        fee_2: Fee amount for rows 2, 8
        fee_3: Fee amount for rows 4, 6, 9
        fee_4: Fee amount for row 10
        lead_address: Lead withdrawal address (e.g., "3001382195******") - fills rows 1-9
        acter_address: Acter withdrawal address - fills row 10
        template_path: Path to template image
        output_path: Path to save result

    Returns:
        Path to the generated screenshot
    """
    # Load template (no resizing - use original size)
    base_img = Image.open(template_path).convert("RGBA")

    # Define fee distribution mapping
    # fee_1: rows 1, 3, 5
    # fee_2: rows 2, 8
    # fee_3: rows 4, 6, 7
    # fee_4: row 10
    # Row 9: not specified, using fee_3
    fee_mapping = {
        0: fee_1,  # Row 1
        1: fee_2,  # Row 2
        2: fee_1,  # Row 3
        3: fee_3,  # Row 4
        4: fee_1,  # Row 5
        5: fee_3,  # Row 6
        6: fee_3,  # Row 7
        7: fee_2,  # Row 8
        8: fee_3,  # Row 9 (not specified, using fee_3)
        9: fee_4,  # Row 10
    }

    # Prepare row data - 10 rows with 5 columns each
    # Note: "Estado" (Status) column is already on template, so we don't draw it
    rows = []

    # Rows 1-9: Lead data
    for i in range(9):
        rows.append({
            'currency': currency,
            'bank': lead_bank,
            'time': lead_time,
            'fee': fee_mapping[i],
            'address': lead_address,
        })

    # Row 10: Acter data
    rows.append({
        'currency': currency,
        'bank': acter_bank,
        'time': acter_time,
        'fee': fee_4,
        'address': acter_address,
    })

    # Render table using optimized renderer
    config = create_mexc_fd_table_config()
    renderer = TableRenderer(config)
    result_img = renderer.render_table(base_img, rows)

    # Save result
    result_img.convert("RGB").save(output_path, quality=85, optimize=True)

    return output_path
