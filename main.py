import os
import cv2


# get the media dimensions
def get_media_dimensions(media_path):
    cap = cv2.VideoCapture(media_path)
    if not cap.isOpened():
        cap.release()
        raise ValueError(f"Could not open media file: {media_path}")

    media_width, media_height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )
    cap.release()

    return media_width, media_height


# get the new height based on the width and height percentage
def get_new_height(media_width, media_height, width=100, height_percentage=1):
    ratio = (media_height * height_percentage) / media_width
    return int(width * ratio)


# turn video to jpg frames
def to_frames(video, frames_path):
    os.makedirs(frames_path, exist_ok=True)

    cap = cv2.VideoCapture(video)
    if not cap.isOpened():
        print(f"Error: Could not open video {video}")
        return

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        img_path = os.path.join(frames_path, f"{frame_count}.jpg")
        cv2.imwrite(img_path, frame)
        frame_count += 1

    cap.release()
    print(f"Extracted {frame_count} frames from '{video}'")


# quatize color to the n color i.e from 16bit to nbit color
def quantize_pixel(color, n=8):
    levels = n - 1
    return int(color * levels / 255) * (255 // levels)


def rgb_to_grayscale(r, g, b):
    # luminance coefficients ITU-R BT.601
    return int(0.299 * r + 0.587 * g + 0.114 * b)


def quantize_color(r, g, b, n=8, grayscale=False):
    if grayscale:
        gray = rgb_to_grayscale(r, g, b)
        r = g = b = gray
    return (quantize_pixel(r, n), quantize_pixel(g, n), quantize_pixel(b, n))


def quantize_image(pixels, width, height, n=8, grayscale=False):
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y][:3]
            pixels[x, y] = quantize_color(r, g, b, n, grayscale)


# adjust_height_percentage scales height based on the width of the image to maintain the aspect ratio
def resize_image(image, new_width=100, adjust_height_percentage=1):
    width, height = image.size
    new_height = get_new_height(width, height, new_width, adjust_height_percentage)
    resized_image = image.resize((new_width, new_height))
    return resized_image


def to_ascii(pixels, width, height, ascii_chars="  .:-=+*#%@"):
    line = ""
    for y in range(height):
        for x in range(width):
            gray = pixels[x, y][0]
            line += ascii_chars[gray * len(ascii_chars) // 256]
        line += "\n"
    return line
