"""Cross-platform download path management."""

from __future__ import annotations

import os
from pathlib import Path


def get_download_paths(device_type: str | None = None, os_type: str | None = None) -> dict[str, str]:
    home = Path.home()
    is_termux = bool(os.environ.get("TERMUX_VERSION")) or os_type == "Android (Termux)"
    if is_termux:
        root = home / "storage"
        return {"music": str(root / "music"), "videos": str(root / "shared" / "Movies")}
    return {"music": str(home / "Music"), "videos": str(home / "Videos")}


def get_download_path(file_type: str, device_type: str | None = None, os_type: str | None = None) -> str:
    paths = get_download_paths(device_type, os_type)
    return paths.get(file_type, str(Path.home() / "Downloads"))


def create_download_directories(device_type: str | None = None, os_type: str | None = None) -> tuple[str, str]:
    paths = get_download_paths(device_type, os_type)
    Path(paths["music"]).mkdir(parents=True, exist_ok=True)
    Path(paths["videos"]).mkdir(parents=True, exist_ok=True)
    return paths["music"], paths["videos"]
