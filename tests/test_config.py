"""Tests for vidgrab.config loader."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from vidgrab import config as _cfg


class TestLoad:
    def test_returns_empty_when_file_missing(self, tmp_path: Path) -> None:
        missing = tmp_path / "config.toml"
        with patch.object(_cfg, "_CONFIG_PATH", missing):
            assert _cfg.load() == {}

    def test_reads_valid_toml(self, tmp_path: Path) -> None:
        cfg_file = tmp_path / "config.toml"
        cfg_file.write_text('output = "/tmp/videos"\nworkers = 5\n')
        with patch.object(_cfg, "_CONFIG_PATH", cfg_file):
            data = _cfg.load()
        assert data["output"] == "/tmp/videos"
        assert data["workers"] == 5

    def test_returns_empty_on_invalid_toml(self, tmp_path: Path) -> None:
        cfg_file = tmp_path / "config.toml"
        cfg_file.write_text("not valid toml ][")
        with patch.object(_cfg, "_CONFIG_PATH", cfg_file):
            assert _cfg.load() == {}
