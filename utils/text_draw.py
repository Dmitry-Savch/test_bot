from typing import Tuple, Literal, Union
from PIL import Image as PILImage
from PIL import ImageDraw, ImageFont

Point = Tuple[int, int]

def _load_font(font_family: str, font_sz: float) -> ImageFont.FreeTypeFont:
    """
    Try to load a TrueType/OpenType font. If loading fails (e.g., WOFF2),
    fall back to PIL's default bitmap font to avoid crashing.
    """
    try:
        # Pillow prefers .ttf/.otf. WOFF/WOFF2 generally not supported.
        return ImageFont.truetype(font_family, int(font_sz))
    except Exception:
        return ImageFont.load_default()

def _text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> Tuple[int, int]:
    """
    Measure text width/height similarly to Wand's metrics.text_width/height.
    Uses textbbox for precise glyph metrics (ink box).
    """
    bbox = draw.textbbox((0, 0), text, font=font)
    return (bbox[2] - bbox[0], bbox[3] - bbox[1])  # (width, height)

def _text_length(font: ImageFont.FreeTypeFont, draw: ImageDraw.ImageDraw, text: str) -> float:
    """
    Preferred width advance using font.getlength (Pillow >= 8.0); fallback to draw.textlength.
    """
    if hasattr(font, "getlength"):
        return font.getlength(text)
    return draw.textlength(text, font=font)

def _draw_text_with_tracking(
    draw: ImageDraw.ImageDraw,
    position: Tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: Tuple[int, int, int, int],
    tracking: float
) -> None:
    """
    Emulates Wand's draw.text_kerning by adding *extra* tracking (letter spacing) in pixels.
    Pillow applies built-in font kerning automatically; this adds additional spacing.
    """
    x, y = position
    # Fast path if no additional tracking
    if not tracking:
        draw.text((x, y), text, font=font, fill=fill)
        return

    # Draw per-glyph with extra advance
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        # Advance by glyph width + tracking
        adv = _text_length(font, draw, ch)
        x += int(round(adv + tracking))


def execute(
    base_image: PILImage.Image,
    font_sz: float,
    text: str,
    position: Point,
    alignment: Literal['left', 'right'] = 'left',
    font_family: str = 'fonts/semibold.woff2',
    text_color: Union[Tuple[int,int,int], Tuple[int,int,int,int]] = (55, 55, 55),
    kerning: float = 1.0,
) -> PILImage.Image:
    """
    Draw `text` onto `base_image` and return a new Image with the rendering applied.
    The input `base_image` is not modified.

    NOTE: `position[1]` is treated as the **bottom** of the text's ink box.
    """
    result = base_image.copy()

    # No-op early exit: return unchanged clone if position is (0,0)
    if position[0] == 0 and position[1] == 0:
        return result

    needs_alpha = len(text_color) == 4
    if needs_alpha:
        base_rgba = result.convert("RGBA")
        overlay = PILImage.new("RGBA", base_rgba.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
    else:
        draw = ImageDraw.Draw(result)

    font = _load_font(font_family, font_sz)

    # Normalize color to RGBA
    if len(text_color) == 3:
        r, g, b = text_color
        fill = (int(r), int(g), int(b), 255)
    else:
        raise ValueError("text_color must be (R,G,B)")

    # --- Bottom-align on the given Y ---------------------------------------
    req_x, req_y = int(position[0]), int(position[1])

    # Measure text box once (ink box)
    text_w, text_h = _text_size(draw, text, font)

    # # X position (right-align if requested)
    # if alignment.lower() == 'right':
    #     x_pos = req_x - int(text_w)
    # else:
    #     x_pos = req_x

    # Measure advance width the same way we'll draw it
    native_adv = _text_length(font, draw, text)  # font.getlength/textlength
    extra_tracking = max(0, len(text) - 1) * float(kerning or 0.0)
    text_w = int(round(native_adv + extra_tracking))

    # X position (right-align uses advance width)
    if alignment.lower() == 'right':
        x_pos = req_x - text_w
    else:
        x_pos = req_x

    # --- baseline alignment like Wand ---
    ascent, descent = font.getmetrics()
    y_pos = int(req_y - ascent)  # req_y is the baseline you want
    # ------------------------------------

    _draw_text_with_tracking(draw, (x_pos, y_pos), text, font, fill, tracking=float(kerning or 0.0))

    if needs_alpha:
        result = result.convert("RGBA")
        result.alpha_composite(overlay)

    return result