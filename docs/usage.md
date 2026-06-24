---
layout: page
title: Usage
---

# Usage Guide

## Basic Usage

### Single Video

Download a YouTube video at maximum quality:

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ
```

Output file: `20090101-never-gonna-give-you-up-dQw4w9WgXcQ.mp4`

### Inspect Before Downloading

See what will be downloaded without actually downloading:

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --dry-run
```

Output:
```
Rick Astley - Never Gonna Give You Up (Official Video) (4K Remaster)
2160p (DASH) · 232.5 MB
```

---

## Advanced Usage

### Limit Resolution

Cap at 1080p instead of maximum:

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --max-height 1080
```

### Save to Custom Directory

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --output ~/Videos/raw
```

### Batch Download

Download multiple videos from a `.txt` file:

```bash
vidgrab --batch urls.txt
```

**urls.txt:**
```text
# My videos
https://youtu.be/dQw4w9WgXcQ
https://youtu.be/VIDEO_ID_2

# Another video
https://youtu.be/VIDEO_ID_3
```

Comments (`#`) and blank lines are ignored.

### Parallel Downloads

Download multiple files simultaneously:

```bash
vidgrab --batch urls.txt --workers 5
```

**Note:** Max 8 workers to avoid rate-limiting.

### Playlist Expansion

Download all videos from a playlist:

```bash
vidgrab "https://youtube.com/playlist?list=PLxxxx" --playlist
```

vidgrab will expand the playlist and download all videos.

### Force Re-download

By default, vidgrab skips existing files. Force download anyway:

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --force
```

### Age-Gated Videos

For age-restricted videos, provide a cookies file (Netscape format):

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --cookies ~/cookies.txt
```

[How to export cookies →](#exporting-cookies)

### Save Metadata

Save video metadata as JSON sidecar:

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --write-json
```

Creates file: `20090101-never-gonna-give-you-up-dQw4w9WgXcQ.json`

```json
{
  "video_id": "dQw4w9WgXcQ",
  "title": "Rick Astley - Never Gonna Give You Up",
  "channel": "Rick Astley",
  "upload_date": "2009-10-25",
  "duration_seconds": 212,
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "description": "...",
  "tags": ["pop", "80s"]
}
```

### Quiet Mode

Suppress output (useful for scripts):

```bash
vidgrab https://youtu.be/dQw4w9WgXcQ --quiet
```

Only errors are printed.

---

## Configuration

### Personal Defaults

Instead of repeating flags, save defaults in `~/.config/vidgrab/config.toml`:

```toml
output     = "~/Videos/raw"
workers    = 5
max_height = 1080
```

**Note:** CLI flags always override config file.

### Config File Location

- **Linux/macOS:** `~/.config/vidgrab/config.toml`
- **Windows:** `%APPDATA%\vidgrab\config.toml`

---

## File Naming

All downloads follow this pattern:

```
{upload_date}-{title-slug}-{video_id}.{ext}
```

**Example:** `20240315-never-gonna-give-you-up-dQw4w9WgXcQ.mp4`

This ensures:
- ✅ Chronological sorting
- ✅ Easy to identify videos
- ✅ Safe filenames (no special chars)
- ✅ Unique by video ID (no duplicates)

---

## Output Formats

vidgrab automatically chooses the best container based on available streams:

| Video Stream | Audio Stream | Container |
| --- | --- | --- |
| H.264 | AAC | `.mp4` |
| VP9/AV1 | Opus | `.mkv` |

All downloads are **zero re-encoding** (copy mode).

---

## Exporting Cookies

For age-gated videos, export cookies from your browser:

### Firefox
1. Install [Export Cookies](https://addons.mozilla.org/en-US/firefox/addon/export-cookies-txt/) extension
2. Click extension → Export cookies
3. Use exported file with `--cookies`

### Chrome
1. Install [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndcbkpkhkkhkbnkmejlambmlnac) extension
2. Click extension → Export cookies
3. Use exported file with `--cookies`

---

## Troubleshooting

### Rate Limiting

If YouTube rate-limits you, vidgrab automatically retries with exponential backoff (up to 5 attempts). Just wait and try again.

### Age-Gated Videos

Use `--cookies` with exported browser cookies.

### Video Not Found

- Video may be deleted or private
- Try with `--dry-run` to see what vidgrab detects

### Slow Download

Check your connection speed. vidgrab downloads at your network speed.

---

## All Options

```bash
vidgrab --help
```

| Option | Short | Description |
| --- | --- | --- |
| `[URLS]...` | | One or more YouTube URLs |
| `--batch FILE` | `-b` | `.txt` file with one URL per line |
| `--output DIR` | `-o` | Output directory |
| `--max-height INT` | | Limit resolution (e.g. 1080) |
| `--playlist` | | Treat URLs as playlists |
| `--force` | `-f` | Re-download existing files |
| `--cookies FILE` | | Netscape cookies for age-gated videos |
| `--write-json` | | Save metadata as JSON sidecar |
| `--workers INT` | `-w` | Parallel downloads (default 3, max 8) |
| `--dry-run` | | Preview without downloading |
| `--quiet` | `-q` | Suppress output (errors only) |
| `--version` | `-V` | Show version |
| `--install-completion` | | Install shell autocomplete |
| `--help` | | Show help |

---

[← Back to Features](features.md) · [Contributing →](contributing.md)
