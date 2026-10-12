"""Safe GitHub release checking and fast-forward updating."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import requests
from InquirerPy import inquirer

from ui.display import display_error, display_info, display_success, display_warning


class AutoUpdater:
    def __init__(self, current_version: str) -> None:
        self.repo_owner = "PyDragonX"
        self.repo_name = "dawnloader-v2"
        self.current_version = current_version
        self.github_api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"
        self.project_root = Path(__file__).resolve().parents[1]

    @staticmethod
    def _version(value: str) -> tuple[int, ...]:
        numbers = re.findall(r"\d+", value)
        return tuple(int(number) for number in numbers) or (0,)

    def is_new_version_available(self, latest_version: str) -> bool:
        return self._version(latest_version) > self._version(self.current_version)

    def check_for_updates(self) -> None:
        display_info("Checking for updates…")
        try:
            response = requests.get(self.github_api_url, timeout=8, headers={"Accept": "application/vnd.github+json"})
            if response.status_code == 404:
                display_warning("No GitHub release found yet; continuing with the current version.")
                return
            response.raise_for_status()
            release = response.json()
            latest = str(release.get("tag_name", "")).lstrip("vV")
            if not latest or not self.is_new_version_available(latest):
                display_success("You are running the latest version.")
                return
            display_warning(f"New version {latest} is available (current: {self.current_version}).")
            if inquirer.confirm(message="Update now using Git?", default=False).execute():
                self.perform_update(release)
        except requests.RequestException as exc:
            display_warning(f"Could not check GitHub updates: {exc}")
        except Exception as exc:
            display_warning(f"Update check skipped: {exc}")

    def _git(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args], cwd=self.project_root, text=True, capture_output=True, check=False
        )

    def perform_update(self, latest_release: dict) -> bool:
        if not (self.project_root / ".git").exists():
            display_warning(f"This copy is not a Git clone. Download: {latest_release.get('html_url', '')}")
            return False
        status = self._git("status", "--porcelain")
        if status.returncode != 0:
            display_error(status.stderr.strip() or "Git is not available.")
            return False
        if status.stdout.strip():
            display_warning("Update cancelled: commit or stash your local changes first.")
            return False
        display_info("Fetching the latest code…")
        fetch = self._git("fetch", "origin", "main", "--prune")
        if fetch.returncode != 0:
            display_error(fetch.stderr.strip() or "Git fetch failed.")
            return False
        pull = self._git("pull", "--ff-only", "origin", "main")
        if pull.returncode != 0:
            display_error(pull.stderr.strip() or "Fast-forward update failed.")
            return False
        requirements = self.project_root / "requirements.txt"
        if requirements.exists():
            pip = subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements)], text=True, capture_output=True, check=False)
            if pip.returncode != 0:
                display_warning("Code updated, but dependency installation failed. Run pip install -r requirements.txt manually.")
        display_success("Update completed. Restart PyDragonX to use the new version.")
        return True
