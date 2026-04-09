#!/usr/bin/env python3

import sys
import time
from ui.display import (
    display_banner, 
    display_platforms_table, 
    display_info, 
    display_error, 
    display_success, 
    select_device_and_os,
    select_platform,
    select_file_type,
    get_url_input,
    clear_screen
)
from utils.clipboard_monitor import ClipboardMonitor
from core.engine import MediaDownloader
from utils.updater import AutoUpdater
from utils.config import ConfigManager
from InquirerPy import inquirer

TOOL_VERSION = "1.1.0"

def main():
    # 1. Clear screen and show banner
    display_banner()
    
    # 2. Load or ask for device configuration
    config = ConfigManager.load_config()
    if not config:
        device_type, os_type = select_device_and_os()
        ConfigManager.save_config(device_type, os_type)
        display_success(f"Configuration saved: {device_type} - {os_type}")
        time.sleep(1)
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
            time.sleep(1)

    # 3. Silent Update Check
    updater = AutoUpdater(TOOL_VERSION)
    updater.check_for_updates()

    # 4. Initialize components
    monitor = ClipboardMonitor()
    downloader = MediaDownloader(device_type, os_type)
    
    while True:
        display_banner()
        display_platforms_table()
        
        # 5. Professional Workflow: Platform -> File Type -> URL
        platform = select_platform()
        
        if platform == "Exit":
            display_info("Exiting PyDragonX. Goodbye!")
            sys.exit(0)
            
        if platform == "Auto-Detect (Clipboard)":
            display_info("Starting smart clipboard monitor...")
            display_info("Copy a link from YouTube, Instagram, Facebook, or TikTok to begin.")
            
            # Clipboard monitoring loop
            while True:
                url = monitor.check_for_media_link()
                if url:
                    display_info(f"Detected link: [bold cyan]{url}[/bold cyan]")
                    file_type_choice = select_file_type()
                    file_type = "video" if "Video" in file_type_choice else "audio"
                    downloader.download(url, file_type=file_type)
                    monitor.last_clipboard_content = url
                    
                    if not inquirer.confirm(message="Continue monitoring clipboard?", default=True).execute():
                        break
                time.sleep(2)
            continue

        # Manual Input Workflow
        file_type_choice = select_file_type()
        file_type = "video" if "Video" in file_type_choice else "audio"
        url = get_url_input()
        
        # 6. Execute Download
        downloader.download(url, file_type=file_type, selected_platform=platform)
        
        # Ask to continue or exit
        if not inquirer.confirm(message="Do you want to download another file?", default=True).execute():
            display_info("Exiting PyDragonX. Goodbye!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        display_info("\nExiting PyDragonX. Goodbye!")
        sys.exit(0)
    except Exception as e:
        display_error(f"An unexpected error occurred: {e}")
        sys.exit(1)
