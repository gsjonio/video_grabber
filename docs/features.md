---
layout: page
title: Features
---

# Features

## Core Features

### ⚡ Parallel Downloads

Download up to 8 videos simultaneously with `--workers`:

```bash
vidgrab --batch urls.txt --workers 8
```

Perfect for batch downloads. Respects rate limits automatically.

### 🔁 Smart Retry

Exponential backoff when YouTube rate-limits you:

```text
Attempt 1 → Wait 1s
Attempt 2 → Wait 2s
Attempt 3 → Wait 4s
Attempt 4 → Wait 8s
Attempt 5 → Wait 16s
```

vidgrab automatically retries up to 5 times. You never lose progress.

### 🔍 Dry Run

Preview what will be downloaded without actually downloading:

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --dry-run
```

Shows title, resolution, file size, and exact output name.

### ⏸ Auto Resume

Downloads interrupted by network issues resume from where they left off:

```bash
# Download interrupted? Just run again
vidgrab https://youtu.be/dQw4w9WgXcQ
# Resumes automatically
```

No need to restart from the beginning.

### 📁 Smart Skip

vidgrab automatically detects existing files and skips them:

```bash
vidgrab --batch urls.txt
# Already downloaded videos are skipped silently
```

To re-download anyway:

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --force
```

### 📋 Batch Download

Download from a file with one URL per line:

```bash
vidgrab --batch urls.txt --workers 5
```

**urls.txt:**

```text
# My videos (comments are ignored)
https://youtu.be/url1
https://youtu.be/url2

# Blank lines are also ignored
https://youtu.be/url3
```

### 🎬 Playlist Expansion

Download entire playlists automatically:

```bash
vidgrab "https://youtube.com/playlist?list=PLxxxx" --playlist
```

vidgrab expands the playlist and downloads all videos.

### 📄 Metadata Export

Save video metadata as JSON sidecar next to each download:

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --write-json
```

Creates `{filename}.json`:

```json
{
  "video_id": "dQw4w9WgXcQ",
  "title": "Rick Astley - Never Gonna Give You Up",
  "channel": "Rick Astley",
  "upload_date": "2009-10-25",
  "duration_seconds": 212,
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "tags": ["pop", "80s"],
  "description": "Official video..."
}
```

### 🔒 Age-Gated Videos

Download age-restricted videos using browser cookies:

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --cookies ~/cookies.txt
```

[How to export cookies →](usage.md#exporting-cookies)

### ⚙️ Configuration File

Set personal defaults to avoid repeating flags:

```toml
# ~/.config/vidgrab/config.toml
output     = "~/Videos/raw"
workers    = 5
max_height = 1080
```

CLI flags always override config.

### 🏷 Predictable Naming

All files follow the same pattern:

```text
{upload_date}-{title-slug}-{video_id}.{ext}

Example: 20240315-never-gonna-give-you-up-dQw4w9WgXcQ.mp4
```

- ✅ Chronological sorting
- ✅ Safe filenames
- ✅ Unique by video ID
- ✅ Easy to identify

### ⚠️ License Warning

vidgrab alerts you when downloading non-Creative Commons videos:

```text
⚠️  This video is not under a Creative Commons license.
   Download for personal use only.
```

---

## Quality Features

### Maximum Quality Downloads

vidgrab downloads **DASH streams separately** without re-encoding:

```text
YouTube →  video stream (H.264 / VP9 / AV1)  ─┐
        →  audio stream (AAC / Opus)           ─┴→  FFmpeg mux (copy mode)
```

**Result:** Zero quality loss, fastest possible download.

### Multiple Format Support

Automatically chooses the best container:

| Streams | Container | Use Case |
| --- | --- | --- |
| H.264 + AAC | `.mp4` | Most compatible |
| VP9/AV1 + Opus | `.mkv` | Best quality |

### Resolution Control

Limit to specific resolution if needed:

```bash
# Download up to 1080p (not higher)
vidgrab https://youtu.be/dQw4w9WgXcQ --max-height 1080

# Download up to 720p
vidgrab https://youtu.be/dQw4w9WgXcQ --max-height 720
```

---

## Developer Features

### Quiet Mode

Suppress all output except errors (great for scripts):

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --quiet
echo $? # Exit code
```

### Exit Codes

- `0` — All downloads succeeded
- `1` — At least one download failed

Perfect for shell scripts and automation.

### Shell Completion

Auto-complete in bash/zsh/fish:

```bash
vidgrab --install-completion
```

Then:
```bash
vidgrab --m[TAB]  # → --max-height
vidgrab --o[TAB]  # → --output
```

---

## Project Quality

### 93% Test Coverage

123 unit + integration tests covering:
- URL collection and batch processing
- Download orchestration
- Error handling
- CLI interface
- Configuration loading

```bash
poetry run pytest --cov=vidgrab
```

### Code Quality Standards

- **Pylint:** 10/10
- **Mypy:** Strict mode (100% type-checked)
- **Ruff:** 9 rule categories
- **Pre-commit:** Automated checks before every commit
- **CodeQL:** Security scanning on every push

### CI/CD Pipeline

- ✅ Automated testing
- ✅ Linting and type checking
- ✅ Security scanning
- ✅ Automatic releases to PyPI
- ✅ GitHub Pages documentation

---

## What's NOT Included

vidgrab is **deliberately minimal**:

- ❌ GUI/TUI (command-line only)
- ❌ Stream transcoding (copy mode only)
- ❌ Video editing (download only)
- ❌ Playlist management (expand-only)

This keeps it **fast, stable, and predictable**.

---

[← Back to Home](/) · [Usage Guide →](usage.md) · [Installation →](installation.md)
