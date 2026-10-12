#!/usr/bin/env python3
"""PyDragonX application entry point."""

import sys
import time

from InquirerPy import inquirer

from core.engine import MediaDownloader
from ui.display import (
    clear_screen,
    display_banner,
    display_error,
    display_info,
    display_platforms_table,
    display_success,
    select_device_and_os,
    select_file_type,
    select_platform,
    get_url_input,
)
from utils.clipboard_monitor import ClipboardMonitor
from utils.config import ConfigManager
from utils.dependency_checker import DependencyChecker
from utils.updater import AutoUpdater

TOOL_VERSION = "2.0.0"


def parse_file_choice(choice: str) -> tuple[str, str]:
    if "Video" in choice:
        return "video", "mp4"
    return "audio", ("wav" if "WAV" in choice else "mp3")


def download_from_clipboard(monitor: ClipboardMonitor, downloader: MediaDownloader) -> None:
    display_info("Starting smart clipboard monitor… Copy a supported media link.")
    while True:
        url = monitor.check_for_media_link()
        if url:
            display_info(f"Detected link: [bold cyan]{url}[/bold cyan]")
            choice = select_file_type()
            file_type, codec = parse_file_choice(choice)
            downloader.download(url, file_type=file_type, audio_codec=codec)
            if not inquirer.confirm(message="Continue monitoring clipboard?", default=True).execute():
                return
        time.sleep(2)


def main() -> None:
    display_banner()
    DependencyChecker.verify_all()
    time.sleep(0.5)

    config = ConfigManager.load_config()
    if not config:
        device_type, os_type = select_device_and_os()
        ConfigManager.save_config(device_type, os_type)
        display_success(f"Configuration saved: {device_type} - {os_type}")
    else:
        device_type = config.get("device_type", "Laptop/PC")
        os_type = config.get("os_type", "Linux")
        display_info(f"Running on: [bold cyan]{device_type} ({os_type})[/bold cyan]")
        if inquirer.confirm(message="Do you want to change device settings?", default=False).execute():
            device_type, os_type = select_device_and_os()
            ConfigManager.save_config(device_type, os_type)

    AutoUpdater(TOOL_VERSION).check_for_updates()
    monitor = ClipboardMonitor()
    downloader = MediaDownloader(device_type, os_type)

    while True:
        display_banner()
        display_platforms_table()
        platform = select_platform()
        if platform == "Exit":
            display_info("Exiting PyDragonX. Goodbye!")
            return
        if platform == "Auto-Detect (Clipboard)":
            download_from_clipboard(monitor, downloader)
            continue

        choice = select_file_type()
        file_type, codec = parse_file_choice(choice)
        url = get_url_input()
        downloader.download(url, file_type=file_type, selected_platform=platform, audio_codec=codec)
        if not inquirer.confirm(message="Download another file?", default=True).execute():
            display_info("Exiting PyDragonX. Goodbye!")
            return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        display_info("\nExiting PyDragonX. Goodbye!")
        sys.exit(0)
    except Exception as exc:
        display_error(f"An unexpected error occurred: {exc}")
        sys.exit(1)
