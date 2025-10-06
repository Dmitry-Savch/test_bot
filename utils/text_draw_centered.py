from typing import Tuple, Literal, Union, Optional
from PIL import Image as PILImage
from PIL import ImageDraw, ImageFont

Point = Tuple[int, int]

def _load_font(font_family: str, font_sz: float) -> ImageFont.FreeTypeFont:
    """Try to load TTF/OTF; fall back to PIL default if not supported."""
    try:
        return ImageFont.truetype(font_family, int(font_sz))
    except Exception:
        return ImageFont.load_default()

def _glyph_advance(font: ImageFont.FreeTypeFont, draw: ImageDraw.ImageDraw, text: str) -> float:
    """
    Preferred x-advance using font.getlength when available; fallback to draw.textlength.
    This reflects what Pillow will advance when drawing (excludes extra tracking).
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
    Draw per-glyph, adding extra tracking (letter spacing) in pixels on top of font kerning.
    """
    x, y = position
    if not tracking:
        draw.text((x, y), text, font=font, fill=fill)
        return

    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        adv = _glyph_advance(font, draw, ch)
        x += int(round(adv + tracking))

def execute_centered_between(
    base_image: PILImage.Image,
    font_sz: float,
    text: str,
    x1: int,
    x2: int,
    y: int,  # baseline Y (your current behavior)
    font_family: str = 'fonts/semibold.woff2',
    text_color: Union[Tuple[int,int,int], Tuple[int,int,int,int]] = (55, 55, 55),
    kerning: float = 1.0,  # extra tracking in px between glyphs
    y_limit: Optional[int] = None,
    vertical_bound: Optional[Literal['above','below']] = None
) -> PILImage.Image:
    """
    Draw `text` centered horizontally between x1 and x2, on baseline y.
    Returns a new PIL Image; does not modify the input.
    """
    if x2 <= x1:
        raise ValueError("x2 must be greater than x1")

    result = base_image.copy()

    # Optional vertical bound early-exit (preserves your existing behavior)
    if y_limit is not None and vertical_bound in ('above', 'below'):
        if vertical_bound == 'above' and y < y_limit:
            return result
        elif vertical_bound == 'below' and y > y_limit:
            return result

    # Prepare drawing surface (respect alpha in text_color)
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
    elif len(text_color) == 4:
        r, g, b, a = text_color
        if isinstance(a, float) and 0.0 <= a <= 1.0:
            a = int(round(a * 255))
        a = int(max(0, min(255, a)))
        fill = (int(r), int(g), int(b), a)
    else:
        raise ValueError("text_color must be (R,G,B) or (R,G,B,A)")

    # ---- compute total advance including extra tracking to center properly ----
    base_advance = _glyph_advance(font, draw, text)  # Pillow's native advance
    extra_tracking = max(0.0, float(kerning or 0.0)) * max(0, len(text) - 1)
    total_advance = base_advance + extra_tracking

    # Center within [x1, x2]
    span_width = x2 - x1
    start_x = int(round(x1 + (span_width - total_advance) / 2.0))

    # Optionally clamp to stay within bounds (keeps text inside the span)
    if total_advance > span_width:
        # If text is wider than the span, align to x1 (left) to keep it visible.
        start_x = x1

    # Convert baseline Y to top-left Y using font metrics (as before)
    ascent, _descent = font.getmetrics()
    top_y = int(y - ascent)

    # Draw text
    _draw_text_with_tracking(draw, (start_x, top_y), text, font, fill, tracking=float(kerning or 0.0))

    if needs_alpha:
        result = result.convert("RGBA")
        result.alpha_composite(overlay)

    return result