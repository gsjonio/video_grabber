"""CLI entry point for vidgrab."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from . import __version__
from .downloader import Downloader
from .exceptions import FfmpegNotFoundError

app = typer.Typer(
    name="vidgrab",
    help="Download YouTube videos at maximum quality for video editing.",
    add_completion=False,
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
        Optional[list[str]],
        typer.Argument(help="One or more YouTube URLs to download."),
    ] = None,
    batch: Annotated[
        Optional[Path],
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
        Path,
        typer.Option(
            "--output",
            "-o",
            help="Directory to save downloaded files.",
        ),
    ] = Path("."),
    max_height: Annotated[
        Optional[int],
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
        Optional[Path],
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
    version: Annotated[
        Optional[bool],
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
      vidgrab --batch urls.txt --output ~/Videos/raw
      vidgrab https://youtube.com/playlist?list=PLxxx --playlist
    """
    # Collect all URLs from positional args and/or batch file
    all_urls: list[str] = list(urls or [])

    if batch:
        lines = batch.read_text(encoding="utf-8").splitlines()
        batch_urls = [line.strip() for line in lines if line.strip() and not line.startswith("#")]
        all_urls.extend(batch_urls)

    if not all_urls:
        _ERR_CONSOLE.print(
            "[red]Error:[/red] provide at least one URL or use --batch <file.txt>."
        )
        raise typer.Exit(code=1)

    try:
        dl = Downloader(
            output_dir=output_dir,
            max_height=max_height,
            cookies_file=cookies,
            force=force,
            workers=workers,
        )
    except FfmpegNotFoundError as exc:
        _ERR_CONSOLE.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    if playlist:
        all_urls = dl.expand_playlists(all_urls)

    results = dl.download_batch(all_urls)

    # Summary table
    success = [r for r in results if r.success and not r.skipped]
    skipped = [r for r in results if r.skipped]
    failed = [r for r in results if not r.success]

    _CONSOLE.print()
    table = Table(title="Summary", show_header=True, header_style="bold")
    table.add_column("Status", style="bold", width=10)
    table.add_column("Count", justify="right")
    table.add_row("[green]Downloaded[/green]", str(len(success)))
    table.add_row("[yellow]Skipped[/yellow]", str(len(skipped)))
    table.add_row("[red]Failed[/red]", str(len(failed)))
    _CONSOLE.print(table)

    if failed:
        _CONSOLE.print("\n[red]Failed URLs:[/red]")
        for r in failed:
            _CONSOLE.print(f"  • {r.url}")
            if r.error:
                _CONSOLE.print(f"    [dim]{r.error}[/dim]")
        raise typer.Exit(code=1)


def main() -> None:
    """Package entry point."""
    app()


if __name__ == "__main__":
    main()
