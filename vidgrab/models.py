"""Data models for vidgrab."""

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any


@dataclass
class VideoMetadata:
    """Metadata extracted from a YouTube video info dict.

    Args:
        video_id: YouTube video ID (e.g. "dQw4w9WgXcQ").
        title: Human-readable title.
        channel: Channel name.
        upload_date: Date the video was uploaded.
        duration_seconds: Length of the video in seconds.
        url: Original watch URL.
        description: Full video description (may be empty).
        tags: List of tags associated with the video.
    """

    video_id: str
    title: str
    channel: str
    upload_date: date
    duration_seconds: int
    url: str
    description: str = ""
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dict suitable for JSON serialisation."""
        return {
            "video_id": self.video_id,
            "title": self.title,
            "channel": self.channel,
            "upload_date": self.upload_date.isoformat(),
            "duration_seconds": self.duration_seconds,
            "url": self.url,
            "description": self.description,
            "tags": self.tags,
        }

    @classmethod
    def from_yt_dlp_info(cls, info: dict[str, Any]) -> "VideoMetadata":
        """Build a VideoMetadata from the raw info dict returned by yt-dlp.

        Args:
            info: The dict returned by ``YoutubeDL.extract_info``.

        Returns:
            A populated VideoMetadata instance.
        """
        raw_date = info.get("upload_date", "19700101")
        upload_date = date(
            int(raw_date[:4]),
            int(raw_date[4:6]),
            int(raw_date[6:8]),
        )
        return cls(
            video_id=info["id"],
            title=info.get("title", ""),
            channel=info.get("channel") or info.get("uploader", ""),
            upload_date=upload_date,
            duration_seconds=int(info.get("duration") or 0),
            url=info.get("webpage_url") or info.get("original_url", ""),
            description=info.get("description") or "",
            tags=list(info.get("tags") or []),
        )


@dataclass
class DownloadResult:
    """Outcome of a single video download attempt.

    Args:
        url: The URL that was requested.
        success: Whether the download completed without error.
        output_path: Path to the downloaded file (None on failure).
        metadata: Extracted metadata (None on failure).
        error: Error message (None on success).
        skipped: True when the file already existed and --force was not set.
    """

    url: str
    success: bool
    output_path: Path | None = None
    metadata: VideoMetadata | None = None
    error: str | None = None
    skipped: bool = False
