import requests
import json
import sys
import os
from ui.display import display_info, display_success, display_error, display_warning
from InquirerPy import inquirer

class AutoUpdater:
    def __init__(self, repo_owner, repo_name, current_version):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = current_version
        self.github_api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"

    def check_for_updates(self):
        display_info("Checking for updates...")
        try:
            response = requests.get(self.github_api_url)
            response.raise_for_status() # Raise an exception for HTTP errors
            latest_release = response.json()
            latest_version = latest_release["tag_name"].lstrip("vV") # Remove 'v' or 'V' prefix if present

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
        except requests.exceptions.RequestException as e:
            display_error(f"Failed to check for updates: {e}")
        except KeyError:
            display_error("Could not parse latest release information from GitHub.")

    def is_new_version_available(self, latest_version):
        # Simple version comparison (e.g., 1.1.0 < 1.1.1)
        current_parts = list(map(int, self.current_version.split(".")))
        latest_parts = list(map(int, latest_version.split(".")))

        return latest_parts > current_parts

    def perform_update(self, latest_release):
        display_info("Performing update...")
        # In a real-world scenario, this would involve downloading the new executable/script
        # and replacing the current one. For this example, we'll just simulate it.
        display_warning("Automatic update mechanism is a placeholder. Please update manually from GitHub.")
        display_info(f"Download latest release from: {latest_release['html_url']}")
        # For a more robust solution, consider using a tool like 'pip' for package updates
        # or a custom script to download and replace files.
        sys.exit(0) # Exit after suggesting manual update
