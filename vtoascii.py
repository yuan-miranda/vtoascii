import os
import argparse
from PIL import Image
import time
from main import (
    to_frames,
    resize_image,
    quantize_image,
    to_ascii,
    get_media_dimensions,
    get_new_height,
)

FILE_NAME = None
WIDTH = 32
HEIGHT_PERCENTAGE = 0.38
BIT_DEPTH = 8


def main():
    global WIDTH, HEIGHT_PERCENTAGE, BIT_DEPTH, FILE_NAME

    parser = argparse.ArgumentParser(description="Convert video to ASCII animation.")

    # positional
    parser.add_argument(
        "pos_file_name",
        nargs="?",
    )
    parser.add_argument(
        "pos_width",
        nargs="?",
        type=int,
    )
    parser.add_argument(
        "pos_height_percentage",
        nargs="?",
        type=float,
    )
    parser.add_argument(
        "pos_bit_depth",
        nargs="?",
        type=int,
    )

    # optional
    parser.add_argument(
        "-f",
        "--file",
        help="Specify the video file to convert.",
    )
    parser.add_argument(
        "-w",
        "--width",
        type=int,
        help="Width of the ASCII animation (default: 32).",
    )
    parser.add_argument(
        "-p",
        "--height-percentage",
        type=float,
        help="Height percentage relative to width (default: 0.38).",
    )
    parser.add_argument(
        "-b",
        "--bit-depth",
        type=int,
        help="Bit depth for color quantization (default: 8).",
    )

    args = parser.parse_args()
    FILE_NAME = args.pos_file_name or args.file
    WIDTH = args.pos_width or args.width or WIDTH
    HEIGHT_PERCENTAGE = (
        args.pos_height_percentage or args.height_percentage or HEIGHT_PERCENTAGE
    )
    BIT_DEPTH = args.pos_bit_depth or args.bit_depth or BIT_DEPTH

    print(
        r"""
         __                             .__.__ 
___  ___/  |_  _________    ______ ____ |__|__|
\  \/ /\   __\/  _ \__  \  /  ___// ___\|  |  |
 \   /  |  | (  <_> ) __ \_\___ \\  \___|  |  |
  \_/   |__|  \____(____  /____  >\___  >__|__|
                        \/     \/     \/       
        Convert video to ASCII animation
"""
    )

    if FILE_NAME is None:
        try:
            files = os.listdir("media")

            if not files:
                raise FileNotFoundError("No files found in /media directory.")
        except FileNotFoundError:
            os.makedirs("media", exist_ok=True)
            return print(
                "No files found in /media directory. Please add a video file to convert."
            )

        print("Available files in /media directory:")
        for i, file in enumerate(files):
            print(f"{i}: {file}")

        try:
            choice = int(input("> "))
            if choice < 0 or choice >= len(files):
                raise ValueError()

            time.sleep(0.5)
            FILE_NAME = files[choice]
        except ValueError:
            return print(
                f"Invalid or out of range. Selection must be between 0 and {len(files) - 1}."
            )

        try:
            width_input = input(f"Width Length (default: {WIDTH}):\n> ").strip()
            if width_input:
                WIDTH = int(width_input)
                if WIDTH <= 0:
                    raise ValueError("Width must be positive")
        except ValueError:
            print(f"Invalid width. Using default: {WIDTH}")

        try:
            height_input = input(
                f"Height Percentage (defualt: {HEIGHT_PERCENTAGE}):\n> "
            ).strip()
            if height_input:
                HEIGHT_PERCENTAGE = float(height_input)
                if HEIGHT_PERCENTAGE <= 0:
                    raise ValueError("Height percentage must be positive")
        except ValueError:
            print(f"Invalid height percentage. Using default: {HEIGHT_PERCENTAGE}")

        try:
            bit_input = input(f"Bit Depth (default: {BIT_DEPTH}bit):\n> ").strip()
            if bit_input:
                BIT_DEPTH = int(bit_input)
                if BIT_DEPTH <= 0:
                    raise ValueError("Bit depth must be positive")
        except ValueError:
            print(f"Invalid bit depth. Using default: {BIT_DEPTH}bit")

    if not os.path.exists(os.path.join("media", FILE_NAME)):
        return print(f"{FILE_NAME} does not exist.")

    file_base_name = os.path.splitext(FILE_NAME)[0]
    media_path = os.path.join("media", FILE_NAME)

    media_width, media_height = get_media_dimensions(media_path)
    new_height = get_new_height(media_width, media_height, WIDTH, HEIGHT_PERCENTAGE)
    file_base_name = f"{file_base_name}_{WIDTH}x{new_height}_{BIT_DEPTH}bit"

    output_path = os.path.join("output", file_base_name)
    frames_path = os.path.join(output_path, "frames")

    time_start = time.time()

    print(f"\nConverting '{FILE_NAME}' to video frames...")
    to_frames(media_path, frames_path)
    frames = sorted(os.listdir(frames_path), key=lambda x: int(os.path.splitext(x)[0]))

    # resize image
    print(f"Resizing {len(frames)} frames to {WIDTH}x{new_height}...")
    for i in frames:
        img = resize_image(Image.open(f"{frames_path}/{i}"), WIDTH, HEIGHT_PERCENTAGE)
        img.save(f"{frames_path}/{i}")

    # quantize image to 8 bit grayscale
    print(f"Quantizing {len(frames)} frames to {BIT_DEPTH}bit grayscale...")
    for i in frames:
        img = Image.open(f"{frames_path}/{i}")
        width, height = img.size
        quantize_image(img.load(), width, height, grayscale=True)
        img.save(f"{frames_path}/{i}")

    # Convert frames to ascii
    print(f"Converting {len(frames)} frames to ASCII animation...")
    txt_path = os.path.join(output_path, f"{file_base_name}.txt")
    with open(txt_path, "w") as f:
        for i in frames:
            img = Image.open(f"{frames_path}/{i}")
            width, height = img.size
            ascii_img = to_ascii(img.load(), width, height)
            f.write(ascii_img)
            f.write("END\n")

    print(
        f"Converted video frames to ascii animation in {time.time() - time_start:.2f} seconds"
    )


if __name__ == "__main__":
    main()
