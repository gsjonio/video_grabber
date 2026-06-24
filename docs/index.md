---
layout: home
---

# vidgrab

## Download YouTube videos at maximum quality for video editing

> Don't re-encode. Download DASH streams separately and mux in copy mode — zero quality loss.

---

## Why vidgrab?

Most download tools apply re-encoding to merge video and audio, degrading quality and wasting time. vidgrab is different:

```text
YouTube  →  video stream (H.264 / VP9 / AV1)  ─┐
         →  audio stream (AAC / Opus)           ─┴→  FFmpeg mux  →  final file (copy mode)
```

**No transcoding. No quality loss.**

---

## Quick Start

```bash
# Install
pip install vidgrab

# Download in maximum quality
vidgrab https://youtu.be/dQw4w9WgXcQ

# Inspect before downloading
vidgrab https://youtu.be/dQw4w9WgXcQ --dry-run

# Batch download with 5 workers
vidgrab --batch urls.txt --workers 5

# Limit to 1080p
vidgrab https://youtu.be/dQw4w9WgXcQ --max-height 1080
```

---

## ✨ Features

- ⚡ **Parallel downloads** — Up to 8 simultaneous
- 🔁 **Smart retry** — Exponential backoff on rate-limits
- 🔍 **Dry run** — Preview before downloading
- 📋 **Batch** — Download from `.txt` file
- 🎬 **Playlists** — Expand and download all videos
- 📁 **Smart skip** — Auto-detect existing files
- 📄 **Metadata** — Save JSON sidecar with video info
- 🔒 **Age-gated** — Cookie support for restricted videos
- ⚙️ **Config** — Personal defaults in `~/.config/vidgrab/config.toml`

---

## Install

**Via pip (recommended):**

```bash
pip install vidgrab
```

**Via pipx (isolated):**

```bash
pipx install vidgrab
```

**Via Docker:**

```bash
docker build -t vidgrab .
docker run -v /downloads:/data vidgrab https://youtu.be/dQw4w9WgXcQ
```

**Automated scripts:**

- Linux/macOS: `bash scripts/install.sh`
- Windows: `scripts/install.bat`

[See full installation guide →](installation.md)

---

## Documentation

- 📖 [Installation & Setup](installation.md)
- 💻 [Usage & Examples](usage.md)
- ✨ [Features Overview](features.md)
- 🤝 [Contributing Guide](contributing.md)
- 📋 [Changelog](changelog.md)

---

## Requirements

- **Python 3.11+**
- **ffmpeg** — For merging streams
- **yt-dlp** — Installed automatically

---

## Project Status

🎉 **v1.0.2** — Production-ready  
✅ **93% test coverage** (123 tests)  
✅ **Pylint 10/10** · **Mypy strict** · **100% type-checked**

[View on GitHub](https://github.com/gsjonio/video_grabber)  
[View on PyPI](https://pypi.org/project/vidgrab/)
