from PIL import Image, ImageEnhance

def overlay_image_pillow(
    base_img: Image.Image,
    overlay_img: Image.Image,
    bottom_right_coords: tuple,
    overlay_height: int,
    brightness: int = 100,   # 0–100 (100 = normal)
    opacity: int = 255,      # 0–255 (255 = fully opaque)
    align: str = 'right'
) -> Image.Image:
    """
    Overlays overlay_img onto base_img. Both must be PIL Images.

    Args:
        base_img (PIL.Image.Image): The base image.
        overlay_img (PIL.Image.Image): The overlay image.
        bottom_right_coords (tuple): (x, y) anchor in base image along the bottom edge
                                     of the overlay. If align='right', (x, y) is the
                                     overlay's bottom-right corner; if 'left', it's
                                     the bottom-left corner.
        overlay_height (int): Desired overlay height in pixels (width keeps aspect).
        brightness (int): 0–100, where 100 = no change.
        opacity (int): 0–255 alpha applied on top of overlay's existing alpha.
        align (str): 'right' or 'left'.
    Returns:
        PIL.Image.Image: A new image with the overlay applied.
    """
    # Work on copies; normalize modes
    base_mode = base_img.mode
    base = base_img.convert("RGBA").copy()
    ov = overlay_img.convert("RGBA").copy()

    # --- resize proportionally by height ---
    aspect = ov.width / ov.height if ov.height else 1.0
    new_w = max(1, int(round(overlay_height * aspect)))
    new_h = max(1, int(overlay_height))
    ov = ov.resize((new_w, new_h), Image.LANCZOS)

    # --- brightness (apply to RGB channels only) ---
    # Map 0–100 to a factor (100 -> 1.0, 0 -> 0.0)
    factor = max(0.0, brightness / 100.0)
    r, g, b, a = ov.split()
    rgb = Image.merge("RGB", (r, g, b))
    rgb = ImageEnhance.Brightness(rgb).enhance(factor)
    ov = Image.merge("RGBA", (*rgb.split(), a))

    # --- opacity (multiply existing alpha by opacity/255) ---
    if opacity < 255:
        alpha_mul = max(0.0, min(1.0, opacity / 255.0))
        a = ov.getchannel("A").point(lambda px: int(px * alpha_mul))
        ov.putalpha(a)

    # --- positioning ---
    x, y = bottom_right_coords
    if align == 'right':
        top_left_x = int(x - new_w)
    elif align == 'left':
        top_left_x = int(x)
    else:
        raise ValueError("align must be 'right' or 'left'.")

    top_left_y = int(y - new_h)

    # Optional: clip paste box to base bounds? (Pillow will handle off-canvas parts.)
    # Paste using overlay's alpha as mask
    base.paste(ov, (top_left_x, top_left_y), ov)

    # Return in the original base mode if possible
    return base.convert(base_mode) if base_mode != "RGBA" else base