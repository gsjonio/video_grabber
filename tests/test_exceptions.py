"""Tests for custom exception hierarchy."""

from __future__ import annotations

import pytest

from vidgrab.exceptions import (
    AgeRestrictedError,
    DownloadError,
    FfmpegNotFoundError,
    GeoBlockedError,
    VideoUnavailableError,
    VidGrabError,
)


class TestExceptionHierarchy:
    """Test that all exceptions inherit from VidGrabError."""

    def test_video_unavailable_error_inheritance(self) -> None:
        assert issubclass(VideoUnavailableError, VidGrabError)

    def test_geo_blocked_error_inheritance(self) -> None:
        assert issubclass(GeoBlockedError, VidGrabError)

    def test_age_restricted_error_inheritance(self) -> None:
        assert issubclass(AgeRestrictedError, VidGrabError)

    def test_download_error_inheritance(self) -> None:
        assert issubclass(DownloadError, VidGrabError)

    def test_ffmpeg_not_found_error_inheritance(self) -> None:
        assert issubclass(FfmpegNotFoundError, VidGrabError)


class TestVideoUnavailableError:
    """Test VideoUnavailableError construction and message."""

    def test_construct_with_url_and_reason(self) -> None:
        err = VideoUnavailableError("https://youtu.be/test", reason="private video")
        assert "https://youtu.be/test" in str(err)
        assert "private video" in str(err)

    def test_construct_with_url_only(self) -> None:
        err = VideoUnavailableError("https://youtu.be/test")
        assert "https://youtu.be/test" in str(err)

    def test_is_vidgrab_error(self) -> None:
        err = VideoUnavailableError("https://youtu.be/test")
        assert isinstance(err, VidGrabError)


class TestGeoBlockedError:
    """Test GeoBlockedError construction and message."""

    def test_construct_with_url(self) -> None:
        err = GeoBlockedError("https://youtu.be/test")
        assert "https://youtu.be/test" in str(err)
        assert "geo-blocked" in str(err).lower()

    def test_is_vidgrab_error(self) -> None:
        err = GeoBlockedError("https://youtu.be/test")
        assert isinstance(err, VidGrabError)


class TestAgeRestrictedError:
    """Test AgeRestrictedError construction and message."""

    def test_construct_with_url(self) -> None:
        err = AgeRestrictedError("https://youtu.be/test")
        assert "https://youtu.be/test" in str(err)
        assert "age" in str(err).lower()

    def test_message_includes_cookies_instruction(self) -> None:
        err = AgeRestrictedError("https://youtu.be/test")
        assert "https://youtu.be/test" in str(err)
        assert "cookies" in str(err).lower()

    def test_is_vidgrab_error(self) -> None:
        err = AgeRestrictedError("https://youtu.be/test")
        assert isinstance(err, VidGrabError)


class TestDownloadError:
    """Test DownloadError construction and message."""

    def test_construct_with_url_and_reason(self) -> None:
        err = DownloadError("https://youtu.be/test", reason="network timeout")
        assert "https://youtu.be/test" in str(err)
        assert "network timeout" in str(err)

    def test_construct_with_generic_reason(self) -> None:
        err = DownloadError("https://youtu.be/test", reason="unknown error")
        assert "https://youtu.be/test" in str(err)
        assert "unknown error" in str(err)

    def test_is_vidgrab_error(self) -> None:
        err = DownloadError("https://youtu.be/test", reason="network error")
        assert isinstance(err, VidGrabError)


class TestFfmpegNotFoundError:
    """Test FfmpegNotFoundError construction and message."""

    def test_construct_no_args(self) -> None:
        err = FfmpegNotFoundError()
        assert "ffmpeg" in str(err).lower()

    def test_message_includes_download_link(self) -> None:
        err = FfmpegNotFoundError()
        err_msg = str(err).lower()
        assert ("ffmpeg.org" in err_msg or "download" in err_msg)

    def test_is_vidgrab_error(self) -> None:
        err = FfmpegNotFoundError()
        assert isinstance(err, VidGrabError)


class TestExceptionCatching:
    """Test that exceptions can be caught by base class."""

    def test_catch_video_unavailable_as_vidgrab_error(self) -> None:
        with pytest.raises(VidGrabError):
            raise VideoUnavailableError("https://youtu.be/test")

    def test_catch_geo_blocked_as_vidgrab_error(self) -> None:
        with pytest.raises(VidGrabError):
            raise GeoBlockedError("https://youtu.be/test")

    def test_catch_age_restricted_as_vidgrab_error(self) -> None:
        with pytest.raises(VidGrabError):
            raise AgeRestrictedError("https://youtu.be/test")

    def test_catch_download_error_as_vidgrab_error(self) -> None:
        with pytest.raises(VidGrabError):
            raise DownloadError("https://youtu.be/test", reason="network error")

    def test_catch_ffmpeg_not_found_as_vidgrab_error(self) -> None:
        with pytest.raises(VidGrabError):
            raise FfmpegNotFoundError()
