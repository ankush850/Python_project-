import os
from pathlib import Path
from PIL import Image


def read_images_from_directory(directory):
    """
    Reads all image file paths from a directory
    """
    supported_exts = [".jpg", ".jpeg", ".png", ".bmp"]
    directory = Path(directory)

    if not directory.is_dir():
        raise FileNotFoundError(f"Directory {directory} not found!")

    image_files = []
    for ext in supported_exts:
        image_files.extend(directory.glob(f"*{ext}"))

    return [str(path) for path in image_files]
