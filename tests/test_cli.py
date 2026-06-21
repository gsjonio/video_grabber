"""Tests for vidgrab.cli helpers."""

from __future__ import annotations

from pathlib import Path

import pytest
import typer

from vidgrab.cli import _collect_urls


class TestCollectUrls:
    def test_positional_only(self) -> None:
        urls = _collect_urls(["https://youtu.be/A", "https://youtu.be/B"], None)
        assert urls == ["https://youtu.be/A", "https://youtu.be/B"]

    def test_batch_file(self, tmp_path: Path) -> None:
        batch = tmp_path / "urls.txt"
        batch.write_text("https://youtu.be/A\nhttps://youtu.be/B\n")
        urls = _collect_urls(None, batch)
        assert urls == ["https://youtu.be/A", "https://youtu.be/B"]

    def test_batch_file_ignores_comments(self, tmp_path: Path) -> None:
        batch = tmp_path / "urls.txt"
        batch.write_text("# comment\nhttps://youtu.be/A\n# another\n")
        urls = _collect_urls(None, batch)
        assert urls == ["https://youtu.be/A"]

    def test_batch_file_ignores_blank_lines(self, tmp_path: Path) -> None:
        batch = tmp_path / "urls.txt"
        batch.write_text("\nhttps://youtu.be/A\n\n")
        urls = _collect_urls(None, batch)
        assert urls == ["https://youtu.be/A"]

    def test_merges_positional_and_batch(self, tmp_path: Path) -> None:
        batch = tmp_path / "urls.txt"
        batch.write_text("https://youtu.be/B\n")
        urls = _collect_urls(["https://youtu.be/A"], batch)
        assert urls == ["https://youtu.be/A", "https://youtu.be/B"]

    def test_no_urls_raises_exit(self) -> None:
        with pytest.raises(typer.Exit):
            _collect_urls(None, None)

    def test_empty_positional_and_empty_batch_raises_exit(self, tmp_path: Path) -> None:
        batch = tmp_path / "urls.txt"
        batch.write_text("# only comments\n")
        with pytest.raises(typer.Exit):
            _collect_urls([], batch)
