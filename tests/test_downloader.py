"""Tests for vidgrab.downloader pure functions and DownloadConfig."""

from __future__ import annotations

from pathlib import Path

import pytest

from vidgrab.downloader import (
    DownloadConfig,
    _ErrorKind,
    _classify_error,
    _format_selector,
    _slugify,
)


# ---------------------------------------------------------------------------
# _slugify
# ---------------------------------------------------------------------------

class TestSlugify:
    def test_lowercases(self) -> None:
        assert _slugify("Hello World") == "hello-world"

    def test_strips_special_chars(self) -> None:
        assert _slugify("Rick & Morty!") == "rick-morty"

    def test_collapses_spaces(self) -> None:
        assert _slugify("a   b") == "a-b"

    def test_collapses_dashes(self) -> None:
        assert _slugify("a--b") == "a-b"

    def test_truncates_to_max_length(self) -> None:
        long = "a" * 200
        assert len(_slugify(long, max_length=80)) == 80

    def test_strips_leading_trailing_dashes(self) -> None:
        assert not _slugify("-hello-").startswith("-")
        assert not _slugify("-hello-").endswith("-")


# ---------------------------------------------------------------------------
# _classify_error
# ---------------------------------------------------------------------------

class TestClassifyError:
    def test_unavailable(self) -> None:
        assert _classify_error("Video unavailable") is _ErrorKind.UNAVAILABLE

    def test_private(self) -> None:
        assert _classify_error("This is a private video") is _ErrorKind.UNAVAILABLE

    def test_removed(self) -> None:
        assert _classify_error("This video has been removed") is _ErrorKind.UNAVAILABLE

    def test_geo_blocked(self) -> None:
        assert _classify_error("not available in your country") is _ErrorKind.GEO

    def test_age_restricted(self) -> None:
        assert _classify_error("age-restricted content") is _ErrorKind.AGE

    def test_rate_limited_429(self) -> None:
        assert _classify_error("HTTP Error 429: Too Many Requests") is _ErrorKind.RATE_LIMITED

    def test_rate_limited_500(self) -> None:
        assert _classify_error("http error 500") is _ErrorKind.RATE_LIMITED

    def test_generic_fallback(self) -> None:
        assert _classify_error("something completely unexpected") is _ErrorKind.GENERIC

    def test_case_insensitive(self) -> None:
        assert _classify_error("VIDEO UNAVAILABLE") is _ErrorKind.UNAVAILABLE


# ---------------------------------------------------------------------------
# _format_selector
# ---------------------------------------------------------------------------

class TestFormatSelector:
    def test_no_limit(self) -> None:
        assert _format_selector(None) == "bestvideo+bestaudio/best"

    def test_with_limit(self) -> None:
        sel = _format_selector(1080)
        assert "1080" in sel
        assert sel.startswith("bestvideo")


# ---------------------------------------------------------------------------
# DownloadConfig
# ---------------------------------------------------------------------------

class TestDownloadConfig:
    def test_defaults(self) -> None:
        cfg = DownloadConfig()
        assert cfg.output_dir == Path(".")
        assert cfg.max_height is None
        assert cfg.cookies_file is None
        assert cfg.force is False
        assert cfg.workers == 3
        assert cfg.write_json is False
        assert cfg.dry_run is False

    def test_is_frozen(self) -> None:
        cfg = DownloadConfig()
        with pytest.raises(Exception):
            cfg.force = True  # type: ignore[misc]

    def test_custom_values(self) -> None:
        cfg = DownloadConfig(
            output_dir=Path("/tmp"),
            max_height=1080,
            force=True,
            workers=5,
            dry_run=True,
        )
        assert cfg.output_dir == Path("/tmp")
        assert cfg.max_height == 1080
        assert cfg.force is True
        assert cfg.workers == 5
        assert cfg.dry_run is True
