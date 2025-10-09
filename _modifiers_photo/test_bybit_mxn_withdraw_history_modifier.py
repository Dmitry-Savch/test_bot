import os
import pytest
from PIL import Image
from bybit_mxn_withdraw_history_modifier import render_bybit_mxn_withdraw_history


def test_render_bybit_mxn_withdraw_history_creates_file():
    """Test that render_bybit_mxn_withdraw_history creates an output file."""
    output_path = "output/test_bybit_mxn_history.png"
    template_path = "templates/bybit_mxn_withdraw_history.png"

    if not os.path.exists(template_path):
        pytest.skip(f"Template not found: {template_path}")

    result = render_bybit_mxn_withdraw_history(
        transaction_lead_10="488.323",
        transaction_lead_main="241.579",
        transaction_lead_11="620.000",
        total_payout="4.911.820",
        lead_bank="BBVA Bancomer",
        lead_number="4152888",
        persa_number="9876543",
        time_in_description="Hace un mes",
        template_path=template_path,
        output_path=output_path
    )

    assert result == output_path
    assert os.path.exists(output_path)

    if os.path.exists(output_path):
        os.remove(output_path)


def test_render_bybit_mxn_withdraw_history_valid_image():
    """Test that the output is a valid PNG image."""
    output_path = "output/test_bybit_mxn_history_valid.png"
    template_path = "templates/bybit_mxn_withdraw_history.png"

    if not os.path.exists(template_path):
        pytest.skip(f"Template not found: {template_path}")

    result = render_bybit_mxn_withdraw_history(
        transaction_lead_10="500.00",
        transaction_lead_main="750.50",
        transaction_lead_11="1,200.25",
        total_payout="10.000.000",
        lead_bank="Santander",
        lead_number="1234567",
        persa_number="7654321",
        time_in_description="Hace 2 días",
        template_path=template_path,
        output_path=output_path
    )

    try:
        img = Image.open(result)
        assert img.format == "PNG"
        img.close()
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)
