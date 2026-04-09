#!/usr/bin/env python3

import sys
import time
from ui.display import display_banner, display_platforms_table, display_info, display_error, display_success
from utils.clipboard_monitor import ClipboardMonitor
from core.engine import MediaDownloader
from utils.updater import AutoUpdater
from InquirerPy import inquirer

TOOL_VERSION = "1.1.0"
REPO_OWNER = "PyDragonX"
REPO_NAME = "PyDragonX" # Assuming the repo name is also PyDragonX

def main():
    display_banner()
    display_platforms_table()
    display_info("Welcome to PyDragonX - The Professional All-in-One Media Downloader Tool!")

    updater = AutoUpdater(REPO_OWNER, REPO_NAME, TOOL_VERSION)
    updater.check_for_updates()

    monitor = ClipboardMonitor()
    downloader = MediaDownloader()
    display_info("Starting smart clipboard monitor...")

    while True:
        url = monitor.check_for_media_link()
        if url:
            display_info(f"Detected media link in clipboard: {url}")
            confirm_download = inquirer.confirm(
                message="Do you want to download this media?",
                default=True,
            ).execute()

            if confirm_download:
                display_success(f"User confirmed download for: {url}")
                # Determine file type (simple heuristic for now, can be improved)
                if any(ext in url for ext in [".mp3", ".wav", ".ogg"]):
                    file_type = "audio"
                else:
                    file_type = "video"
                
                downloader.download(url, file_type=file_type)
            else:
                display_info("Download cancelled by user.")
            monitor.last_clipboard_content = url # Prevent re-prompting for the same URL
        time.sleep(2) # Check clipboard every 2 seconds


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        display_info("Exiting PyDragonX. Goodbye!")
        sys.exit(0)
    except Exception as e:
        display_error(f"An unexpected error occurred: {e}")
        sys.exit(1)
