"""User config file loader (~/.config/vidgrab/config.toml)."""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

_CONFIG_PATH = Path.home() / ".config" / "vidgrab" / "config.toml"


def load() -> dict[str, Any]:
    """Read ~/.config/vidgrab/config.toml and return its contents.

    Returns an empty dict if the file does not exist.
    Silently ignores parse errors to avoid breaking the CLI on bad config.
    """
    if not _CONFIG_PATH.exists():
        return {}
    try:
        with _CONFIG_PATH.open("rb") as fh:
            return tomllib.load(fh)
    except tomllib.TOMLDecodeError:
        return {}
