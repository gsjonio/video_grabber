---
layout: page
title: Installation
---

# Installation Guide

## Prerequisites

Before installing vidgrab, make sure you have:

### Python 3.11+

[Download from python.org](https://www.python.org/downloads/)

Check your version:

```bash
python --version
```

### ffmpeg

Required to merge video and audio streams.

<details>
<summary><strong>Windows</strong></summary>

```bash
winget install ffmpeg
```

Or download from [ffmpeg.org](https://ffmpeg.org/download.html)

</details>

<details>
<summary><strong>macOS</strong></summary>

```bash
brew install ffmpeg
```

</details>

<details>
<summary><strong>Linux (Debian/Ubuntu)</strong></summary>

```bash
sudo apt install ffmpeg
```

</details>

---

## Installation Methods

### 1. Via pip (Recommended)

The simplest way to install:

```bash
pip install vidgrab
vidgrab --version
```

**Update:**

```bash
pip install --upgrade vidgrab
```

### 2. Via pipx (Isolated)

For isolated environment (no conflicts with other packages):

```bash
pipx install vidgrab
```

### 3. Via Docker

No need to install Python or ffmpeg locally:

```bash
# Build image
docker build -t vidgrab .

# Use it
docker run -v /your/directory:/data vidgrab https://youtu.be/dQw4w9WgXcQ
```

### 4. From Source (Development)

For development or latest code:

```bash
git clone https://github.com/gsjonio/video_grabber.git
cd video_grabber
poetry install
poetry run vidgrab --help
```

### 5. Automated Installers

**Linux/macOS:**

```bash
bash scripts/install.sh
```

**Windows:**

```bash
scripts/install.bat
```

These check for Python 3.11+ and ffmpeg, then install via pip.

---

## Verify Installation

```bash
vidgrab --version
# → vidgrab 1.0.2

vidgrab --help
# → Show all options
```

---

## Configuration (Optional)

Create personal defaults at `~/.config/vidgrab/config.toml`:

```toml
output     = "~/Videos/raw"
workers    = 5
max_height = 1080
```

[Full config guide →](usage.md#configuration)

---

## Troubleshooting

### Command not found: vidgrab

Make sure the pip install location is in your PATH:

```bash
# Add to PATH if needed
export PATH="$HOME/.local/bin:$PATH"
```

### FFmpeg not found

If vidgrab can't find ffmpeg, verify installation:

```bash
ffmpeg -version
```

And add it to PATH if needed.

### Python version error

vidgrab requires Python 3.11 or higher:

```bash
python --version
python3.11 --version  # Try explicit version
```

---

## Next Steps

- [Usage & Examples →](usage.md)
- [All Features →](features.md)
- [GitHub →](https://github.com/gsjonio/video_grabber)
