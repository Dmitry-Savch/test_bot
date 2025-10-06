from PIL import Image
from utils.text_draw import execute as text_draw_execute


def render_sat_form(
    beneficiario: str,
    numero_cuenta: str,
    importe: str,
    valor_enviado: str,
    template_path: str = "templates/sat_form.png",
    output_path: str = "output/result.png"
) -> str:
    base_img = Image.open(template_path).convert("RGBA")

    font_family = "fonts/OpenSans-Semibold.ttf"
    black_color = (55, 55, 55)
    font_size = 50
    kr_default = 1.0

    base_img = text_draw_execute(
        base_image=base_img,
        font_sz=font_size,
        text=beneficiario,
        position=(580, 903),
        alignment='left',
        font_family=font_family,
        text_color=black_color,
        kerning=kr_default
    )

    base_img = text_draw_execute(
        base_image=base_img,
        font_sz=font_size,
        text=numero_cuenta,
        position=(580, 1109),
        alignment='left',
        font_family=font_family,
        text_color=black_color,
        kerning=kr_default
    )

    base_img = text_draw_execute(
        base_image=base_img,
        font_sz=font_size,
        text=importe,
        position=(580, 1307),
        alignment='left',
        font_family=font_family,
        text_color=black_color,
        kerning=kr_default
    )

    base_img = text_draw_execute(
        base_image=base_img,
        font_sz=font_size,
        text=valor_enviado,
        position=(580, 1503),
        alignment='left',
        font_family=font_family,
        text_color=black_color,
        kerning=kr_default
    )

    width, height = base_img.size
    new_size = (int(width * 0.7), int(height * 0.7))
    base_img_resized = base_img.resize(new_size, Image.LANCZOS)
    base_img_resized.convert("RGB").save(output_path, quality=85, optimize=True)

    return output_path
