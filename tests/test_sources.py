"""Tests for source resolution and per-source URL handling."""

from __future__ import annotations

import pytest

from vidgrab.sources import GenericSource, YouTubeSource, resolve


class TestResolve:
    """resolve() picks the right Source for a URL."""

    @pytest.mark.parametrize(
        "url",
        [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://youtube.com/shorts/dQw4w9WgXcQ",
        ],
    )
    def test_youtube_urls_resolve_to_youtube_source(self, url: str) -> None:
        assert resolve(url).name == "youtube"

    @pytest.mark.parametrize(
        "url",
        [
            "https://vimeo.com/123456",
            "https://www.twitch.tv/videos/123",
            "https://example.com/whatever",
        ],
    )
    def test_unknown_urls_fall_back_to_generic(self, url: str) -> None:
        assert resolve(url).name == "generic"


class TestYouTubeSource:
    """YouTubeSource extracts IDs and normalises playlist entries."""

    @pytest.mark.parametrize(
        ("url", "expected"),
        [
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://youtube.com/shorts/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ],
    )
    def test_extract_id(self, url: str, expected: str) -> None:
        assert YouTubeSource().extract_id(url) == expected

    def test_extract_id_returns_none_when_absent(self) -> None:
        assert YouTubeSource().extract_id("https://youtube.com/feed/subscriptions") is None

    def test_canonical_url_builds_watch_url_from_bare_id(self) -> None:
        url = YouTubeSource().canonical_url({"url": "abc123"})
        assert url == "https://www.youtube.com/watch?v=abc123"

    def test_canonical_url_keeps_full_url(self) -> None:
        full = "https://www.youtube.com/watch?v=abc123"
        assert YouTubeSource().canonical_url({"url": full}) == full


class TestGenericSource:
    """GenericSource disables skip-existing and never forces youtube.com."""

    def test_extract_id_is_none(self) -> None:
        assert GenericSource().extract_id("https://vimeo.com/123456") is None

    def test_canonical_url_passes_entry_through(self) -> None:
        entry = {"url": "https://vimeo.com/123456"}
        assert GenericSource().canonical_url(entry) == "https://vimeo.com/123456"

    def test_canonical_url_does_not_prepend_youtube(self) -> None:
        # ponytail: this is the regression guard for the cross-source playlist bug
        url = GenericSource().canonical_url({"webpage_url": "https://vimeo.com/9"})
        assert "youtube.com" not in url
