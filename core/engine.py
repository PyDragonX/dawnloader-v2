"""Core media downloading engine for PyDragonX."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yt_dlp

from ui.display import (
    console,
    display_error,
    display_info,
    display_success,
    display_warning,
    is_valid_media_url,
    progress,
)
from utils.config import ConfigManager
from utils.dependency_checker import DependencyChecker


class MediaDownloader:
    """Small, isolated wrapper around yt-dlp.

    Every call to :meth:`download` builds a new options dictionary. This is
    important because yt-dlp mutates/reads options and an audio download must
    never affect the following video download.
    """

    def __init__(self, device_type: str, os_type: str) -> None:
        self.device_type = device_type
        self.os_type = os_type
        self.paths = ConfigManager.get_paths(device_type, os_type)
        self.ffmpeg_installed = DependencyChecker.check_ffmpeg()
        self.current_task_id: int | None = None

    @staticmethod
    def detect_platform(url: str) -> str:
        host = (url.split("//", 1)[-1].split("/", 1)[0]).lower()
        host = host.removeprefix("www.")
        platforms = {
            "youtube.com": "YouTube",
            "youtu.be": "YouTube",
            "youtube-nocookie.com": "YouTube",
            "instagram.com": "Instagram",
            "facebook.com": "Facebook",
            "fb.watch": "Facebook",
            "tiktok.com": "TikTok",
            "twitter.com": "Twitter (X)",
            "x.com": "Twitter (X)",
            "kwai.com": "Kwai",
            "soundcloud.com": "SoundCloud",
        }
        for domain, name in platforms.items():
            if host == domain or host.endswith(f".{domain}"):
                return name
        return "Unknown"

    @staticmethod
    def _format_size(value: int | float | None) -> str:
        if not value:
            return "Unknown"
        size = float(value)
        for unit in ("B", "KB", "MB", "GB"):
            if size < 1024 or unit == "GB":
                return f"{size:.2f}{unit}"
            size /= 1024
        return "Unknown"

    def progress_hook(self, status: dict[str, Any]) -> None:
        if self.current_task_id is None:
            return
        state = status.get("status")
        if state == "downloading":
            downloaded = status.get("downloaded_bytes", 0)
            total = status.get("total_bytes") or status.get("total_bytes_estimate")
            progress.update(
                self.current_task_id,
                total=total,
                completed=downloaded,
                downloaded_size=self._format_size(downloaded),
                total_size=self._format_size(total),
            )
        elif state == "finished":
            progress.update(
                self.current_task_id,
                description="[bold green]Processing media…[/bold green]",
                downloaded_size="Complete",
            )

    def _build_options(self, download_path: Path, file_type: str, audio_codec: str) -> dict[str, Any]:
        """Create clean yt-dlp options for one download only."""
        if file_type == "video":
            # Prefer separate best streams, but retain a single-file fallback.
            # Without FFmpeg, requesting separate streams causes merge failures.
            media_format = (
                "bestvideo*+bestaudio/best"
                if self.ffmpeg_installed
                else "best[ext=mp4]/best"
            )
        else:
            media_format = "bestaudio/best"

        options: dict[str, Any] = {
            "format": media_format,
            "outtmpl": str(download_path / "%(title)s.%(ext)s"),
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "ignoreerrors": False,
            "retries": 10,
            "fragment_retries": 10,
            "file_access_retries": 3,
            "continuedl": True,
            "concurrent_fragment_downloads": 4,
            "socket_timeout": 30,
            "progress_hooks": [self.progress_hook],
            "writethumbnail": False,
            "merge_output_format": "mp4" if file_type == "video" else None,
            "postprocessor_args": [
                "-metadata",
                "comment=Downloaded by PyDragonX (https://github.com/PyDragonX)",
                "-metadata",
                "artist=PyDragonX Downloader",
            ],
        }
        if os.name == "nt":
            options["windowsfilenames"] = True

        if not self.ffmpeg_installed:
            options.pop("postprocessor_args", None)
            options.pop("merge_output_format", None)
        elif file_type == "audio":
            options["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": audio_codec,
                    "preferredquality": "192" if audio_codec == "mp3" else None,
                },
                {"key": "FFmpegMetadata"},
            ]
        else:
            options["postprocessors"] = [{"key": "FFmpegMetadata"}]
        return {key: value for key, value in options.items() if value is not None}

    def download(
        self,
        url: str,
        file_type: str = "video",
        selected_platform: str | None = None,
        audio_codec: str = "mp3",
    ) -> bool:
        """Download one media URL and return True only on success."""
        url = url.strip()
        if not is_valid_media_url(url):
            display_error("الرابط غير صالح أو غير مدعوم. تأكد من نسخه كاملًا.")
            return False
        if file_type not in {"video", "audio"}:
            display_error("نوع الملف غير معروف.")
            return False
        if audio_codec not in {"mp3", "wav"}:
            audio_codec = "mp3"

        platform = (
            selected_platform
            if selected_platform and selected_platform != "Auto-Detect (Clipboard)"
            else self.detect_platform(url)
        )
        display_info(f"Target Platform: [bold yellow]{platform}[/bold yellow]")
        if not self.ffmpeg_installed:
            display_warning(
                "FFmpeg غير مثبت؛ سيعمل تنزيل الفيديو الأساسي، لكن الدمج والتحويل إلى MP3/WAV غير متاح."
            )
            if file_type == "audio":
                display_warning("سيتم حفظ الصوت بصيغته الأصلية بدل التحويل.")

        download_path = Path(self.paths["videos"] if file_type == "video" else self.paths["music"])
        download_path.mkdir(parents=True, exist_ok=True)
        options = self._build_options(download_path, file_type, audio_codec)

        with progress:
            self.current_task_id = progress.add_task(
                f"[red]Downloading from {platform}[/red]",
                total=None,
                downloaded_size="0.00B",
                total_size="Calculating…",
            )
            try:
                with yt_dlp.YoutubeDL(options) as ydl:
                    result = ydl.download([url])
                if result not in (None, 0):
                    raise RuntimeError(f"yt-dlp returned exit code {result}")
                progress.update(
                    self.current_task_id,
                    description="[bold green]Download Complete[/bold green]",
                )
                display_success(f"Successfully saved to: {download_path}")
                return True
            except yt_dlp.utils.DownloadError as exc:
                display_error(f"yt-dlp failed: {exc}")
                return False
            except Exception as exc:
                display_error(f"Download failed: {exc}")
                return False
            finally:
                self.current_task_id = None
