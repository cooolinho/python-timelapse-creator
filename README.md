<h1 align="center">🎬 Timelapse Creator</h1>

<p align="center">
  <em>Turn a folder of photos into a timelapse video — for plant growth, construction sites, weather, or any slow process.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV">
  <img src="https://img.shields.io/badge/License-MIT-4A5568?style=for-the-badge" alt="MIT License">
</p>

<p align="center">
  <a href="README.de.md">🇩🇪 Deutsche Version</a>
</p>

---

## 📖 About

A single-file command line tool that stitches a series of photos into a timelapse
video. Point it at a folder, get an MP4 back.

It sorts images alphabetically, so chronologically named files fall into the right
order on their own. Mixed resolutions are handled automatically — every frame is
scaled to a common size so the video stays smooth instead of jittering between
dimensions.

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"> Python | 3.8+ | Runtime |
| <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white" alt="OpenCV"> opencv-python | 4.8+ | Image reading, scaling, video encoding |

## ✨ Features

- **Six input formats** — `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tiff`
- **Three output formats** — MP4, AVI and MKV
- **Automatic resolution matching** — scales every frame to the largest resolution found
- **FPS or seconds per frame** — set the pace whichever way is more natural
- **Chronological sorting** — images are sorted by filename, duplicates removed
- **No configuration** — sensible defaults, everything overridable by flag

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or newer
- pip

### Installation

```bash
git clone https://github.com/cooolinho/python-timelapse-creator.git
cd python-timelapse-creator
pip install -r requirements.txt
```

## 📋 Usage

Run all commands from the project folder. Use `python3` if `python` is not on your
PATH.

```bash
# Default: 24fps MP4, ./photos -> ./output
python3 timelapse.py

# Custom frame rate
python3 timelapse.py --fps 12

# 0.5 seconds per frame (= 2fps)
python3 timelapse.py --duration 0.5

# Custom input and output folders
python3 timelapse.py -i ./my_photos -o ./my_video

# Force Full HD
python3 timelapse.py --resolution 1920x1080

# Everything at once
python3 timelapse.py -i ./photos -o ./output --fps 12 --format mp4 \
  --resolution 1920x1080 --filename growth
```

### Parameters

| Argument | Description | Default |
|----------|-------------|---------|
| `--input` / `-i` | Input folder with photos | `./photos` |
| `--output` / `-o` | Output folder | `./output` |
| `--fps` | Frames per second | `24` |
| `--duration` | Seconds per frame (overrides `--fps`) | — |
| `--format` | `mp4`, `avi` or `mkv` | `mp4` |
| `--resolution` | `WIDTHxHEIGHT` or `original` | `original` |
| `--filename` | Output filename, without extension | `timelapse` |

### Choosing a frame rate

Higher FPS means a faster timelapse. With hourly photos (24 images = one day):

| Setting | Video per day of footage |
|---------|--------------------------|
| `--fps 24` | 1 second |
| `--fps 12` | 2 seconds |
| `--fps 4` | 6 seconds |

### Tips

- **Name images chronologically** — e.g. `2024-08-31_12-00.jpg`. Files are sorted
  alphabetically, so timestamped names sort themselves correctly.
- **Mixed resolutions are fine** — with `original`, all frames are scaled up to the
  largest resolution found.

## 📁 Project Structure

```
python-timelapse-creator/
├── timelapse.py          # The entire tool
├── requirements.txt      # Dependencies
├── photos/               # Put your photos here
└── output/               # Videos are written here
```

## 📄 License

Released under the [MIT License](LICENSE).
