"""CLI entry point for vidgrab."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from . import __version__
from . import config as _cfg
from .downloader import DownloadConfig, Downloader
from .exceptions import FfmpegNotFoundError
from .models import DownloadResult

app = typer.Typer(
    name="vidgrab",
    help="Download YouTube videos at maximum quality for video editing.",
    add_completion=True,
)
_CONSOLE: Console = Console()
_ERR_CONSOLE: Console = Console(stderr=True)


def _version_callback(value: bool) -> None:
    if value:
        _CONSOLE.print(f"vidgrab {__version__}")
        raise typer.Exit()


@app.command()
def download(
    urls: Annotated[
        list[str] | None,
        typer.Argument(help="One or more YouTube URLs to download."),
    ] = None,
    batch: Annotated[
        Path | None,
        typer.Option(
            "--batch",
            "-b",
            help="Path to a .txt file with one URL per line.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ] = None,
    output_dir: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            help="Directory to save downloaded files (default: ~/Downloads).",
        ),
    ] = None,
    max_height: Annotated[
        int | None,
        typer.Option(
            "--max-height",
            help="Limit video resolution (e.g. 1080 for 1080p). Omit for maximum.",
            min=144,
            max=8640,
        ),
    ] = None,
    playlist: Annotated[
        bool,
        typer.Option(
            "--playlist",
            help="Treat URLs as playlists and download all videos in them.",
        ),
    ] = False,
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            "-f",
            help="Re-download even if the file already exists.",
        ),
    ] = False,
    cookies: Annotated[
        Path | None,
        typer.Option(
            "--cookies",
            help="Path to a Netscape cookies file for age-restricted content.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ] = None,
    workers: Annotated[
        int,
        typer.Option(
            "--workers",
            "-w",
            help="Number of parallel downloads.",
            min=1,
            max=8,
        ),
    ] = 3,
    write_json: Annotated[
        bool,
        typer.Option(
            "--write-json",
            help="Save a .json sidecar file with video metadata alongside each download.",
        ),
    ] = False,
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            help="Show title, resolution and estimated size without downloading.",
        ),
    ] = False,
    quiet: Annotated[
        bool,
        typer.Option(
            "--quiet",
            "-q",
            help="Suppress all output except errors. Useful for scripting.",
        ),
    ] = False,
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            "-V",
            callback=_version_callback,
            is_eager=True,
            help="Show version and exit.",
        ),
    ] = None,
) -> None:
    """Download YouTube videos at the highest available quality.

    \b
    Examples:
      vidgrab https://youtu.be/dQw4w9WgXcQ
      vidgrab https://youtu.be/dQw4w9WgXcQ --max-height 1080
      vidgrab --batch urls.txt --output ~/Videos/raw  (default: ~/Downloads)
      vidgrab https://youtube.com/playlist?list=PLxxx --playlist
    """
    file_cfg = _cfg.load()
    all_urls = _collect_urls(urls, batch)

    _default_output = Path(file_cfg.get("output", Path.home() / "Downloads"))
    config = DownloadConfig(
        output_dir=output_dir if output_dir is not None else _default_output,
        max_height=max_height if max_height is not None else file_cfg.get("max_height"),
        cookies_file=cookies,
        force=force,
        workers=workers if workers != 3 else int(file_cfg.get("workers", 3)),
        write_json=write_json,
        dry_run=dry_run,
        quiet=quiet,
    )
    try:
        dl = Downloader(config)
    except FfmpegNotFoundError as exc:
        _ERR_CONSOLE.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    if playlist:
        all_urls = dl.expand_playlists(all_urls)

    results = dl.download_batch(all_urls)
    if not _print_summary(results, quiet=quiet):
        raise typer.Exit(code=1)


def _collect_urls(positional: list[str] | None, batch_file: Path | None) -> list[str]:
    """Merge positional URL args and batch file into a single list.

    Raises:
        typer.Exit: If no URLs are found.
    """
    all_urls: list[str] = list(positional or [])

    if batch_file:
        lines = batch_file.read_text(encoding="utf-8").splitlines()
        all_urls += [
            line.strip()
            for line in lines
            if line.strip() and not line.startswith("#")
        ]

    if not all_urls:
        _ERR_CONSOLE.print(
            "[red]Error:[/red] provide at least one URL or use --batch <file.txt>."
        )
        raise typer.Exit(code=1)

    return all_urls


def _print_summary(results: list[DownloadResult], *, quiet: bool = False) -> bool:
    """Render the download summary table and list any failed URLs.

    Returns:
        True if all downloads succeeded or were skipped, False if any failed.
    """
    failed = [r for r in results if not r.success]

    if quiet:
        return not failed

    success = [r for r in results if r.success and not r.skipped]
    skipped = [r for r in results if r.skipped]

    _CONSOLE.print()
    table = Table(title="Summary", show_header=True, header_style="bold")
    table.add_column("Status", style="bold", width=10)
    table.add_column("Count", justify="right")
    table.add_row("[green]Downloaded[/green]", str(len(success)))
    table.add_row("[yellow]Skipped[/yellow]",  str(len(skipped)))
    table.add_row("[red]Failed[/red]",          str(len(failed)))
    _CONSOLE.print(table)

    if failed:
        _CONSOLE.print("\n[red]Failed URLs:[/red]")
        for r in failed:
            _CONSOLE.print(f"  • {r.url}")
            if r.error:
                _CONSOLE.print(f"    [dim]{r.error}[/dim]")

    return not failed


def main() -> None:
    """Package entry point."""
    # Show friendly intro when run without arguments
    if len(sys.argv) == 1:
        _CONSOLE.print(
            "[bold cyan]vidgrab[/bold cyan] — Download YouTube videos at maximum quality\n"
        )
        _CONSOLE.print("[dim]Usage:[/dim]")
        _CONSOLE.print("  vidgrab <URL>              Download a single video")
        _CONSOLE.print("  vidgrab --batch urls.txt   Batch download from file")
        _CONSOLE.print("  vidgrab --help             Show all options")
        _CONSOLE.print("  vidgrab --install-completion  Install shell auto-complete\n")
        _CONSOLE.print("[dim]Examples:[/dim]")
        _CONSOLE.print("  vidgrab https://youtu.be/dQw4w9WgXcQ")
        _CONSOLE.print("  vidgrab https://youtu.be/x --dry-run")
        _CONSOLE.print("  vidgrab https://youtu.be/x --max-height 1080")
        _CONSOLE.print(
            "\n[bold]>>> Run [cyan]vidgrab --help[/cyan] for all options[/bold]"
        )
        sys.exit(0)

    app()


if __name__ == "__main__":
    main()
