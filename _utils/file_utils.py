"""
General file operation utilities.
"""
import os
from typing import Optional


def ensure_directory_exists(directory_path: str) -> None:
    """
    Create directory if it doesn't exist.

    Args:
        directory_path: Path to directory
    """
    os.makedirs(directory_path, exist_ok=True)


def get_file_extension(file_path: str) -> str:
    """
    Get file extension from path.

    Args:
        file_path: Path to file

    Returns:
        File extension (with dot)
    """
    return os.path.splitext(file_path)[1]


def file_exists(file_path: str) -> bool:
    """
    Check if file exists.

    Args:
        file_path: Path to file

    Returns:
        True if file exists, False otherwise
    """
    return os.path.exists(file_path) and os.path.isfile(file_path)


def generate_output_path(
    output_dir: str,
    user_id: int,
    prefix: str = "screenshot",
    extension: str = ".png"
) -> str:
    """
    Generate output file path for a screenshot.

    Args:
        output_dir: Output directory
        user_id: User ID
        prefix: Filename prefix
        extension: File extension

    Returns:
        Full path to output file
    """
    ensure_directory_exists(output_dir)
    filename = f"{prefix}_{user_id}{extension}"
    return os.path.join(output_dir, filename)
