"""Persistent user configuration and download paths."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

CONFIG_FILE = Path.home() / ".pydragonx_config.json"
CONFIG_VERSION = "2.0.0"


class ConfigManager:
    @staticmethod
    def save_config(device_type: str, os_type: str) -> None:
        data = {
            "device_type": device_type,
            "os_type": os_type,
            "version": CONFIG_VERSION,
        }
        temporary = CONFIG_FILE.with_suffix(".tmp")
        temporary.write_text(json.dumps(data, indent=2), encoding="utf-8")
        temporary.replace(CONFIG_FILE)

    @staticmethod
    def load_config() -> dict[str, Any] | None:
        if not CONFIG_FILE.exists():
            return None
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                return None
            return data
        except (OSError, json.JSONDecodeError):
            return None

    @staticmethod
    def get_paths(device_type: str, os_type: str) -> dict[str, str]:
        from utils.path_manager import get_download_paths

        return get_download_paths(device_type, os_type)
