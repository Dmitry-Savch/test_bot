import os
import pytest
from PIL import Image
from mexc_mxn_withdraw_history_modifier import render_mexc_mxn_withdraw_history


def test_render_mexc_mxn_withdraw_history_creates_file():
    """Test that render_mexc_mxn_withdraw_history creates an output file."""
    output_path = "output/test_mexc_mxn_history.png"
    template_path = "templates/mexc_mxn_withdraw_history.png"

    if not os.path.exists(template_path):
        pytest.skip(f"Template not found: {template_path}")

    result = render_mexc_mxn_withdraw_history(
        tran_1="1,234.56",
        tran_2="987.65",
        tran_3="2,345.67",
        tran_4="456.78",
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


def test_render_mexc_mxn_withdraw_history_valid_image():
    """Test that the output is a valid PNG image."""
    output_path = "output/test_mexc_mxn_history_valid.png"
    template_path = "templates/mexc_mxn_withdraw_history.png"

    if not os.path.exists(template_path):
        pytest.skip(f"Template not found: {template_path}")

    result = render_mexc_mxn_withdraw_history(
        tran_1="500.00",
        tran_2="750.50",
        tran_3="1,200.25",
        tran_4="300.75",
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
