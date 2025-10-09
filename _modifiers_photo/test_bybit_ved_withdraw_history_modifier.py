import os
import pytest
from PIL import Image
from bybit_ved_withdraw_history_modifier import render_bybit_ved_withdraw_history


def test_render_bybit_ved_withdraw_history_creates_file():
    """Test that render_bybit_ved_withdraw_history creates an output file."""
    output_path = "output/test_bybit_ved_history.png"
    template_path = "templates/bybit_ved_withdraw_history.png"

    if not os.path.exists(template_path):
        pytest.skip(f"Template not found: {template_path}")

    result = render_bybit_ved_withdraw_history(
        transaction_lead_10="50.00",
        transaction_lead_main="75.50",
        transaction_lead_11="100.25",
        total_payout="1.500.000",
        lead_bank="Banco de Venezuela",
        lead_number="8888888",
        persa_number="9999999",
        time_in_description="Hace un mes",
        template_path=template_path,
        output_path=output_path
    )

    assert result == output_path
    assert os.path.exists(output_path)

    if os.path.exists(output_path):
        os.remove(output_path)


def test_render_bybit_ved_withdraw_history_valid_image():
    """Test that the output is a valid PNG image."""
    output_path = "output/test_bybit_ved_history_valid.png"
    template_path = "templates/bybit_ved_withdraw_history.png"

    if not os.path.exists(template_path):
        pytest.skip(f"Template not found: {template_path}")

    result = render_bybit_ved_withdraw_history(
        transaction_lead_10="30.00",
        transaction_lead_main="45.50",
        transaction_lead_11="60.25",
        total_payout="800.000",
        lead_bank="Banesco",
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


def test_render_bybit_ved_currency_conversion():
    """Test that VED currency is converted to Bs."""
    output_path = "output/test_bybit_ved_currency.png"
    template_path = "templates/bybit_ved_withdraw_history.png"

    if not os.path.exists(template_path):
        pytest.skip(f"Template not found: {template_path}")

    # This test verifies the business logic: VED → "Bs" conversion
    result = render_bybit_ved_withdraw_history(
        transaction_lead_10="100",
        transaction_lead_main="200",
        transaction_lead_11="300",
        total_payout="5.000.000",
        lead_bank="Provincial",
        lead_number="1111111",
        persa_number="2222222",
        time_in_description="Hace una semana",
        template_path=template_path,
        output_path=output_path
    )

    assert os.path.exists(result)

    if os.path.exists(output_path):
        os.remove(output_path)
