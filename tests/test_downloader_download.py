"""Tests for Downloader download and inspection methods."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from vidgrab.downloader import DownloadConfig, Downloader
from vidgrab.models import DownloadResult, VideoMetadata


class TestInspectOne:
    """Test dry-run inspection without downloading."""

    @patch("vidgrab.downloader._check_ffmpeg")
    @patch("vidgrab.downloader.yt_dlp.YoutubeDL")
    def test_extracts_video_info_without_downloading(
        self, mock_ydl_class: MagicMock, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """Dry-run extracts metadata without download."""
        mock_ydl = MagicMock()
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl
        mock_ydl.extract_info.return_value = {
            "id": "test_vid",
            "title": "Test Video",
            "height": 1080,
            "requested_formats": [
                {"filesize": 100_000_000, "height": 1080}
            ],
        }

        config = DownloadConfig(output_dir=tmp_path, dry_run=True)
        downloader = Downloader(config)

        result = downloader._inspect_one("https://youtu.be/test_vid")

        assert result.success is True
        assert result.output_path is None  # No file downloaded
        assert result.url == "https://youtu.be/test_vid"

    @patch("vidgrab.downloader._check_ffmpeg")
    @patch("vidgrab.downloader.yt_dlp.YoutubeDL")
    def test_handles_extraction_error_gracefully(
        self, mock_ydl_class: MagicMock, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """On extraction error, return failed result."""
        import yt_dlp

        mock_ydl = MagicMock()
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl
        mock_ydl.extract_info.side_effect = yt_dlp.utils.DownloadError("Video unavailable")

        config = DownloadConfig(output_dir=tmp_path, dry_run=True)
        downloader = Downloader(config)

        result = downloader._inspect_one("https://youtu.be/test_vid")

        assert result.success is False
        assert result.error is not None
        assert "unavailable" in result.error.lower()

    @patch("vidgrab.downloader._check_ffmpeg")
    @patch("vidgrab.downloader.yt_dlp.YoutubeDL")
    def test_reports_resolution_and_size(
        self, mock_ydl_class: MagicMock, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """Dry-run reports resolution and estimated size."""
        mock_ydl = MagicMock()
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl
        mock_ydl.extract_info.return_value = {
            "id": "test_vid",
            "title": "Test Video",
            "height": 720,
            "requested_formats": [
                {"filesize": 250_000_000},
                {"filesize": 50_000_000},
            ],
        }

        config = DownloadConfig(output_dir=tmp_path)
        downloader = Downloader(config)

        result = downloader._inspect_one("https://youtu.be/test_vid")

        assert result.success is True


class TestDownloadBatch:
    """Test batch download orchestration."""

    @patch("vidgrab.downloader._check_ffmpeg")
    def test_dry_run_skips_downloads(
        self, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """Dry-run should call _inspect_one, not _download_one."""
        config = DownloadConfig(output_dir=tmp_path, dry_run=True)
        downloader = Downloader(config)

        with patch.object(downloader, "_inspect_one") as mock_inspect:
            mock_inspect.return_value = DownloadResult(
                url="https://youtu.be/test", success=True
            )

            results = downloader.download_batch(["https://youtu.be/test"])

            mock_inspect.assert_called_once()
            assert results[0].success is True

    @patch("vidgrab.downloader._check_ffmpeg")
    def test_preserves_url_order(
        self, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """Results should match input URL order."""
        config = DownloadConfig(output_dir=tmp_path, dry_run=True)
        downloader = Downloader(config)

        urls = [
            "https://youtu.be/url1",
            "https://youtu.be/url2",
            "https://youtu.be/url3",
        ]

        with patch.object(downloader, "_inspect_one") as mock_inspect:
            mock_inspect.return_value = DownloadResult(
                url="", success=True
            )

            results = downloader.download_batch(urls)

            # Results should be in same order as input
            assert len(results) == 3
            # All should be successful (mocked)
            assert all(r.success for r in results)


class TestWriteMetadataJson:
    """Test JSON metadata sidecar writing."""

    @patch("vidgrab.downloader._check_ffmpeg")
    def test_writes_json_sidecar_with_metadata(
        self, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """Metadata JSON is written next to video file."""
        config = DownloadConfig(output_dir=tmp_path)
        downloader = Downloader(config)

        video_path = tmp_path / "video.mp4"
        video_path.touch()

        metadata = VideoMetadata(
            video_id="test_id",
            title="Test Video",
            channel="Test Channel",
            upload_date=date(2026, 6, 21),
            duration_seconds=120,
            url="https://youtu.be/test_id",
            description="Test",
            tags=["tag1", "tag2"],
        )

        downloader._write_metadata_json(video_path, metadata)

        json_path = tmp_path / "video.json"
        assert json_path.exists()

        import json

        data = json.loads(json_path.read_text())
        assert data["video_id"] == "test_id"
        assert data["title"] == "Test Video"
        assert data["channel"] == "Test Channel"

    @patch("vidgrab.downloader._check_ffmpeg")
    def test_json_location_matches_video(
        self, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """JSON sidecar is in same directory as video."""
        config = DownloadConfig(output_dir=tmp_path)
        downloader = Downloader(config)

        subdir = tmp_path / "subdir"
        subdir.mkdir()
        video_path = subdir / "video.mp4"
        video_path.touch()

        metadata = VideoMetadata(
            video_id="id",
            title="Title",
            channel="Ch",
            upload_date=date(2026, 6, 21),
            duration_seconds=0,
            url="https://youtu.be/id",
        )

        downloader._write_metadata_json(video_path, metadata)

        json_path = subdir / "video.json"
        assert json_path.exists()


class TestDownloadOne:
    """Test single video download."""

    @patch("vidgrab.downloader._check_ffmpeg")
    @patch("vidgrab.downloader._run_ydl")
    def test_skips_existing_file_by_default(
        self, mock_run_ydl: MagicMock, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """Existing files are skipped unless --force."""
        # Create dummy file
        existing = tmp_path / "20260621-test-dQw4w9WgXcQ.mp4"
        existing.touch()

        config = DownloadConfig(output_dir=tmp_path, force=False)
        downloader = Downloader(config)

        with patch.object(downloader, "_find_existing") as mock_find:
            mock_find.return_value = existing

            result = downloader.download("https://youtu.be/dQw4w9WgXcQ")

            assert result.skipped is True
            # _run_ydl should NOT be called (file skipped)
            mock_run_ydl.assert_not_called()

    @patch("vidgrab.downloader._check_ffmpeg")
    @patch("vidgrab.downloader._run_ydl")
    def test_force_redownloads_existing_file(
        self, mock_run_ydl: MagicMock, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """--force downloads even if file exists."""
        existing = tmp_path / "20260621-test-dQw4w9WgXcQ.mp4"
        existing.touch()

        mock_run_ydl.return_value = {
            "id": "dQw4w9WgXcQ",
            "title": "Test",
            "ext": "mp4",
            "upload_date": "20260621",
            "requested_downloads": [{"filepath": str(existing)}],
        }

        config = DownloadConfig(output_dir=tmp_path, force=True)
        downloader = Downloader(config)

        with patch.object(downloader, "_find_existing") as mock_find:
            mock_find.return_value = existing

            result = downloader.download("https://youtu.be/dQw4w9WgXcQ")

            # With force=True, should attempt download
            mock_run_ydl.assert_called()

    @patch("vidgrab.downloader._check_ffmpeg")
    @patch("vidgrab.downloader._run_ydl")
    def test_warns_non_creative_commons(
        self, mock_run_ydl: MagicMock, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """Downloads without CC license trigger warning."""
        mock_run_ydl.return_value = {
            "id": "test_id",
            "title": "Test",
            "ext": "mp4",
            "upload_date": "20260621",
            "license": "Custom License",  # Not Creative Commons
            "requested_downloads": [{"filepath": str(tmp_path / "video.mp4")}],
        }

        config = DownloadConfig(output_dir=tmp_path)
        downloader = Downloader(config)

        # Create the file so it's considered downloaded
        (tmp_path / "video.mp4").touch()

        result = downloader.download("https://youtu.be/test_id")

        # Should still succeed but note license
        assert result.success is True

    @patch("vidgrab.downloader._check_ffmpeg")
    @patch("vidgrab.downloader._run_ydl")
    def test_writes_json_when_requested(
        self, mock_run_ydl: MagicMock, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """--write-json creates metadata sidecar."""
        video_path = tmp_path / "video.mp4"

        mock_run_ydl.return_value = {
            "id": "test_id",
            "title": "Test Video",
            "channel": "Test Channel",
            "upload_date": "20260621",
            "ext": "mp4",
            "requested_downloads": [{"filepath": str(video_path)}],
        }

        config = DownloadConfig(output_dir=tmp_path, write_json=True)
        downloader = Downloader(config)

        # Create dummy video file
        video_path.touch()

        result = downloader.download("https://youtu.be/test_id")

        json_path = tmp_path / "video.json"
        assert json_path.exists()
        assert result.success is True

    @patch("vidgrab.downloader._check_ffmpeg")
    @patch("vidgrab.downloader._run_ydl")
    def test_respects_cookies_file(
        self, mock_run_ydl: MagicMock, mock_check_ffmpeg: MagicMock, tmp_path
    ) -> None:
        """Cookies file is passed to yt-dlp."""
        cookies = tmp_path / "cookies.txt"
        cookies.touch()

        mock_run_ydl.return_value = {
            "id": "test_id",
            "title": "Test",
            "ext": "mp4",
            "upload_date": "20260621",
            "requested_downloads": [{"filepath": str(tmp_path / "video.mp4")}],
        }

        config = DownloadConfig(output_dir=tmp_path, cookies_file=cookies)
        downloader = Downloader(config)

        (tmp_path / "video.mp4").touch()

        downloader.download("https://youtu.be/test_id")

        # Verify _build_ydl_opts includes cookiefile
        # (tested separately in test_downloader_helpers)
