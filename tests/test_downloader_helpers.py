"""Tests for Downloader helper methods."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yt_dlp

from vidgrab.downloader import DownloadConfig, Downloader


class TestExpandPlaylists:
    """Test playlist expansion logic."""

    @patch("vidgrab.downloader._check_ffmpeg")
    @patch("vidgrab.downloader.yt_dlp.YoutubeDL")
    def test_expands_playlist_to_individual_urls(
        self, mock_ydl_class: MagicMock, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """Expand a playlist URL into individual watch URLs."""
        mock_ydl = MagicMock()
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl
        mock_ydl.extract_info.return_value = {
            "entries": [
                {"url": "https://www.youtube.com/watch?v=vid1"},
                {"url": "https://www.youtube.com/watch?v=vid2"},
            ]
        }

        config = DownloadConfig(output_dir=tmp_path)
        downloader = Downloader(config)

        urls = downloader.expand_playlists(["https://youtube.com/playlist?list=PLxxx"])

        assert len(urls) == 2
        assert "vid1" in urls[0]
        assert "vid2" in urls[1]

    @patch("vidgrab.downloader._check_ffmpeg")
    @patch("vidgrab.downloader.yt_dlp.YoutubeDL")
    def test_non_playlist_url_passes_through(
        self, mock_ydl_class: MagicMock, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """Non-playlist URLs should pass through unchanged."""
        mock_ydl = MagicMock()
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl
        mock_ydl.extract_info.return_value = {"entries": None}

        config = DownloadConfig(output_dir=tmp_path)
        downloader = Downloader(config)

        urls = downloader.expand_playlists(["https://youtu.be/single_video"])

        assert urls == ["https://youtu.be/single_video"]

    @patch("vidgrab.downloader._check_ffmpeg")
    @patch("vidgrab.downloader.yt_dlp.YoutubeDL")
    def test_mixed_playlist_and_single_urls(
        self, mock_ydl_class: MagicMock, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """Handle mix of playlists and single videos."""
        mock_ydl = MagicMock()
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl

        def side_effect(url, **kwargs):
            if "playlist" in url:
                return {
                    "entries": [
                        {"url": "https://www.youtube.com/watch?v=pl_vid1"},
                        {"url": "https://www.youtube.com/watch?v=pl_vid2"},
                    ]
                }
            return {"entries": None}

        mock_ydl.extract_info.side_effect = side_effect

        config = DownloadConfig(output_dir=tmp_path)
        downloader = Downloader(config)

        urls = downloader.expand_playlists([
            "https://youtube.com/playlist?list=PLxxx",
            "https://youtu.be/single",
        ])

        assert len(urls) == 3
        assert "pl_vid1" in urls[0]
        assert "pl_vid2" in urls[1]
        assert "single" in urls[2]

    @patch("vidgrab.downloader._check_ffmpeg")
    @patch("vidgrab.downloader.yt_dlp.YoutubeDL")
    def test_handles_extraction_error_gracefully(
        self, mock_ydl_class: MagicMock, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """On extraction error, return original URL."""
        mock_ydl = MagicMock()
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl
        mock_ydl.extract_info.side_effect = Exception("Network error")

        config = DownloadConfig(output_dir=tmp_path)
        downloader = Downloader(config)

        urls = downloader.expand_playlists(["https://youtube.com/playlist?list=PLxxx"])

        # Should return original URL on error
        assert urls == ["https://youtube.com/playlist?list=PLxxx"]


class TestResolveOutputPath:
    """Test output path resolution logic."""

    @patch("vidgrab.downloader._check_ffmpeg")
    def test_uses_requested_downloads_filepath(
        self, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """Prefer filepath from requested_downloads."""
        config = DownloadConfig(output_dir=tmp_path)
        downloader = Downloader(config)

        info = {
            "requested_downloads": [
                {"filepath": str(tmp_path / "video.mp4")}
            ]
        }

        path = downloader._resolve_output_path(info)
        assert path == Path(tmp_path / "video.mp4")

    @patch("vidgrab.downloader._check_ffmpeg")
    def test_generates_path_from_metadata(
        self, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """Generate path from id, upload_date, and title."""
        config = DownloadConfig(output_dir=tmp_path)
        downloader = Downloader(config)

        info = {
            "id": "abc123",
            "upload_date": "20260621",
            "title": "Test Video",
            "ext": "mp4",
        }

        path = downloader._resolve_output_path(info)

        assert path.name == "20260621-test-video-abc123.mp4"
        assert path.parent == tmp_path

    @patch("vidgrab.downloader._check_ffmpeg")
    def test_handles_missing_fields_gracefully(
        self, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """Use defaults for missing fields."""
        config = DownloadConfig(output_dir=tmp_path)
        downloader = Downloader(config)

        info = {"id": "abc123"}

        path = downloader._resolve_output_path(info)

        assert "abc123" in path.name
        assert "untitled" in path.name or "19700101" in path.name


class TestFindExisting:
    """Test existing file detection."""

    @patch("vidgrab.downloader._check_ffmpeg")
    def test_finds_existing_file_by_video_id(
        self, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """Detect existing file by video ID."""
        # Create a dummy file with 11-char video ID
        dummy_file = tmp_path / "20260621-test-dQw4w9WgXcQ.mp4"
        dummy_file.touch()

        config = DownloadConfig(output_dir=tmp_path)
        downloader = Downloader(config)

        url = "https://youtu.be/dQw4w9WgXcQ"
        existing = downloader._find_existing(url)

        assert existing == dummy_file

    @patch("vidgrab.downloader._check_ffmpeg")
    def test_returns_none_when_file_not_found(
        self, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """Return None if no file exists."""
        config = DownloadConfig(output_dir=tmp_path)
        downloader = Downloader(config)

        url = "https://youtu.be/XXXXXXXXXXXX"
        existing = downloader._find_existing(url)

        assert existing is None

    @patch("vidgrab.downloader._check_ffmpeg")
    def test_ignores_json_sidecar(
        self, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """Skip .json files when looking for video."""
        json_file = tmp_path / "20260621-test-dQw4w9WgXcQ.json"
        json_file.touch()

        config = DownloadConfig(output_dir=tmp_path)
        downloader = Downloader(config)

        url = "https://youtu.be/dQw4w9WgXcQ"
        existing = downloader._find_existing(url)

        # Should not return the JSON file
        assert existing is None

    @patch("vidgrab.downloader._check_ffmpeg")
    def test_handles_invalid_url(
        self, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """Return None for URLs without valid video ID."""
        config = DownloadConfig(output_dir=tmp_path)
        downloader = Downloader(config)

        url = "https://invalid.com/short"
        existing = downloader._find_existing(url)

        assert existing is None


class TestBuildYdlOpts:
    """Test yt-dlp options building."""

    @patch("vidgrab.downloader._check_ffmpeg")
    def test_includes_required_options(
        self, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """Verify all required options are present."""
        config = DownloadConfig(output_dir=tmp_path)
        downloader = Downloader(config)

        def dummy_hook(d):
            pass

        opts = downloader._build_ydl_opts(dummy_hook)

        assert "format" in opts
        assert "outtmpl" in opts
        assert "merge_output_format" in opts
        assert "continuedl" in opts
        assert opts["continuedl"] is True
        assert "progress_hooks" in opts

    @patch("vidgrab.downloader._check_ffmpeg")
    def test_respects_cookies_file(
        self, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """Include cookies file in options when provided."""
        cookies = tmp_path / "cookies.txt"
        cookies.touch()

        config = DownloadConfig(output_dir=tmp_path, cookies_file=cookies)
        downloader = Downloader(config)

        def dummy_hook(d):
            pass

        opts = downloader._build_ydl_opts(dummy_hook)

        assert "cookiefile" in opts
        assert str(cookies) in opts["cookiefile"]

    @patch("vidgrab.downloader._check_ffmpeg")
    def test_format_selector_with_max_height(
        self, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """Format string includes height limit when specified."""
        config = DownloadConfig(output_dir=tmp_path, max_height=1080)
        downloader = Downloader(config)

        def dummy_hook(d):
            pass

        opts = downloader._build_ydl_opts(dummy_hook)

        assert "1080" in opts["format"]
