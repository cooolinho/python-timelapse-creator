#!/usr/bin/env python3
"""
Timelapse Creator
=================
Creates a timelapse video from a series of photos.

Usage:
    python3 timelapse.py                                    # Defaults
    python3 timelapse.py --fps 12 --format mp4              # 12fps MP4
    python3 timelapse.py --duration 0.5                     # 0.5s per frame
    python3 timelapse.py -i ./my_photos -o ./my_video       # Custom paths
    python3 timelapse.py --resolution 1920x1080             # Force Full-HD
"""

from __future__ import annotations

import argparse
import glob
import os
import sys
from pathlib import Path

import cv2
import numpy as np


# Supported image formats
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Creates a timelapse video from photos.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 timelapse.py                                    # Defaults: 24fps, MP4
  python3 timelapse.py --fps 12 --format mp4              # 12fps MP4
  python3 timelapse.py --duration 0.5 --format mp4        # 0.5s per frame = 2fps
  python3 timelapse.py -i ./my_photos -o ./my_video       # Custom paths
  python3 timelapse.py --resolution 1920x1080             # Force Full-HD
  python3 timelapse.py --resolution original              # Original size
        """,
    )

    parser.add_argument(
        "-i",
        "--input",
        default="./photos",
        help="Input folder with photos (default: ./photos)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="./output",
        help="Output folder (default: ./output)",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=24,
        help="Frames per second / frame rate (default: 24)",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=None,
        help="Duration of each frame in seconds (overrides --fps)",
    )
    parser.add_argument(
        "--format",
        choices=["mp4", "avi", "mkv"],
        default="mp4",
        help="Video format (default: mp4)",
    )
    parser.add_argument(
        "--resolution",
        default="original",
        help="Target resolution: WIDTHxHEIGHT or 'original' (default: original)",
    )
    parser.add_argument(
        "--filename",
        default="timelapse",
        help="Output filename without extension (default: timelapse)",
    )

    return parser.parse_args()


def find_images(input_dir: str) -> list[str]:
    """Find all images in the input folder, sorted by name."""
    input_path = Path(input_dir)

    if not input_path.exists():
        print(f"Error: Input folder '{input_dir}' does not exist.")
        sys.exit(1)

    images = []
    for ext in IMAGE_EXTENSIONS:
        images.extend(input_path.glob(f"*{ext}"))
        images.extend(input_path.glob(f"*{ext.upper()}"))

    # Deduplicate and sort
    images = sorted(set(str(p) for p in images))

    return images


def validate_images(images: list[str]) -> None:
    """Check that at least 2 images are present."""
    if len(images) == 0:
        print("Error: No images found in the input folder.")
        print(f"Supported formats: {', '.join(sorted(IMAGE_EXTENSIONS))}")
        sys.exit(1)

    if len(images) < 2:
        print("Error: At least 2 images are required for a video.")
        sys.exit(1)


def parse_resolution(resolution_str: str, images: list[str]) -> tuple[int, int]:
    """Parse the resolution or find the largest common one."""
    if resolution_str.lower() == "original":
        return _find_max_resolution(images)

    try:
        width, height = resolution_str.lower().split("x")
        return int(width), int(height)
    except ValueError:
        print(f"Error: Invalid resolution '{resolution_str}'.")
        print("Expected format: WIDTHxHEIGHT (e.g. 1920x1080) or 'original'.")
        sys.exit(1)


def _find_max_resolution(images: list[str]) -> tuple[int, int]:
    """Find the largest width and height across all images."""
    max_width = 0
    max_height = 0

    for img_path in images:
        img = cv2.imread(img_path)
        if img is None:
            print(f"Warning: '{img_path}' could not be read, skipping.")
            continue
        h, w = img.shape[:2]
        max_width = max(max_width, w)
        max_height = max(max_height, h)

    if max_width == 0 or max_height == 0:
        print("Error: No valid images found.")
        sys.exit(1)

    return max_width, max_height


def get_fourcc_and_ext(fmt: str) -> tuple[int, str]:
    """Return the codec and file extension for the chosen format."""
    codecs = {
        "mp4": (cv2.VideoWriter_fourcc(*"mp4v"), ".mp4"),
        "avi": (cv2.VideoWriter_fourcc(*"MJPG"), ".avi"),
        "mkv": (cv2.VideoWriter_fourcc(*"X264"), ".mkv"),
    }

    if fmt not in codecs:
        print(f"Error: Video format '{fmt}' is not supported.")
        sys.exit(1)

    return codecs[fmt]


def create_timelapse(
    images: list[str],
    output_dir: str,
    fps: int,
    resolution: tuple[int, int],
    video_format: str,
    filename: str,
) -> None:
    """Create the timelapse video."""
    width, height = resolution
    fourcc, ext = get_fourcc_and_ext(video_format)

    # Prepare the output path
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    output_file = output_path / f"{filename}_{fps}fps_{width}x{height}{ext}"

    # Initialize the video writer
    writer = cv2.VideoWriter(str(output_file), fourcc, fps, (width, height))

    if not writer.isOpened():
        print("Error: Could not initialize the video writer.")
        print("The codec may be missing. Try a different format.")
        sys.exit(1)

    print(f"Creating timelapse: {len(images)} images -> {fps}fps")
    print(f"Resolution: {width}x{height} | Format: {video_format.upper()}")
    print(f"Output: {output_file}")
    print()

    # Process frames
    for i, img_path in enumerate(images, 1):
        # Show progress
        progress = i / len(images) * 100
        bar_len = 40
        filled = int(bar_len * i / len(images))
        bar = "=" * filled + "-" * (bar_len - filled)
        print(f"\r[{bar}] {progress:5.1f}%  ({i}/{len(images)})", end="", flush=True)

        # Load image
        img = cv2.imread(img_path)
        if img is None:
            print(f"\nWarning: '{img_path}' could not be read, skipping.")
            continue

        # Resize to target size
        current_h, current_w = img.shape[:2]
        if current_w != width or current_h != height:
            img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

        # Write frame
        writer.write(img)

    writer.release()
    print("\n")

    # Result
    file_size = output_file.stat().st_size
    size_str = _format_size(file_size)
    duration = len(images) / fps

    print("Done!")
    print(f"  File:       {output_file}")
    print(f"  Size:       {size_str}")
    print(f"  Duration:   {duration:.1f} seconds ({len(images)} frames @ {fps}fps)")
    print(f"  Resolution: {width}x{height}")


def _format_size(size_bytes: int) -> str:
    """Format file size in a human-readable way."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def main():
    """Main entry point."""
    args = parse_args()

    # Determine fps
    fps = args.fps
    if args.duration is not None:
        if args.duration <= 0:
            print("Error: --duration must be greater than 0.")
            sys.exit(1)
        fps = max(1, int(1 / args.duration))

    # Find images
    images = find_images(args.input)
    validate_images(images)

    # Determine resolution
    resolution = parse_resolution(args.resolution, images)

    # Create timelapse
    create_timelapse(
        images=images,
        output_dir=args.output,
        fps=fps,
        resolution=resolution,
        video_format=args.format,
        filename=args.filename,
    )


if __name__ == "__main__":
    main()
