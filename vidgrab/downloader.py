"""Core download logic — thin wrapper over yt-dlp."""

from __future__ import annotations

import enum
import json
import re
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable

import yt_dlp
from rich.console import Console
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

from .exceptions import (
    AgeRestrictedError,
    DownloadError,
    FfmpegNotFoundError,
    GeoBlockedError,
    VideoUnavailableError,
    VidGrabError,
)
from .models import DownloadResult, VideoMetadata

_CONSOLE: Console = Console(stderr=True)

_UNAVAILABLE_PHRASES = (
    "video unavailable",
    "private video",
    "has been removed",
    "no longer available",
    "deleted",
)
_GEO_PHRASES = ("not available in your country", "geo", "region")
_AGE_PHRASES = ("age-restricted", "age restricted", "sign in to confirm your age")
_RATE_PHRASES = ("429", "rate", "too many", "http error 5")

_MAX_RETRY_ATTEMPTS: int = 5
_RETRY_BASE_DELAY: float = 2.0

_VIDEO_ID_RE: re.Pattern[str] = re.compile(
    r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})"
)


def _slugify(text: str, max_length: int = 80) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:max_length]


def _output_template(output_dir: Path) -> str:
    return str(output_dir / "%(upload_date)s-%(title)s-%(id)s.%(ext)s")


def _format_selector(max_height: int | None) -> str:
    if max_height:
        return f"bestvideo[height<={max_height}]+bestaudio/best[height<={max_height}]"
    return "bestvideo+bestaudio/best"


class _ErrorKind(enum.Enum):
    UNAVAILABLE = enum.auto()
    GEO = enum.auto()
    AGE = enum.auto()
    RATE_LIMITED = enum.auto()
    GENERIC = enum.auto()


def _classify_error(msg: str) -> _ErrorKind:
    lower = msg.lower()
    if any(p in lower for p in _UNAVAILABLE_PHRASES):
        return _ErrorKind.UNAVAILABLE
    if any(p in lower for p in _GEO_PHRASES):
        return _ErrorKind.GEO
    if any(p in lower for p in _AGE_PHRASES):
        return _ErrorKind.AGE
    if any(p in lower for p in _RATE_PHRASES):
        return _ErrorKind.RATE_LIMITED
    return _ErrorKind.GENERIC


def _check_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        raise FfmpegNotFoundError()


def _build_ydl_opts(
    output_dir: Path,
    max_height: int | None,
    cookies_file: Path | None,
    progress_hook: Callable[[dict], None] | None,
) -> dict:
    opts: dict = {
        "format": _format_selector(max_height),
        "outtmpl": _output_template(output_dir),
        "merge_output_format": "mp4",
        "writethumbnail": False,
        "writeinfojson": False,
        "noplaylist": True,
        "retries": 10,
        "fragment_retries": 10,
        "retry_sleep_functions": {
            "http": lambda n: min(2**n, 60),
            "fragment": lambda n: min(2**n, 60),
        },
        "quiet": True,
        "no_warnings": False,
        "noprogress": True,
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            }
        ],
        # Remux only — never re-encode video or audio.
        "postprocessor_args": {
            "ffmpeg": ["-c", "copy"],
        },
    }

    if progress_hook:
        opts["progress_hooks"] = [progress_hook]

    if cookies_file:
        opts["cookiefile"] = str(cookies_file)

    return opts


def _run_ydl(url: str, opts: dict) -> dict:
    """Execute a single yt-dlp extraction + download attempt.

    Translates yt-dlp errors into typed VidGrabErrors.

    Raises:
        VideoUnavailableError: Video is private, deleted or unavailable.
        GeoBlockedError: Video is blocked in the current region.
        AgeRestrictedError: Video requires cookies to bypass age gate.
        DownloadError: Any other failure (including retryable rate-limits).
    """
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:  # type: ignore[arg-type]
            info = ydl.extract_info(url, download=True)
            if info is None:
                raise DownloadError(url, "yt-dlp returned no info")
            return info
    except yt_dlp.utils.DownloadError as exc:
        msg = str(exc)
        kind = _classify_error(msg)
        if kind is _ErrorKind.UNAVAILABLE:
            raise VideoUnavailableError(url, reason=msg) from exc
        if kind is _ErrorKind.GEO:
            raise GeoBlockedError(url) from exc
        if kind is _ErrorKind.AGE:
            raise AgeRestrictedError(url) from exc
        raise DownloadError(url, reason=msg) from exc


def _make_progress() -> Progress:
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=_CONSOLE,
        transient=True,
    )


class Downloader:
    """High-level download orchestrator.

    Args:
        output_dir: Directory where downloaded files are saved.
        max_height: Optional resolution cap in pixels.
        cookies_file: Path to a Netscape cookies file.
        force: If True, re-download even when the output file already exists.
        workers: Number of parallel downloads for batch operations.
    """

    def __init__(
        self,
        output_dir: Path,
        max_height: int | None = None,
        cookies_file: Path | None = None,
        force: bool = False,
        workers: int = 3,
    ) -> None:
        _check_ffmpeg()
        self.output_dir = output_dir
        self.max_height = max_height
        self.cookies_file = cookies_file
        self.force = force
        self.workers = workers
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def download(self, url: str) -> DownloadResult:
        """Download a single video URL.

        Args:
            url: YouTube watch or shorts URL.

        Returns:
            DownloadResult with outcome details.
        """
        with _make_progress() as progress:
            return self._download_one(url, progress)

    def download_batch(self, urls: list[str]) -> list[DownloadResult]:
        """Download multiple URLs in parallel.

        Args:
            urls: List of YouTube URLs to download.

        Returns:
            List of DownloadResult objects in the same order as *urls*.
        """
        result_map: dict[str, DownloadResult] = {}

        with _make_progress() as progress:
            with ThreadPoolExecutor(max_workers=self.workers) as executor:
                future_to_url = {
                    executor.submit(self._download_one, url, progress): url
                    for url in urls
                }
                for future in as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        result = future.result()
                    except VidGrabError as exc:
                        _CONSOLE.print(f"  [red]✗[/red] {exc}")
                        result = DownloadResult(url=url, success=False, error=str(exc))
                    result_map[url] = result

        # Print results in original input order
        for url in urls:
            result = result_map[url]
            if result.skipped:
                _CONSOLE.print(f"[yellow]↷[/yellow] Already exists: {url}")
            elif result.success and result.output_path:
                _CONSOLE.print(f"[green]✓[/green] {result.output_path.name}")
            else:
                _CONSOLE.print(f"[red]✗[/red] {url}")

        return [result_map[url] for url in urls]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _download_one(self, url: str, progress: Progress) -> DownloadResult:
        """Download a single URL, adding a task to the shared *progress*.

        Args:
            url: YouTube URL.
            progress: Shared Rich Progress instance (thread-safe).

        Returns:
            DownloadResult with outcome details.

        Raises:
            VidGrabError: On any typed download failure.
        """
        if not self.force:
            existing = self._find_existing(url)
            if existing:
                return DownloadResult(url=url, success=True, output_path=existing, skipped=True)

        task_id: TaskID | None = None

        def _hook(d: dict) -> None:
            nonlocal task_id
            status = d.get("status")

            if status == "downloading":
                filename = d.get("filename", "")
                total = d.get("total_bytes") or d.get("total_bytes_estimate")
                done = d.get("downloaded_bytes", 0)
                if task_id is None:
                    label = Path(filename).name[:55] if filename else url[:55]
                    task_id = progress.add_task(f"[cyan]{label}", total=total)
                else:
                    progress.update(task_id, completed=done, total=total)

            elif status == "finished":
                if task_id is not None:
                    progress.update(task_id, completed=d.get("total_bytes", 0))

        info = self._extract_and_download(url, _hook)
        metadata = VideoMetadata.from_yt_dlp_info(info)
        final_path = self._resolve_output_path(info)
        self._write_metadata_json(final_path, metadata)

        return DownloadResult(
            url=url,
            success=True,
            output_path=final_path,
            metadata=metadata,
        )

    def _extract_and_download(self, url: str, hook: Callable[[dict], None]) -> dict:
        """Run yt-dlp download with exponential-backoff retry on rate-limits.

        Args:
            url: YouTube URL.
            hook: Progress hook forwarded to yt-dlp.

        Returns:
            Raw yt-dlp info dict on success.

        Raises:
            VidGrabError: Typed error matching the failure category.
        """
        opts = _build_ydl_opts(self.output_dir, self.max_height, self.cookies_file, hook)

        for attempt in range(_MAX_RETRY_ATTEMPTS):
            try:
                return _run_ydl(url, opts)
            except DownloadError as exc:
                is_last = attempt == _MAX_RETRY_ATTEMPTS - 1
                if _classify_error(exc.reason) is not _ErrorKind.RATE_LIMITED or is_last:
                    raise
                delay = _RETRY_BASE_DELAY * (2**attempt)
                _CONSOLE.print(
                    f"  [yellow]Rate limited — retrying in {delay:.0f}s "
                    f"({attempt + 1}/{_MAX_RETRY_ATTEMPTS})[/yellow]"
                )
                time.sleep(delay)

        raise RuntimeError("unreachable")  # pragma: no cover

    def _resolve_output_path(self, info: dict) -> Path:
        requested = info.get("requested_downloads")
        if requested:
            filepath = requested[0].get("filepath") or requested[0].get("filename")
            if filepath:
                return Path(filepath)

        video_id = info.get("id", "")
        ext = info.get("ext", "mp4")
        matches = list(self.output_dir.glob(f"*{video_id}*.{ext}"))
        if matches:
            return matches[0]
        matches = list(self.output_dir.glob(f"*{video_id}*"))
        if matches:
            return matches[0]

        upload_date = info.get("upload_date", "19700101")
        title = _slugify(info.get("title", "untitled"))
        return self.output_dir / f"{upload_date}-{title}-{video_id}.{ext}"

    def _find_existing(self, url: str) -> Path | None:
        video_id_match = _VIDEO_ID_RE.search(url)
        if not video_id_match:
            return None
        video_id = video_id_match.group(1)
        matches = list(self.output_dir.glob(f"*{video_id}*"))
        matches = [p for p in matches if p.suffix != ".json"]
        return matches[0] if matches else None

    @staticmethod
    def _write_metadata_json(video_path: Path, metadata: VideoMetadata) -> None:
        json_path = video_path.with_suffix(".json")
        json_path.write_text(
            json.dumps(metadata.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
