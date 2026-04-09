import requests
import sys
import os
from ui.display import display_info, display_success, display_error, display_warning
from InquirerPy import inquirer

class AutoUpdater:
    def __init__(self, current_version):
        self.repo_owner = "PyDragonX"
        self.repo_name = "dawnloader-v2"
        self.current_version = current_version
        self.github_api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"

    def check_for_updates(self):
        display_info("Checking for updates...")
        try:
            response = requests.get(self.github_api_url, timeout=10)
            if response.status_code == 404:
                display_warning("Update server not found (404). Please check the repository manually.")
                return
            
            response.raise_for_status()
            latest_release = response.json()
            latest_version = latest_release["tag_name"].lstrip("vV")

            if self.is_new_version_available(latest_version):
                display_warning(f"New version ({latest_version}) available! Current version: {self.current_version}")
                confirm_update = inquirer.confirm(
                    message="Do you want to update now?",
                    default=True,
                ).execute()
                if confirm_update:
                    self.perform_update(latest_release)
                else:
                    display_info("Update skipped by user.")
            else:
                display_success("You are running the latest version.")
        except Exception as e:
            display_error(f"Failed to check for updates: {e}")

    def is_new_version_available(self, latest_version):
        try:
            current_parts = list(map(int, self.current_version.split(".")))
            latest_parts = list(map(int, latest_version.split(".")))
            return latest_parts > current_parts
        except:
            return False

    def perform_update(self, latest_release):
        display_info("Performing update...")
        display_warning("Automatic update mechanism is a placeholder. Please update manually from GitHub.")
        display_info(f"Download latest release from: {latest_release['html_url']}")
        sys.exit(0)
