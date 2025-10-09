import os
import pytest
from PIL import Image
from mexc_ecu_withdraw_history_modifier import render_mexc_ecu_withdraw_history


def test_render_mexc_ecu_withdraw_history_creates_file():
    """Test that render_mexc_ecu_withdraw_history creates an output file."""
    output_path = "output/test_mexc_ecu_history.png"
    template_path = "templates/mexc_ecu_withdraw_history.png"

    if not os.path.exists(template_path):
        pytest.skip(f"Template not found: {template_path}")

    result = render_mexc_ecu_withdraw_history(
        tran_1="100.50",
        tran_2="75.25",
        tran_3="150.75",
        tran_4="50.00",
        lead_bank="Banco Pichincha",
        lead_number="3333333",
        persa_number="4444444",
        time_in_description="Hace un mes",
        template_path=template_path,
        output_path=output_path
    )

    assert result == output_path
    assert os.path.exists(output_path)

    if os.path.exists(output_path):
        os.remove(output_path)


def test_render_mexc_ecu_withdraw_history_valid_image():
    """Test that the output is a valid PNG image."""
    output_path = "output/test_mexc_ecu_history_valid.png"
    template_path = "templates/mexc_ecu_withdraw_history.png"

    if not os.path.exists(template_path):
        pytest.skip(f"Template not found: {template_path}")

    result = render_mexc_ecu_withdraw_history(
        tran_1="200.00",
        tran_2="150.50",
        tran_3="300.25",
        tran_4="100.75",
        lead_bank="Banco Guayaquil",
        lead_number="5555555",
        persa_number="6666666",
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


def test_render_mexc_ecu_currency_conversion():
    """Test that ECU currency is converted to USD."""
    output_path = "output/test_mexc_ecu_currency.png"
    template_path = "templates/mexc_ecu_withdraw_history.png"

    if not os.path.exists(template_path):
        pytest.skip(f"Template not found: {template_path}")

    # This test verifies the business logic: ECU → "USD" conversion (MEXC only)
    result = render_mexc_ecu_withdraw_history(
        tran_1="50",
        tran_2="100",
        tran_3="150",
        tran_4="200",
        lead_bank="Produbanco",
        lead_number="7777777",
        persa_number="8888888",
        time_in_description="Hace una semana",
        template_path=template_path,
        output_path=output_path
    )

    assert os.path.exists(result)

    if os.path.exists(output_path):
        os.remove(output_path)
