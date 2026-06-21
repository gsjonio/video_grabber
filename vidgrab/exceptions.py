"""Custom exceptions for vidgrab."""


class VidGrabError(Exception):
    """Base class for all vidgrab errors."""


class VideoUnavailableError(VidGrabError):
    """Raised when a video is private, deleted, or otherwise unavailable."""

    def __init__(self, url: str, reason: str = "unknown") -> None:
        self.url = url
        self.reason = reason
        super().__init__(f"Video unavailable ({reason}): {url}")


class GeoBlockedError(VidGrabError):
    """Raised when a video is blocked in the current region."""

    def __init__(self, url: str, country: str = "your region") -> None:
        self.url = url
        self.country = country
        super().__init__(f"Video is geo-blocked in {country}: {url}")


class AgeRestrictedError(VidGrabError):
    """Raised when a video requires age verification but no cookies are provided."""

    def __init__(self, url: str) -> None:
        self.url = url
        super().__init__(
            f"Video is age-restricted. Provide cookies via --cookies to download: {url}"
        )


class FfmpegNotFoundError(VidGrabError):
    """Raised when ffmpeg is not found in PATH."""

    def __init__(self) -> None:
        super().__init__(
            "ffmpeg not found in PATH. Install it from https://ffmpeg.org/download.html "
            "and make sure it is accessible as 'ffmpeg' in your terminal."
        )


class DownloadError(VidGrabError):
    """Generic download failure (network error, rate limit exhausted, etc.)."""

    def __init__(self, url: str, reason: str) -> None:
        self.url = url
        self.reason = reason
        super().__init__(f"Download failed for {url}: {reason}")
