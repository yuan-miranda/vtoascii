import sys
import os
from PIL import Image
import time
from main import to_frames, resize_image, quantize_image, to_ascii

WIDTH = 64
HEIGHT_PERCENTAGE = 0.38
BIT_DEPTH = 8
FILE_NAME = None


def main():
    global FILE_NAME
    if len(sys.argv) > 1:
        FILE_NAME = sys.argv[1]
    elif FILE_NAME is None:
        files = os.listdir("media")
        if not files:
            return print("No files found in /media directory.")

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

    if not os.path.exists(os.path.join("media", FILE_NAME)):
        return print(f"{FILE_NAME} does not exist.")

    file_base_name = os.path.splitext(FILE_NAME)[0]
    if os.path.exists(os.path.join("output", file_base_name)):
        return print(f"{file_base_name} already converted.")

    media_path = os.path.join("media", FILE_NAME)
    output_path = os.path.join("output", file_base_name)
    frames_path = os.path.join(output_path, "frames")
    os.makedirs(frames_path, exist_ok=True)

    time_start = time.time()

    to_frames(media_path, frames_path)
    frames = sorted(os.listdir(frames_path), key=lambda x: int(os.path.splitext(x)[0]))

    # resize image
    for i in frames:
        img = Image.open(f"{frames_path}/{i}")
        img = resize_image(img, WIDTH, HEIGHT_PERCENTAGE)
        img.save(f"{frames_path}/{i}")

    # quantize image to 8 bit color
    for i in frames:
        img = Image.open(f"{frames_path}/{i}")
        width, height = img.size
        pixels = img.load()
        quantize_image(pixels, width, height, grayscale=True)
        img.save(f"{frames_path}/{i}")

    txt_path = os.path.join(output_path, f"{file_base_name}.txt")
    with open(txt_path, "w") as f:
        for i in frames:
            img = Image.open(f"{frames_path}/{i}")
            width, height = img.size
            ascii_img = to_ascii(img.load(), width, height)
            f.write(ascii_img)
            f.write("END\n")

    print(f"Converted frames to ascii in {time.time() - time_start:.2f} seconds")


if __name__ == "__main__":
    main()
