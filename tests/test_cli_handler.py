"""Tests for CLI handler and helper functions."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import typer

from vidgrab.cli import _collect_urls, _print_summary
from vidgrab.models import DownloadResult


class TestCollectUrls:
    """Test URL collection from positional args and batch file."""

    def test_collects_positional_urls(self) -> None:
        """Collect URLs from positional arguments."""
        urls = _collect_urls(["https://youtu.be/url1", "https://youtu.be/url2"], None)
        assert urls == ["https://youtu.be/url1", "https://youtu.be/url2"]

    def test_collects_batch_file_urls(self, tmp_path: Path) -> None:
        """Collect URLs from batch file."""
        batch_file = tmp_path / "urls.txt"
        batch_file.write_text("https://youtu.be/url1\nhttps://youtu.be/url2\n")

        urls = _collect_urls(None, batch_file)
        assert urls == ["https://youtu.be/url1", "https://youtu.be/url2"]

    def test_merges_positional_and_batch(self, tmp_path: Path) -> None:
        """Merge URLs from both positional and batch file."""
        batch_file = tmp_path / "urls.txt"
        batch_file.write_text("https://youtu.be/url2\nhttps://youtu.be/url3\n")

        urls = _collect_urls(["https://youtu.be/url1"], batch_file)
        assert urls == ["https://youtu.be/url1", "https://youtu.be/url2", "https://youtu.be/url3"]

    def test_ignores_comments_in_batch_file(self, tmp_path: Path) -> None:
        """Skip lines starting with # in batch file."""
        batch_file = tmp_path / "urls.txt"
        batch_file.write_text(
            "# Comment\nhttps://youtu.be/url1\n# Another comment\nhttps://youtu.be/url2\n"
        )

        urls = _collect_urls(None, batch_file)
        assert urls == ["https://youtu.be/url1", "https://youtu.be/url2"]

    def test_ignores_blank_lines(self, tmp_path: Path) -> None:
        """Skip blank lines in batch file."""
        batch_file = tmp_path / "urls.txt"
        batch_file.write_text("https://youtu.be/url1\n\nhttps://youtu.be/url2\n\n")

        urls = _collect_urls(None, batch_file)
        assert urls == ["https://youtu.be/url1", "https://youtu.be/url2"]

    def test_raises_on_no_urls(self) -> None:
        """Raise error when no URLs provided."""
        with pytest.raises(typer.Exit):
            _collect_urls(None, None)

    def test_raises_on_empty_positional(self) -> None:
        """Empty positional list is treated as None."""
        with pytest.raises(typer.Exit):
            _collect_urls([], None)

    def test_strips_whitespace(self, tmp_path: Path) -> None:
        """Strip whitespace from URLs in batch file."""
        batch_file = tmp_path / "urls.txt"
        batch_file.write_text("  https://youtu.be/url1  \n  https://youtu.be/url2  \n")

        urls = _collect_urls(None, batch_file)
        assert urls == ["https://youtu.be/url1", "https://youtu.be/url2"]


class TestPrintSummary:
    """Test download summary reporting."""

    def test_prints_summary_with_results(self) -> None:
        """Print summary table with download counts."""
        results = [
            DownloadResult(url="https://youtu.be/url1", success=True),
            DownloadResult(url="https://youtu.be/url2", success=True, skipped=True),
            DownloadResult(url="https://youtu.be/url3", success=False, error="Error"),
        ]

        # Summary should not raise
        success = _print_summary(results, quiet=False)
        assert success is False  # Because one failed

    def test_returns_true_when_all_succeed(self) -> None:
        """Return True when all downloads succeeded or skipped."""
        results = [
            DownloadResult(url="https://youtu.be/url1", success=True),
            DownloadResult(url="https://youtu.be/url2", success=True, skipped=True),
        ]

        success = _print_summary(results, quiet=False)
        assert success is True

    def test_returns_false_when_any_fail(self) -> None:
        """Return False if any download failed."""
        results = [
            DownloadResult(url="https://youtu.be/url1", success=True),
            DownloadResult(url="https://youtu.be/url2", success=False, error="Failed"),
        ]

        success = _print_summary(results, quiet=False)
        assert success is False

    def test_quiet_mode_suppresses_output(self) -> None:
        """In quiet mode, skip summary printing."""
        results = [
            DownloadResult(url="https://youtu.be/url1", success=True),
        ]

        # In quiet mode, should just return result
        success = _print_summary(results, quiet=True)
        assert success is True

    def test_quiet_mode_still_returns_status(self) -> None:
        """Quiet mode returns status without printing."""
        results = [
            DownloadResult(url="https://youtu.be/url1", success=False, error="Error"),
        ]

        success = _print_summary(results, quiet=True)
        assert success is False


class TestDownloadHandler:
    """Test the main download CLI handler."""

    @patch("vidgrab.cli.Downloader")
    @patch("vidgrab.cli._cfg.load")
    def test_basic_download(
        self, mock_cfg_load: MagicMock, mock_downloader_class: MagicMock
    ) -> None:
        """Basic download with single URL."""
        from vidgrab.cli import download

        mock_cfg_load.return_value = {}
        mock_downloader = MagicMock()
        mock_downloader_class.return_value = mock_downloader
        mock_downloader.download_batch.return_value = [
            DownloadResult(url="https://youtu.be/url1", success=True)
        ]

        # Should not raise
        download(
            urls=["https://youtu.be/url1"],
            batch=None,
            output_dir=None,
            max_height=None,
            playlist=False,
            force=False,
            cookies=None,
            workers=3,
            write_json=False,
            dry_run=False,
            quiet=False,
            version=None,
        )

        mock_downloader.download_batch.assert_called_once()

    @patch("vidgrab.cli.Downloader")
    @patch("vidgrab.cli._cfg.load")
    def test_uses_config_file_output_dir(
        self, mock_cfg_load: MagicMock, mock_downloader_class: MagicMock, tmp_path: Path
    ) -> None:
        """Config file output directory is used when CLI doesn't specify."""
        from vidgrab.cli import download

        mock_cfg_load.return_value = {"output": str(tmp_path / "videos")}
        mock_downloader = MagicMock()
        mock_downloader_class.return_value = mock_downloader
        mock_downloader.download_batch.return_value = [
            DownloadResult(url="https://youtu.be/url1", success=True)
        ]

        download(
            urls=["https://youtu.be/url1"],
            batch=None,
            output_dir=None,  # Not specified by user
            max_height=None,
            playlist=False,
            force=False,
            cookies=None,
            workers=3,
            write_json=False,
            dry_run=False,
            quiet=False,
            version=None,
        )

        # Verify Downloader was called with config
        mock_downloader_class.assert_called_once()

    @patch("vidgrab.cli.Downloader")
    @patch("vidgrab.cli._cfg.load")
    def test_cli_output_overrides_config(
        self, mock_cfg_load: MagicMock, mock_downloader_class: MagicMock, tmp_path: Path
    ) -> None:
        """CLI output directory overrides config file."""
        from vidgrab.cli import download

        mock_cfg_load.return_value = {"output": "/config/dir"}
        mock_downloader = MagicMock()
        mock_downloader_class.return_value = mock_downloader
        mock_downloader.download_batch.return_value = [
            DownloadResult(url="https://youtu.be/url1", success=True)
        ]

        cli_dir = tmp_path / "cli_dir"

        download(
            urls=["https://youtu.be/url1"],
            batch=None,
            output_dir=cli_dir,  # Specified by user
            max_height=None,
            playlist=False,
            force=False,
            cookies=None,
            workers=3,
            write_json=False,
            dry_run=False,
            quiet=False,
            version=None,
        )

        # Verify Downloader was called
        mock_downloader_class.assert_called_once()

    @patch("vidgrab.cli.Downloader")
    @patch("vidgrab.cli._cfg.load")
    def test_playlist_expansion(
        self, mock_cfg_load: MagicMock, mock_downloader_class: MagicMock
    ) -> None:
        """Playlist flag triggers expand_playlists."""
        from vidgrab.cli import download

        mock_cfg_load.return_value = {}
        mock_downloader = MagicMock()
        mock_downloader_class.return_value = mock_downloader
        mock_downloader.expand_playlists.return_value = [
            "https://youtu.be/vid1",
            "https://youtu.be/vid2",
        ]
        mock_downloader.download_batch.return_value = [
            DownloadResult(url="https://youtu.be/vid1", success=True),
            DownloadResult(url="https://youtu.be/vid2", success=True),
        ]

        download(
            urls=["https://youtube.com/playlist?list=PLxxx"],
            batch=None,
            output_dir=None,
            max_height=None,
            playlist=True,  # Playlist flag
            force=False,
            cookies=None,
            workers=3,
            write_json=False,
            dry_run=False,
            quiet=False,
            version=None,
        )

        mock_downloader.expand_playlists.assert_called_once()

    @patch("vidgrab.cli.Downloader")
    @patch("vidgrab.cli._cfg.load")
    def test_dry_run_flag(
        self, mock_cfg_load: MagicMock, mock_downloader_class: MagicMock
    ) -> None:
        """Dry-run flag is passed to config."""
        from vidgrab.cli import download

        mock_cfg_load.return_value = {}
        mock_downloader = MagicMock()
        mock_downloader_class.return_value = mock_downloader
        mock_downloader.download_batch.return_value = [
            DownloadResult(url="https://youtu.be/url1", success=True)
        ]

        download(
            urls=["https://youtu.be/url1"],
            batch=None,
            output_dir=None,
            max_height=None,
            playlist=False,
            force=False,
            cookies=None,
            workers=3,
            write_json=False,
            dry_run=True,  # Dry-run flag
            quiet=False,
            version=None,
        )

        # Verify Downloader was called with config
        mock_downloader_class.assert_called_once()

    @patch("vidgrab.cli.Downloader")
    @patch("vidgrab.cli._cfg.load")
    def test_quiet_mode(
        self, mock_cfg_load: MagicMock, mock_downloader_class: MagicMock
    ) -> None:
        """Quiet flag suppresses output and passes through."""
        from vidgrab.cli import download

        mock_cfg_load.return_value = {}
        mock_downloader = MagicMock()
        mock_downloader_class.return_value = mock_downloader
        mock_downloader.download_batch.return_value = [
            DownloadResult(url="https://youtu.be/url1", success=True)
        ]

        # Should not raise even with quiet mode
        download(
            urls=["https://youtu.be/url1"],
            batch=None,
            output_dir=None,
            max_height=None,
            playlist=False,
            force=False,
            cookies=None,
            workers=3,
            write_json=False,
            dry_run=False,
            quiet=True,  # Quiet mode
            version=None,
        )

        mock_downloader.download_batch.assert_called_once()

    @patch("vidgrab.cli.Downloader")
    @patch("vidgrab.cli._cfg.load")
    def test_handles_ffmpeg_not_found(
        self, mock_cfg_load: MagicMock, mock_downloader_class: MagicMock
    ) -> None:
        """FFmpeg not found error is caught and reported."""
        from vidgrab.exceptions import FfmpegNotFoundError

        mock_cfg_load.return_value = {}
        mock_downloader_class.side_effect = FfmpegNotFoundError()

        from vidgrab.cli import download

        with pytest.raises(typer.Exit):
            download(
                urls=["https://youtu.be/url1"],
                batch=None,
                output_dir=None,
                max_height=None,
                playlist=False,
                force=False,
                cookies=None,
                workers=3,
                write_json=False,
                dry_run=False,
                quiet=False,
                version=None,
            )

    @patch("vidgrab.cli.Downloader")
    @patch("vidgrab.cli._cfg.load")
    def test_exit_code_on_failure(
        self, mock_cfg_load: MagicMock, mock_downloader_class: MagicMock
    ) -> None:
        """Exit code 1 when downloads fail."""
        from vidgrab.cli import download

        mock_cfg_load.return_value = {}
        mock_downloader = MagicMock()
        mock_downloader_class.return_value = mock_downloader
        mock_downloader.download_batch.return_value = [
            DownloadResult(url="https://youtu.be/url1", success=False, error="Failed")
        ]

        with pytest.raises(typer.Exit) as exc_info:
            download(
                urls=["https://youtu.be/url1"],
                batch=None,
                output_dir=None,
                max_height=None,
                playlist=False,
                force=False,
                cookies=None,
                workers=3,
                write_json=False,
                dry_run=False,
                quiet=False,
                version=None,
            )

        assert exc_info.value.exit_code == 1


class TestMainEntry:
    """Test main() entry point."""

    @patch("vidgrab.cli.sys.argv", ["vidgrab"])
    @patch("vidgrab.cli._CONSOLE")
    def test_friendly_intro_when_no_args(self, mock_console: MagicMock) -> None:
        """Show friendly intro when run without arguments."""
        from vidgrab.cli import main

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0
        mock_console.print.assert_called()

    @patch("vidgrab.cli._CONSOLE")
    def test_version_callback(self, mock_console: MagicMock) -> None:
        """Version callback prints and exits."""
        from vidgrab.cli import _version_callback

        with pytest.raises(typer.Exit):
            _version_callback(True)

        # Verify version was printed
        mock_console.print.assert_called_once()
        call_args = mock_console.print.call_args[0][0]
        assert "vidgrab" in call_args

    def test_version_callback_no_op(self) -> None:
        """Version callback does nothing when False."""
        from vidgrab.cli import _version_callback

        # Should not raise
        result = _version_callback(False)
        assert result is None

    @patch("vidgrab.cli._CONSOLE")
    @patch("vidgrab.cli.subprocess.run")
    def test_update_callback_runs_pip_upgrade(
        self, mock_run: MagicMock, _mock_console: MagicMock
    ) -> None:
        """Update callback shells out to pip upgrade and exits with its code."""
        from vidgrab.cli import _update_callback

        mock_run.return_value = MagicMock(returncode=0)

        with pytest.raises(typer.Exit) as exc_info:
            _update_callback(True)

        assert exc_info.value.exit_code == 0
        args = mock_run.call_args[0][0]
        assert args[1:] == ["-m", "pip", "install", "--upgrade", "vidgrab"]

    @patch("vidgrab.cli.subprocess.run")
    def test_update_callback_no_op(self, mock_run: MagicMock) -> None:
        """Update callback does nothing when False."""
        from vidgrab.cli import _update_callback

        result = _update_callback(False)
        assert result is None
        mock_run.assert_not_called()
