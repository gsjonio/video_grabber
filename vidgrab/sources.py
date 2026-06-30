"""Per-source strategy — isolates the only bits that differ between video sites.

The download engine (yt-dlp) is source-agnostic and shared. A ``Source`` owns
just the three things that vary per site: recognising its URLs, extracting a
video ID from a URL (for skip-existing), and normalising playlist entries into
full watch URLs.

ponytail: only a Source seam exists, not a download-engine abstraction — yt-dlp
already handles every planned source. Add an engine interface only if a future
source is not yt-dlp-supported (custom API/scraper).
"""

from __future__ import annotations

import re
from typing import Any, Protocol


class Source(Protocol):
    """A video site. Encapsulates the URL handling that differs per site."""

    name: str

    def matches(self, url: str) -> bool:
        """Return True if *url* belongs to this source."""

    def extract_id(self, url: str) -> str | None:
        """Return the site video ID from *url*, or None if it can't be parsed.

        None disables the pre-download skip-existing check for that URL.
        """

    def canonical_url(self, entry: dict[str, Any]) -> str:
        """Turn a playlist entry dict into a full watch URL."""


_YOUTUBE_ID_RE: re.Pattern[str] = re.compile(
    r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})"
)


class YouTubeSource:
    """YouTube — youtube.com / youtu.be watch, shorts and playlist URLs."""

    name = "youtube"

    def matches(self, url: str) -> bool:
        """True for youtube.com / youtu.be URLs."""
        return "youtube.com" in url or "youtu.be" in url

    def extract_id(self, url: str) -> str | None:
        """Return the 11-char YouTube video ID, or None."""
        match = _YOUTUBE_ID_RE.search(url)
        return match.group(1) if match else None

    def canonical_url(self, entry: dict[str, Any]) -> str:
        """Build a watch?v= URL, reconstructing it from a bare ID if needed."""
        entry_url = str(entry.get("url") or entry.get("webpage_url", ""))
        if not entry_url.startswith("http"):
            entry_url = f"https://www.youtube.com/watch?v={entry_url}"
        return entry_url


class GenericSource:
    """Fallback for any yt-dlp-supported URL without a dedicated Source.

    Skip-existing is disabled (no URL→ID rule); playlist entries are used as-is
    instead of being forced under youtube.com.
    """

    name = "generic"

    def matches(self, url: str) -> bool:
        """Match anything — used only as the registry fallback."""
        return True

    def extract_id(self, url: str) -> str | None:
        """No URL→ID rule; skip-existing is disabled for unknown sources."""
        return None

    def canonical_url(self, entry: dict[str, Any]) -> str:
        """Use the entry URL as-is, without forcing any host."""
        return str(entry.get("url") or entry.get("webpage_url", ""))


# Registry: first match wins. Register new sources here.
_SOURCES: list[Source] = [YouTubeSource()]
_GENERIC: Source = GenericSource()


def resolve(url: str) -> Source:
    """Return the first registered Source matching *url*, else the generic one."""
    return next((s for s in _SOURCES if s.matches(url)), _GENERIC)
