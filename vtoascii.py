import sys
import os
from PIL import Image
import time
from main import to_frames, resize_image, quantize_image, to_ascii

WIDTH = 32*2
HEIGHT_PERCENTAGE = 0.38
BIT_DEPTH = 8
FILE = None

def main():
    global FILE
    if FILE is None:
        filenames = os.listdir("media")
        for i, filename in enumerate(filenames):
            print(f"{i}: {filename}")
        
        choice = int(input("> "))
        time.sleep(0.5)
        FILE = filenames[choice]

    output_path = f"output/{os.path.splitext(FILE)[0]}"
    output_path_frames = f"output/{os.path.splitext(FILE)[0]}/frames"

    os.makedirs(output_path_frames, exist_ok=True)

    time_start = time.time()

    to_frames(f"media/{FILE}", output_path_frames)
    frames = sorted(os.listdir(output_path_frames), key=lambda x: int(os.path.splitext(x)[0]))

    # resize image
    for i in frames:
        img = Image.open(f"{output_path_frames}/{i}")
        img = resize_image(img, WIDTH, HEIGHT_PERCENTAGE)
        img.save(f"{output_path_frames}/{i}")

    # quantize image to 8 bit color
    for i in frames:
        img = Image.open(f"{output_path_frames}/{i}")
        width, height = img.size
        pixels = img.load()
        quantize_image(pixels, width, height, grayscale=True)
        img.save(f"{output_path_frames}/{i}")
    
    for i in frames:
        img = Image.open(f"{output_path_frames}/{i}")
        width, height = img.size
        ascii_img = to_ascii(img.load(), width, height)
        with open(f"{output_path}/{os.path.splitext(FILE)[0]}.txt", "a") as f:
            f.write(ascii_img)
            f.write("END\n")

    print(f"Converted frames to ascii in {time.time() - time_start:.2f} seconds")

if __name__ == "__main__":
    main()