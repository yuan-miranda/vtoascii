import sys
import os
import time

FILE_BASE_NAME = None


def clear_console():
    if sys.platform.startswith("win"):
        _ = os.system("cls")
    else:
        _ = os.system("clear")


def main():
    global FILE_BASE_NAME
    if len(sys.argv) > 1:
        FILE_BASE_NAME = sys.argv[1]
    elif FILE_BASE_NAME is None:
        try:
            files = os.listdir("output")

            if not files:
                raise FileNotFoundError("No files found in /output directory.")
        except FileNotFoundError:
            os.makedirs("output", exist_ok=True)
            return print(
                "No files found in /output directory. Please convert a video first."
            )

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
                time.sleep(0.03)
                clear_console()
                continue

            print(line, end="")


if __name__ == "__main__":
    main()
