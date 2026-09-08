<h1 align="center">🎬 Timelapse Creator</h1>

<p align="center">
  <em>Macht aus einem Ordner voller Fotos ein Zeitraffer-Video — für Pflanzenwachstum, Baustellen, Wetter oder andere langsame Prozesse.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV">
  <img src="https://img.shields.io/badge/License-MIT-4A5568?style=for-the-badge" alt="MIT-Lizenz">
</p>

<p align="center">
  <a href="README.md">🇬🇧 English version</a>
</p>

---

## 📖 Über das Projekt

Ein Kommandozeilen-Tool aus einer einzigen Datei, das eine Fotoserie zu einem
Zeitraffer-Video zusammensetzt. Du gibst einen Ordner an und bekommst ein MP4
zurück.

Die Bilder werden alphabetisch sortiert — chronologisch benannte Dateien landen
also von selbst in der richtigen Reihenfolge. Unterschiedliche Auflösungen sind
kein Problem: Jedes Bild wird auf eine gemeinsame Größe skaliert, damit das Video
ruhig läuft statt zwischen Formaten zu springen.

## 🛠️ Tech-Stack

| Technologie | Version | Zweck |
|-------------|---------|-------|
| <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"> Python | 3.8+ | Laufzeitumgebung |
| <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white" alt="OpenCV"> opencv-python | 4.8+ | Bilder lesen, skalieren, Video kodieren |

## ✨ Funktionen

- **Sechs Eingabeformate** — `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tiff`
- **Drei Ausgabeformate** — MP4, AVI und MKV
- **Automatischer Auflösungsabgleich** — skaliert jedes Bild auf die größte gefundene Auflösung
- **FPS oder Sekunden pro Bild** — leg das Tempo so fest, wie es dir leichter fällt
- **Chronologische Sortierung** — Bilder werden nach Dateiname sortiert, Duplikate entfernt
- **Keine Konfiguration nötig** — sinnvolle Standardwerte, alles per Flag überschreibbar

## 🚀 Erste Schritte

### Voraussetzungen

- Python 3.8 oder neuer
- pip

### Installation

```bash
git clone https://github.com/cooolinho/python-timelapse-creator.git
cd python-timelapse-creator
pip install -r requirements.txt
```

## 📋 Verwendung

Alle Befehle werden im Projektordner ausgeführt. Nutze `python3`, falls `python`
nicht in deinem PATH liegt.

```bash
# Standard: 24fps MP4, ./photos -> ./output
python3 timelapse.py

# Eigene Bildrate
python3 timelapse.py --fps 12

# 0,5 Sekunden pro Bild (= 2fps)
python3 timelapse.py --duration 0.5

# Eigene Ein- und Ausgabeordner
python3 timelapse.py -i ./meine_fotos -o ./mein_video

# Full HD erzwingen
python3 timelapse.py --resolution 1920x1080

# Alles zusammen
python3 timelapse.py -i ./photos -o ./output --fps 12 --format mp4 \
  --resolution 1920x1080 --filename wachstum
```

### Parameter

| Argument | Beschreibung | Standard |
|----------|--------------|----------|
| `--input` / `-i` | Eingabeordner mit den Fotos | `./photos` |
| `--output` / `-o` | Ausgabeordner | `./output` |
| `--fps` | Bilder pro Sekunde | `24` |
| `--duration` | Sekunden pro Bild (überschreibt `--fps`) | — |
| `--format` | `mp4`, `avi` oder `mkv` | `mp4` |
| `--resolution` | `BREITExHÖHE` oder `original` | `original` |
| `--filename` | Dateiname der Ausgabe, ohne Endung | `timelapse` |

### Die richtige Bildrate wählen

Höhere FPS bedeutet einen schnelleren Zeitraffer. Bei stündlichen Fotos
(24 Bilder = ein Tag):

| Einstellung | Video pro Tag Aufnahme |
|-------------|------------------------|
| `--fps 24` | 1 Sekunde |
| `--fps 12` | 2 Sekunden |
| `--fps 4` | 6 Sekunden |

### Tipps

- **Benenne die Bilder chronologisch** — z.B. `2024-08-31_12-00.jpg`. Die Dateien
  werden alphabetisch sortiert, Zeitstempel im Namen sortieren sich damit von selbst
  richtig.
- **Gemischte Auflösungen sind kein Problem** — mit `original` werden alle Bilder
  auf die größte gefundene Auflösung hochskaliert.

## 📁 Projektstruktur

```
python-timelapse-creator/
├── timelapse.py          # Das komplette Tool
├── requirements.txt      # Abhängigkeiten
├── photos/               # Hier kommen deine Fotos hinein
└── output/               # Hier werden die Videos abgelegt
```

## 📄 Lizenz

Veröffentlicht unter der [MIT-Lizenz](LICENSE).
