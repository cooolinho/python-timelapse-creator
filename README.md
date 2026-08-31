# 🌱 Timelapse Creator

Creates a timelapse video from a series of photos — ideal for plant growth, construction sites, weather, or other slow processes.

> 🇩🇪 Deutsche Version: [README.de.md](README.de.md)

## Requirements

- Python 3.8+
- pip

## Installation

```bash
cd python-timelapse-creator
pip install -r requirements.txt
```

## Usage

All commands are run **from the project folder** (`cd python-timelapse-creator`). Use `python3` instead of `python` if `python` is not available on your system.

### Basic

```bash
# Default: 24fps MP4, photos from ./photos -> ./output
python3 timelapse.py

# Custom FPS
python3 timelapse.py --fps 12

# 0.5 seconds per frame (= 2fps)
python3 timelapse.py --duration 0.5

# Custom paths
python3 timelapse.py -i ./my_photos -o ./my_video

# Force Full-HD resolution
python3 timelapse.py --resolution 1920x1080

# All settings
python3 timelapse.py -i ./photos -o ./output --fps 12 --format mp4 --resolution 1920x1080 --filename growth
```

### Parameters

| Argument | Description | Default |
|---|---|---|
| `--input` / `-i` | Input folder with photos | `./photos` |
| `--output` / `-o` | Output folder | `./output` |
| `--fps` | Frames per second | `24` |
| `--duration` | Duration per frame in seconds (overrides `--fps`) | — |
| `--format` | `mp4`, `avi`, `mkv` | `mp4` |
| `--resolution` | `WIDTHxHEIGHT` or `original` | `original` |
| `--filename` | Output filename (without extension) | `timelapse` |

**Note on FPS:** Higher FPS = faster timelapse. With hourly photos (24 images = 1 day of recording):
- `--fps 24` → 1 second of video per day
- `--fps 12` → 2 seconds of video per day
- `--fps 4` → 6 seconds of video per day

### Tips

- **Naming images**: Photos should be named chronologically (e.g. `2024-08-31_12-00.jpg`, `2024-08-31_13-00.jpg`), since they are sorted alphabetically.
- **Supported formats**: `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tiff`
- **Resolution**: With `original`, all images are scaled to the largest resolution found, so the video stays smooth.

## Project structure

```
python-timelapse-creator/
├── timelapse.py          # Main script
├── requirements.txt      # Dependencies
├── photos/               # Put your photos here
├── output/               # Videos are saved here
└── README.md             # This file
```
