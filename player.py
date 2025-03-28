import sys
import os
import time

def clear_console():
    if sys.platform.startswith('win'):
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def main():
    filenames = os.listdir("output")
    for i, filename in enumerate(filenames):
        print(f"{i}: {filename}")

    choice = int(input("> "))
    time.sleep(0.5)
    filename = filenames[choice]
    filename = os.path.join("output", filename, f"{os.path.splitext(filename)[0]}.txt")

    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line == "END\n":
                time.sleep(0.03)
                clear_console()
                continue

            print(line, end="")

if __name__ == "__main__":
    main()