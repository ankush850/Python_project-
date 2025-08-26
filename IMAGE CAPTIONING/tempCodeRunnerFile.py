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
