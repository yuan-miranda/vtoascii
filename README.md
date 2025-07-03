# Video to Ascii (vtoascii)

A Python script used in [nascii](https://github.com/yuan-miranda/nascii), a Discord bot that turns videos into ASCII animation. Given a video file in `./media`, the script processes each frame and converts it into a text-based representation using a predefined gradient of characters.

It maps pixel brightness to the character set `  .:-=+*#%@`, ordered from lowest to highest visual density.

https://github.com/user-attachments/assets/e929bbb1-a114-4e14-8402-d2b11c94934b

[sauce](https://youtu.be/H-4ITUCEWc4?si=MvjU480WidaAQczT)

## Install

Clone the repository and install the dependencies

```
git clone https://github.com/yuan-miranda/vtoascii.git
```

```
cd vtoascii
```

```
pip install -r requirements.txt
```

## Usage

### For a generic help page

```
python .\vtoascii.py --help
```

### Convert video to ASCII animation (prompt-based)

```
python .\vtoascii.py
```

Inline video file name from `./media`

```
python .\vtoascii.py "video.mp4"
```

Tweak the output with this parameters

```
python .\vtoascii.py --file="video.mp4" --width=64 --height-percentage=1 --bit-depth=16
```

Or using positional arguments

```
python .\vtoascii.py "video.mp4" 64 1 16
```

### Play the ASCII animation (prompt-based)

```
python .\player.py
```

Inline file base name from `./output`

```
python .\player.py "video"
```

## Contributing

PRs accepted.
