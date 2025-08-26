import utils
import torch
from pathlib import Path
from models.blip import blip_decoder
from tqdm import tqdm
import argparse
import numpy as np


def init_parser():
    parser = argparse.ArgumentParser(description="Image Captioning CLI")
    parser.add_argument(
        "-i", "--input",
        help="Input directory path containing images, e.g., ./images"
    )
    parser.add_argument(
        "-b", "--batch",
        help="Batch size",
        default=1,
        type=int
    )
    parser.add_argument(
        "-p", "--paths",
        help="Text file (.txt) containing image paths (one per line)"
    )
    parser.add_argument(
        "-g", "--gpu-id",
        type=int,
        default=0,
        help="GPU device id (0,1,2...). Defaults to CPU if unavailable."
    )
    return parser


def init_model(device):
    print("Checkpoint loading...")
    model = blip_decoder(
        pretrained="./checkpoints/model_large_caption.pth",
        image_size=384,
        vit="large"
    )
    model.eval()
    model = model.to(device)
    print(f"\n✅ Model loaded on {device}")
    return model


if __name__ == "__main__":

    parser = init_parser()
    opt = parser.parse_args()

    device = torch.device(f"cuda:{opt.gpu_id}" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    if opt.paths:
        if not Path(opt.paths).is_file():
            raise FileNotFoundError(f"{opt.paths} not found!")
        with open(opt.paths, "r") as file:
            list_of_images = [line.strip() for line in file if line.strip()]
    elif opt.input:
        if not Path(opt.input).is_dir():
            raise FileNotFoundError(f"Input directory {opt.input} not found!")
        list_of_images = utils.read_images_from_directory(opt.input)
    else:
        parser.error("❌ You must provide either --input directory (-i) or --paths file (-p).")

    if len(list_of_images) == 0:
        raise ValueError("❌ No images found to process!")

    split_size = max(1, len(list_of_images) // opt.batch)
    batches = np.array_split(list_of_images, split_size)
    print(f"Total images: {len(list_of_images)}, Batches: {len(batches)}")

    if not Path("checkpoints").is_dir():
        utils.create_dir("checkpoints")

    if not Path("checkpoints/model_large_caption.pth").is_file():
        utils.download_checkpoint()

    model = init_model(device)

    with torch.no_grad():
        print("🚀 Inference started...")
        for batch_idx, batch in tqdm(enumerate(batches), unit="batch"):
            pil_images = utils.read_with_pil(batch)
            transformed_images = utils.prep_images(pil_images, device)

            if not Path("captions").is_dir():
                utils.create_dir("captions")

            with open(f"captions/{batch_idx}_captions.txt", "w+", encoding="utf-8") as file:
                for path, image in zip(batch, transformed_images):
                    caption = model.generate(
                        image,
                        sample=False,
                        num_beams=3,
                        max_length=20,
                        min_length=5
                    )
                    file.write(path + ", " + caption[0] + "\n")

    print("\n✅ Captioning finished! Check the 'captions/' folder for results.")
