import shutil
import os
import sys
from ui.display import display_error, display_warning, display_info

class DependencyChecker:
    @staticmethod
    def check_ffmpeg():
        """Checks if FFmpeg is installed and accessible."""
        ffmpeg_path = shutil.which("ffmpeg")
        if ffmpeg_path:
            return True
        return False

    @staticmethod
    def get_install_instructions():
        """Returns installation instructions based on the OS."""
        if os.name == 'nt': # Windows
            return "Download FFmpeg from https://ffmpeg.org/download.html and add it to your PATH."
        elif sys.platform == "darwin": # macOS
            return "Install via Homebrew: 'brew install ffmpeg'"
        else: # Linux / Android (Termux)
            if os.environ.get('TERMUX_VERSION'):
                return "Install via Termux: 'pkg install ffmpeg'"
            return "Install via your package manager: 'sudo apt install ffmpeg' or 'sudo pacman -S ffmpeg'"

    @classmethod
    def verify_all(cls):
        """Verifies all dependencies and warns the user if missing."""
        if not cls.check_ffmpeg():
            display_warning("FFmpeg is NOT installed! High-quality merging and audio conversion will fail.")
            display_info(f"Instructions: {cls.get_install_instructions()}")
            return False
        return True
