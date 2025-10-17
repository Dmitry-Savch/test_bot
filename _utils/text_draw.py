from typing import Tuple, Literal, Union, Optional
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
    Uses textbbox for precise glyph metrics.
    """
    # textbbox returns (left, top, right, bottom)
    bbox = draw.textbbox((0, 0), text, font=font)
    return (bbox[2] - bbox[0], bbox[3] - bbox[1])

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


def _normalize_opacity(opacity: Optional[Union[int, float]]) -> int:
    if opacity is None:
        return 255
    if isinstance(opacity, float):
        # accept 0.0–1.0 floats
        return int(round(max(0.0, min(1.0, opacity)) * 255))
    # accept 0–255 ints
    return int(max(0, min(255, opacity)))

def _to_rgba(c, fallback_alpha=255):
    if c is None:
        return None
    if len(c) == 3:
        r, g, b = c
        return (int(r), int(g), int(b), int(fallback_alpha))
    elif len(c) == 4:
        r, g, b, a = c
        if isinstance(a, float):
            a = int(round(max(0.0, min(1.0, a)) * 255))
        return (int(r), int(g), int(b), int(max(0, min(255, a))))
    raise ValueError("Color tuples must be (R,G,B) or (R,G,B,A)")


def execute(
    base_image: PILImage.Image,
    font_sz: float,
    text: str,
    position: Point,
    alignment: Literal['left', 'right', 'center'] = 'left',
    font_family: str = 'fonts/semibold.woff2',
    text_color: Union[Tuple[int,int,int], Tuple[int,int,int,int]] = (55, 55, 55),
    kerning: float = 1.0,
    y_limit: Optional[int] = None,
    vertical_bound: Optional[Literal['above','below']] = None,
    opacity: Optional[int] = 254,
) -> PILImage.Image:
    """
    Draw `text` onto `base_image` and return a new Image with the rendering applied.
    The input `base_image` is not modified.

    Args:
        alignment: Text alignment - 'left', 'right', or 'center'
                  - 'left': position is left edge of text
                  - 'right': position is right edge of text
                  - 'center': position is center of text

    NOTE: `position[1]` is treated as the **bottom** of the text's ink box.
    """
    result = base_image.copy()

    # No-op early exit: return unchanged clone if position is (0,0)
    if position[0] == 0 and position[1] == 0:
        return result

    # Vertical bound checks still compare against the provided Y (bottom line)
    if y_limit is not None and vertical_bound in ('above', 'below'):
        if vertical_bound == 'above' and position[1] < y_limit:
            return result
        elif vertical_bound == 'below' and position[1] > y_limit:
            return result

    font = _load_font(font_family, font_sz)

    # --- Normalize color and opacity ---
    alpha_from_param = _normalize_opacity(opacity)
    fill = _to_rgba(text_color, fallback_alpha=alpha_from_param)

    # Decide if we need an overlay (transparency)
    needs_alpha = (fill[3] < 255)

    # Always work on an RGBA surface to respect alpha
    base_rgba = result.convert("RGBA")
    overlay = PILImage.new("RGBA", base_rgba.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # --- Bottom-align on the given Y ---------------------------------------
    req_x, req_y = int(position[0]), int(position[1])

    # Measure text box once (ink box)
    text_w, text_h = _text_size(draw, text, font)

    # Measure advance width the same way we'll draw it
    native_adv = _text_length(font, draw, text)  # font.getlength/textlength
    extra_tracking = max(0, len(text) - 1) * float(kerning or 0.0)
    text_w = int(round(native_adv + extra_tracking))

    # X position based on alignment
    if alignment.lower() == 'right':
        x_pos = req_x - text_w
    elif alignment.lower() == 'center':
        x_pos = req_x - (text_w // 2)
    else:  # left
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


# Backward compatibility alias with old-style top-based positioning
def draw_text_with_kerning(
    image: PILImage.Image,
    font_size: int,
    text: str,
    position: Tuple[int, int],
    font_family: str = "fonts/OpenSans-Semibold.ttf",
    text_color: Tuple[int, int, int] = (255, 255, 255),
    alignment: Literal['left', 'right', 'center'] = 'left',
    kerning: float = 1.4
) -> PILImage.Image:
    """
    Legacy wrapper for backward compatibility.
    Uses old-style top-based Y positioning (not baseline).
    Supports left, right, and center alignment.
    """
    # Create overlay for transparency
    overlay = PILImage.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Load font
    font = _load_font(font_family, font_size)

    x, y = position
    r, g, b = text_color
    fill = (r, g, b, 255)

    # Calculate text width with kerning
    native_adv = _text_length(font, draw, text)
    extra_tracking = max(0, len(text) - 1) * kerning
    text_width = int(round(native_adv + extra_tracking))

    # Adjust x position based on alignment
    if alignment == 'right':
        x = x - text_width
    elif alignment == 'center':
        x = x - (text_width // 2)

    # Draw text with kerning using old top-based positioning
    _draw_text_with_tracking(draw, (x, y), text, font, fill, tracking=kerning)

    # Composite and return
    result = image.convert("RGBA")
    result.alpha_composite(overlay)
    return result


def execute_centered_between(
    base_image: PILImage.Image,
    font_sz: float,
    text: str,
    x1: int,
    x2: int,
    y: int,  # baseline Y
    font_family: str = 'fonts/semibold.woff2',
    text_color: Union[Tuple[int,int,int], Tuple[int,int,int,int]] = (55, 55, 55),
    kerning: float = 1.0,  # extra tracking in px
    y_limit: Optional[int] = None,
    vertical_bound: Optional[Literal['above','below']] = None,
    opacity: Union[int, float] = 254  # 0–255 or 0.0–1.0
) -> PILImage.Image:
    """
    Draw `text` centered horizontally between x1 and x2, on baseline y.
    Uses an RGBA overlay so opacity always applies (even with RGB text_color).
    Returns a new PIL Image.
    """
    if x2 <= x1:
        raise ValueError("x2 must be greater than x1")

    result = base_image.copy()

    # Optional vertical bound early exit
    if y_limit is not None and vertical_bound in ('above', 'below'):
        if vertical_bound == 'above' and y < y_limit:
            return result
        elif vertical_bound == 'below' and y > y_limit:
            return result

    # ----- Always draw on an RGBA overlay so alpha is respected -----
    base_rgba = result.convert("RGBA")
    overlay = PILImage.new("RGBA", base_rgba.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    font = _load_font(font_family, font_sz)

    # ---- Normalize opacity to 0..255 ----
    if isinstance(opacity, float):
        # allow 0.0..1.0
        opacity = int(round(max(0.0, min(1.0, opacity)) * 255))
    else:
        opacity = int(max(0, min(255, opacity)))

    # ---- Normalize color to RGBA with opacity applied ----
    if len(text_color) == 3:
        r, g, b = text_color
        a = opacity
    elif len(text_color) == 4:
        r, g, b, a = text_color
        if isinstance(a, float) and 0.0 <= a <= 1.0:
            a = int(round(a * 255))
        a = int(max(0, min(255, a)))
        # multiply per-pixel alpha by global opacity
        a = int(round(a * (opacity / 255.0)))
    else:
        raise ValueError("text_color must be (R,G,B) or (R,G,B,A)")

    fill = (int(r), int(g), int(b), int(a))

    # ---- compute total advance including extra tracking ----
    base_advance = _text_length(font, draw, text)
    extra_tracking = max(0.0, float(kerning or 0.0)) * max(0, len(text) - 1)
    total_advance = base_advance + extra_tracking

    span_width = x2 - x1
    start_x = int(round(x1 + (span_width - total_advance) / 2.0))
    if total_advance > span_width:
        start_x = x1

    ascent, _descent = font.getmetrics()
    top_y = int(y - ascent)

    _draw_text_with_tracking(draw, (start_x, top_y), text, font, fill, tracking=float(kerning or 0.0))

    # Composite overlay with correct alpha
    result = base_rgba.copy()
    result.alpha_composite(overlay)
    return result
