"""Tests for rate-limit handling and exponential backoff retry logic."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
import yt_dlp

from vidgrab.downloader import DownloadConfig, Downloader, _classify_error, _ErrorKind
from vidgrab.exceptions import DownloadError as VidGrabDownloadError


class TestErrorClassification:
    """Test _classify_error correctly categorizes error messages."""

    def test_classifies_rate_limit_429(self) -> None:
        assert _classify_error("HTTP Error 429") is _ErrorKind.RATE_LIMITED

    def test_classifies_rate_limit_too_many_requests(self) -> None:
        assert _classify_error("Too many requests") is _ErrorKind.RATE_LIMITED

    def test_classifies_rate_limit_case_insensitive(self) -> None:
        assert _classify_error("RATE LIMIT EXCEEDED") is _ErrorKind.RATE_LIMITED

    def test_classifies_unavailable(self) -> None:
        assert _classify_error("Video unavailable") is _ErrorKind.UNAVAILABLE

    def test_classifies_geo_block(self) -> None:
        assert _classify_error("not available in your country") is _ErrorKind.GEO

    def test_classifies_age_restricted(self) -> None:
        assert _classify_error("age-restricted") is _ErrorKind.AGE

    def test_classifies_generic_error(self) -> None:
        assert _classify_error("Some random error") is _ErrorKind.GENERIC


class TestRetryLogic:
    """Test that rate-limited downloads are retried with exponential backoff."""

    @patch("vidgrab.downloader.yt_dlp.YoutubeDL")
    @patch("vidgrab.downloader.time.sleep")
    def test_retries_on_rate_limit(
        self, mock_sleep: MagicMock, mock_ydl_class: MagicMock, tmp_path
    ) -> None:
        """Simulate 429 on first 2 attempts, success on 3rd."""
        mock_ydl = MagicMock()
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl

        # First 2 calls raise 429, 3rd succeeds
        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                raise yt_dlp.utils.DownloadError("HTTP Error 429: Too many requests")
            return {
                "id": "test_video",
                "title": "Test",
                "ext": "mp4",
                "upload_date": "20260621",
            }

        mock_ydl.extract_info.side_effect = side_effect

        config = DownloadConfig(output_dir=tmp_path)
        downloader = Downloader(config)

        result = downloader.download("https://youtu.be/test")

        # Should have retried twice (sleep called twice)
        assert mock_sleep.call_count == 2
        # Final result should succeed
        assert result.success
        # extract_info should have been called 3 times (2 failures + 1 success)
        assert mock_ydl.extract_info.call_count == 3

    @patch("vidgrab.downloader._run_ydl")
    @patch("vidgrab.downloader.time.sleep")
    def test_rate_limit_all_retries_exhausted(
        self, mock_sleep: MagicMock, mock_run_ydl: MagicMock, tmp_path
    ) -> None:
        """Rate limit on all 5 attempts should raise DownloadError."""
        mock_run_ydl.side_effect = VidGrabDownloadError("test", reason="HTTP Error 429")

        config = DownloadConfig(output_dir=tmp_path)
        downloader = Downloader(config)

        with pytest.raises(VidGrabDownloadError):
            downloader._extract_and_download("https://youtu.be/test", lambda x: None)

        # All 5 attempts should have been made
        assert mock_run_ydl.call_count == 5
        # Backoff sleeps: 2, 4, 8, 16 (4 sleeps for 5 attempts)
        assert mock_sleep.call_count == 4

    @patch("vidgrab.downloader._run_ydl")
    def test_non_rate_limit_error_does_not_retry(
        self, mock_run_ydl: MagicMock, tmp_path
    ) -> None:
        """Non-rate-limit errors should fail immediately without retry."""
        mock_run_ydl.side_effect = VidGrabDownloadError("test", reason="Video unavailable")

        config = DownloadConfig(output_dir=tmp_path)
        downloader = Downloader(config)

        with pytest.raises(VidGrabDownloadError):
            downloader._extract_and_download("https://youtu.be/test", lambda x: None)

        # Should not retry — only 1 attempt
        assert mock_run_ydl.call_count == 1

    @patch("vidgrab.downloader.yt_dlp.YoutubeDL")
    @patch("vidgrab.downloader.time.sleep")
    def test_exponential_backoff_delays(
        self, mock_sleep: MagicMock, mock_ydl_class: MagicMock, tmp_path
    ) -> None:
        """Verify exponential backoff: 2s, 4s, 8s, 16s."""
        mock_ydl = MagicMock()
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl
        mock_ydl.extract_info.side_effect = yt_dlp.utils.DownloadError(
            "HTTP Error 429"
        )

        config = DownloadConfig(output_dir=tmp_path)
        downloader = Downloader(config)

        try:
            downloader.download("https://youtu.be/test")
        except Exception:
            pass

        # Check the delay values
        expected_delays = [2.0, 4.0, 8.0, 16.0]
        actual_delays = [call[0][0] for call in mock_sleep.call_args_list]
        assert actual_delays == expected_delays
