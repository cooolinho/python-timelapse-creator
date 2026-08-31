#!/usr/bin/env python3
"""
Timelapse Creator
=================
Erstellt ein Zeitraffer-Video aus einer Reihe von Fotos.

Verwendung:
    python timelapse.py                                  # Defaults
    python timelapse.py --fps 12 --format mp4            # 12fps MP4
    python timelapse.py --duration 0.5                   # 0.5s pro Bild
    python timelapse.py -i ./meine_fotos -o ./mein_video # Custom Pfade
    python timelapse.py --resolution 1920x1080           # Full-HD Skalierung
"""

from __future__ import annotations

import argparse
import glob
import os
import sys
from pathlib import Path

import cv2
import numpy as np


# Unterstuetzte Bildformate
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}


def parse_args():
    """Parse Kommandozeilen-Argumente."""
    parser = argparse.ArgumentParser(
        description="Erstellt ein Zeitraffer-Video aus Fotos.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  python timelapse.py                                    # Defaults: 24fps, MP4
  python timelapse.py --fps 12 --format mp4              # 12fps MP4
  python timelapse.py --duration 0.5 --format mp4        # 0.5s pro Bild = 2fps
  python timelapse.py -i ./meine_fotos -o ./mein_video   # Custom Pfade
  python timelapse.py --resolution 1920x1080             # Full-HD
  python timelapse.py --resolution original              # Originale Groesse
        """,
    )

    parser.add_argument(
        "-i",
        "--input",
        default="./photos",
        help="Ordner mit Eingabefotos (Standard: ./photos)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="./output",
        help="Ausgabeordner (Standard: ./output)",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=24,
        help="Bilder pro Sekunde / Frame-Rate (Standard: 24)",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=None,
        help="Dauer jedes Frames in Sekunden (ueberschreibt --fps)",
    )
    parser.add_argument(
        "--format",
        choices=["mp4", "avi", "mkv"],
        default="mp4",
        help="Videoformat (Standard: mp4)",
    )
    parser.add_argument(
        "--resolution",
        default="original",
        help="Zielaufloesung: WIDTHxHEIGHT oder 'original' (Standard: original)",
    )
    parser.add_argument(
        "--filename",
        default="timelapse",
        help="Name der Ausgabedatei ohne Endung (Standard: timelapse)",
    )

    return parser.parse_args()


def find_images(input_dir: str) -> list[str]:
    """Findet alle Bilder im Eingabe-Ordner, sortiert nach Name."""
    input_path = Path(input_dir)

    if not input_path.exists():
        print(f"Fehler: Eingabe-Ordner '{input_dir}' existiert nicht.")
        sys.exit(1)

    images = []
    for ext in IMAGE_EXTENSIONS:
        images.extend(input_path.glob(f"*{ext}"))
        images.extend(input_path.glob(f"*{ext.upper()}"))

    # Duplikate entfernen und sortieren
    images = sorted(set(str(p) for p in images))

    return images


def validate_images(images: list[str]) -> None:
    """Prueft ob mindestens 2 Bilder vorhanden sind."""
    if len(images) == 0:
        print("Fehler: Keine Bilder im Eingabe-Ordner gefunden.")
        print(f"Unterstuetzte Formate: {', '.join(sorted(IMAGE_EXTENSIONS))}")
        sys.exit(1)

    if len(images) < 2:
        print("Fehler: Mindestens 2 Bilder sind fuer ein Video noetig.")
        sys.exit(1)


def parse_resolution(resolution_str: str, images: list[str]) -> tuple[int, int]:
    """Parst die Aufloesung oder ermittelt die groesste gemeinsame."""
    if resolution_str.lower() == "original":
        return _find_max_resolution(images)

    try:
        width, height = resolution_str.lower().split("x")
        return int(width), int(height)
    except ValueError:
        print(f"Fehler: Ungueltige Aufloesung '{resolution_str}'.")
        print("Erwartetes Format: WIDTHxHEIGHT (z.B. 1920x1080) oder 'original'.")
        sys.exit(1)


def _find_max_resolution(images: list[str]) -> tuple[int, int]:
    """Findet die groesste Breite und Hoehe ueber alle Bilder."""
    max_width = 0
    max_height = 0

    for img_path in images:
        img = cv2.imread(img_path)
        if img is None:
            print(f"Warnung: '{img_path}' konnte nicht gelesen werden, uebersprungen.")
            continue
        h, w = img.shape[:2]
        max_width = max(max_width, w)
        max_height = max(max_height, h)

    if max_width == 0 or max_height == 0:
        print("Fehler: Keine gueltigen Bilder gefunden.")
        sys.exit(1)

    return max_width, max_height


def get_fourcc_and_ext(fmt: str) -> tuple[int, str]:
    """Gibt den Codec und die Dateiendung fuer das gewaehlte Format zurueck."""
    codecs = {
        "mp4": (cv2.VideoWriter_fourcc(*"mp4v"), ".mp4"),
        "avi": (cv2.VideoWriter_fourcc(*"MJPG"), ".avi"),
        "mkv": (cv2.VideoWriter_fourcc(*"X264"), ".mkv"),
    }

    if fmt not in codecs:
        print(f"Fehler: Videoformat '{fmt}' nicht unterstuetzt.")
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
    """Erstellt das Zeitraffer-Video."""
    width, height = resolution
    fourcc, ext = get_fourcc_and_ext(video_format)

    # Ausgabepfad vorbereiten
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    output_file = output_path / f"{filename}_{fps}fps_{width}x{height}{ext}"

    # VideoWriter initialisieren
    writer = cv2.VideoWriter(str(output_file), fourcc, fps, (width, height))

    if not writer.isOpened():
        print(f" Fehler: Video-Writer konnte nicht initialisiert werden.")
        print("Moeglicherweise fehlt der Codec. Versuche ein anderes Format.")
        sys.exit(1)

    print(f"Erstelle Zeitraffer: {len(images)} Bilder -> {fps}fps")
    print(f"Aufloesung: {width}x{height} | Format: {video_format.upper()}")
    print(f"Ausgabe: {output_file}")
    print()

    # Frames verarbeiten
    for i, img_path in enumerate(images, 1):
        # Fortschritt anzeigen
        progress = i / len(images) * 100
        bar_len = 40
        filled = int(bar_len * i / len(images))
        bar = "=" * filled + "-" * (bar_len - filled)
        print(f"\r[{bar}] {progress:5.1f}%  ({i}/{len(images)})", end="", flush=True)

        # Bild laden
        img = cv2.imread(img_path)
        if img is None:
            print(f"\nWarnung: '{img_path}' konnte nicht gelesen werden, uebersprungen.")
            continue

        # Auf Zielgroesse skalieren
        current_h, current_w = img.shape[:2]
        if current_w != width or current_h != height:
            img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

        # Frame schreiben
        writer.write(img)

    writer.release()
    print("\n")

    # Ergebnis
    file_size = output_file.stat().st_size
    size_str = _format_size(file_size)
    duration = len(images) / fps

    print(f"Fertig!")
    print(f"  Datei:      {output_file}")
    print(f"  Groesse:    {size_str}")
    print(f"  Dauer:      {duration:.1f} Sekunden ({len(images)} Frames @ {fps}fps)")
    print(f"  Aufloesung: {width}x{height}")


def _format_size(size_bytes: int) -> str:
    """Formatiert Dateigroesse menschenlesbar."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def main():
    """Hauptfunktion."""
    args = parse_args()

    # FPS bestimmen
    fps = args.fps
    if args.duration is not None:
        if args.duration <= 0:
            print("Fehler: --duration muss groesser als 0 sein.")
            sys.exit(1)
        fps = max(1, int(1 / args.duration))

    # Bilder finden
    images = find_images(args.input)
    validate_images(images)

    # Aufloesung bestimmen
    resolution = parse_resolution(args.resolution, images)

    # Zeitraffer erstellen
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
