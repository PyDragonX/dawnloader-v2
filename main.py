#!/usr/bin/env python3

import sys
import time
from ui.display import (
    display_banner, 
    display_platforms_table, 
    display_info, 
    display_error, 
    display_success, 
    select_device_and_os
)
from utils.clipboard_monitor import ClipboardMonitor
from core.engine import MediaDownloader
from utils.updater import AutoUpdater
from utils.config import ConfigManager
from InquirerPy import inquirer

TOOL_VERSION = "1.1.0"

def main():
    display_banner()
    
    # Load or ask for device configuration
    config = ConfigManager.load_config()
    if not config:
        device_type, os_type = select_device_and_os()
        ConfigManager.save_config(device_type, os_type)
        display_success(f"Configuration saved: {device_type} - {os_type}")
    else:
        device_type = config.get("device_type")
        os_type = config.get("os_type")
        display_info(f"Running on: [bold cyan]{device_type} ({os_type})[/bold cyan]")
        
        change_config = inquirer.confirm(
            message="Do you want to change device settings?",
            default=False,
        ).execute()
        if change_config:
            device_type, os_type = select_device_and_os()
            ConfigManager.save_config(device_type, os_type)
            display_success(f"Configuration updated: {device_type} - {os_type}")

    display_platforms_table()
    
    # Check for updates
    updater = AutoUpdater(TOOL_VERSION)
    updater.check_for_updates()

    monitor = ClipboardMonitor()
    downloader = MediaDownloader(device_type, os_type)
    
    display_info("Starting smart clipboard monitor...")
    display_info("Copy a link from YouTube, Instagram, Facebook, or TikTok to begin.")

    while True:
        url = monitor.check_for_media_link()
        if url:
            display_info(f"Detected media link in clipboard: [bold cyan]{url}[/bold cyan]")
            
            action = inquirer.select(
                message="Select action:",
                choices=[
                    "Download Video (MP4)",
                    "Download Audio (MP3)",
                    "Ignore Link",
                    "Exit Tool"
                ],
                default="Download Video (MP4)"
            ).execute()

            if action == "Download Video (MP4)":
                downloader.download(url, file_type="video")
            elif action == "Download Audio (MP3)":
                downloader.download(url, file_type="audio")
            elif action == "Exit Tool":
                display_info("Exiting PyDragonX. Goodbye!")
                sys.exit(0)
            else:
                display_info("Link ignored.")
            
            monitor.last_clipboard_content = url
        
        time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        display_info("\nExiting PyDragonX. Goodbye!")
        sys.exit(0)
    except Exception as e:
        display_error(f"An unexpected error occurred: {e}")
        sys.exit(1)
