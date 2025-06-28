import os
import time
import argparse
from main import get_platform

FILE_BASE_NAME = None
PLATFORM = get_platform()


def clear_console():
    if PLATFORM == "windows":
        os.system("cls")
    else:
        os.system("clear")


def main():
    global FILE_BASE_NAME

    parser = argparse.ArgumentParser(description="Display ASCII animation.")

    # positional
    parser.add_argument(
        "pos_file_base_name",
        nargs="?",
    )

    # optional
    parser.add_argument(
        "-f",
        "--file",
        help="Specify the base name of the file to display.",
    )

    args = parser.parse_args()
    FILE_BASE_NAME = args.file or args.pos_file_base_name

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

    if FILE_BASE_NAME is None:
        try:
            files = os.listdir("output")

            if not files:
                raise FileNotFoundError("No files found in /output directory.")
        except FileNotFoundError:
            os.makedirs("output", exist_ok=True)
            return print(
                "No files found in /output directory. Please convert a video first."
            )

        print("Available files in /output directory:")
        for i, file in enumerate(files):
            print(f"{i}: {file}")

        try:
            choice = int(input("> "))
            if choice < 0 or choice >= len(files):
                raise ValueError()

            time.sleep(0.5)
            FILE_BASE_NAME = files[choice]
        except ValueError:
            return print(
                f"Invalid or out of range. Selection must be between 0 and {len(files) - 1}."
            )

    if not os.path.exists(os.path.join("output", FILE_BASE_NAME)):
        return print(f"{FILE_BASE_NAME} does not exist.")

    txt_path = os.path.join("output", FILE_BASE_NAME, f"{FILE_BASE_NAME}.txt")
    with open(txt_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line == "END\n":
                time.sleep(0.02)
                clear_console()
                continue

            print(line, end="")


if __name__ == "__main__":
    main()
