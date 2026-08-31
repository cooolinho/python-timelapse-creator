# 🌱 Timelapse Creator

Erstellt ein Zeitraffer-Video aus einer Reihe von Fotos — ideal für Pflanzenwachstum, Baustellen, Wetter oder andere langsame Prozesse.

> 🇬🇧 English version: [README.md](README.md)

## Voraussetzungen

- Python 3.8+
- pip

## Installation

```bash
cd python-timelapse-creator
pip install -r requirements.txt
```

## Verwendung

Alle Befehle werden **aus dem Projektordner** ausgeführt (`cd python-timelapse-creator`). Verwende `python3` statt `python`, falls `python` bei dir nicht verfügbar ist.

### Grundlegend

```bash
# Standard: 24fps MP4, Fotos aus ./photos -> ./output
python3 timelapse.py

# Custom FPS
python3 timelapse.py --fps 12

# 0.5 Sekunden pro Bild (= 2fps)
python3 timelapse.py --duration 0.5

# Custom Pfade
python3 timelapse.py -i ./meine_fotos -o ./mein_video

# Full-HD Auflösung erzwingen
python3 timelapse.py --resolution 1920x1080

# Alle Einstellungen
python3 timelapse.py -i ./photos -o ./output --fps 12 --format mp4 --resolution 1920x1080 --filename wachstum
```

### Parameter

| Argument | Beschreibung | Standard |
|---|---|---|
| `--input` / `-i` | Ordner mit Eingabefotos | `./photos` |
| `--output` / `-o` | Ausgabeordner | `./output` |
| `--fps` | Bilder pro Sekunde | `24` |
| `--duration` | Dauer pro Bild in Sekunden (überschreibt `--fps`) | — |
| `--format` | `mp4`, `avi`, `mkv` | `mp4` |
| `--resolution` | `WIDTHxHEIGHT` oder `original` | `original` |
| `--filename` | Name der Ausgabedatei (ohne Endung) | `timelapse` |

**Hinweis zum FPS:** Hohe FPS = schneller Zeitraffer. Bei stündlichen Fotos (24 Bilder = 1 Tag Laufzeit):
- `--fps 24` → 1 Sekunde Video pro Tag
- `--fps 12` → 2 Sekunden Video pro Tag
- `--fps 4` → 6 Sekunden Video pro Tag

### Tipps

- **Bildbenennung**: Fotos sollten chronologisch benannt werden (z.B. `2024-08-31_12-00.jpg`, `2024-08-31_13-00.jpg`), da sie alphabetisch sortiert werden.
- **Unterstützte Formate**: `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tiff`
- **Auflösung**: Bei `original` werden alle Bilder auf die größte gefundene Auflösung skaliert, damit das Video flüssig ist.

## Projektstruktur

```
python-timelapse-creator/
├── timelapse.py          # Hauptscript
├── requirements.txt      # Abhängigkeiten
├── photos/               # Hier die Fotos ablegen
├── output/               # Hier werden die Videos gespeichert
└── README.md             # Diese Datei
```
