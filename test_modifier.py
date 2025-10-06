from modifiers.sat_form_modifier import render_sat_form
import os

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)

    result = render_sat_form(
        beneficiario="Juan Perez Rodriguez",
        numero_cuenta="1234567890",
        importe="150.50",
        valor_enviado="150.50",
        template_path="templates/sat_form.png",
        output_path="output/test_result.png"
    )

    print(f"Result saved to: {result}")
