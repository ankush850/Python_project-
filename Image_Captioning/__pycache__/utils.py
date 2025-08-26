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


def read_with_pil(paths):
    """
    Open images using PIL
    """
    pil_images = []
    for p in paths:
        try:
            img = Image.open(p).convert("RGB")
            pil_images.append(img)
        except Exception as e:
            print(f"❌ Could not open {p}: {e}")
    return pil_images


def create_dir(path):
    """
    Creates a directory if it doesn't exist
    """
    os.makedirs(path, exist_ok=True)
    print(f"📂 Created directory: {path}")


def prep_images(pil_images, device):
    """
    Preprocess PIL images for BLIP model
    """
    from torchvision import transforms

    transform = transforms.Compose([
        transforms.Resize((384, 384)),
        transforms.ToTensor(),
    ])

    tensors = [transform(img).unsqueeze(0).to(device) for img in pil_images]
    return tensors


def download_checkpoint():
    print("⚠️ Please download model checkpoint manually and put it in './checkpoints/model_large_caption.pth'")
  
