"""
General image processing utilities.
"""
from typing import Tuple
from PIL import Image


def resize_image(image: Image.Image, scale: float) -> Image.Image:
    """
    Resize image by a given scale factor.

    Args:
        image: PIL Image to resize
        scale: Scale factor (e.g., 0.5 for 50%, 2.0 for 200%)

    Returns:
        Resized PIL Image
    """
    width, height = image.size
    new_size = (int(width * scale), int(height * scale))
    return image.resize(new_size, Image.LANCZOS)


def crop_image(image: Image.Image, box: Tuple[int, int, int, int]) -> Image.Image:
    """
    Crop image to specified box.

    Args:
        image: PIL Image to crop
        box: (left, top, right, bottom) coordinates

    Returns:
        Cropped PIL Image
    """
    return image.crop(box)


def ensure_rgba(image: Image.Image) -> Image.Image:
    """
    Ensure image is in RGBA mode.

    Args:
        image: PIL Image

    Returns:
        PIL Image in RGBA mode
    """
    if image.mode != "RGBA":
        return image.convert("RGBA")
    return image


def ensure_rgb(image: Image.Image) -> Image.Image:
    """
    Ensure image is in RGB mode.

    Args:
        image: PIL Image

    Returns:
        PIL Image in RGB mode
    """
    if image.mode != "RGB":
        return image.convert("RGB")
    return image
