import yt_dlp
import os
import re
from ui.display import progress, console, display_error, display_success, display_info, display_warning
from utils.config import ConfigManager
from utils.dependency_checker import DependencyChecker

class MediaDownloader:
    def __init__(self, device_type, os_type):
        self.device_type = device_type
        self.os_type = os_type
        self.paths = ConfigManager.get_paths(device_type, os_type)
        self.ffmpeg_installed = DependencyChecker.check_ffmpeg()
        
        self.ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'noplaylist': True,
            'progress_hooks': [self.progress_hook],
            'postprocessors': [{
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            }],
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
        }
        self.current_task_id = None

    def detect_platform(self, url):
        url = url.lower()
        if "youtube.com" in url or "youtu.be" in url:
            return "YouTube"
        elif "instagram.com" in url:
            return "Instagram"
        elif "facebook.com" in url or "fb.watch" in url:
            return "Facebook"
        elif "tiktok.com" in url:
            return "TikTok"
        elif "twitter.com" in url or "x.com" in url:
            return "Twitter (X)"
        elif "kwai.com" in url:
            return "Kwai"
        elif "soundcloud.com" in url:
            return "SoundCloud"
        return "Unknown"

    def progress_hook(self, d):
        if self.current_task_id is None:
            return

        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes', 0)
            
            downloaded_size = f"{downloaded_bytes / (1024*1024):.2f}MB"
            total_size = f"{total_bytes / (1024*1024):.2f}MB" if total_bytes else "Unknown"

            progress.update(
                self.current_task_id,
                total=total_bytes,
                completed=downloaded_bytes,
                downloaded_size=downloaded_size,
                total_size=total_size
            )
        elif d['status'] == 'finished':
            progress.update(self.current_task_id, description="[bold green]Download Complete[/bold green]")
            self.current_task_id = None

    def download(self, url, file_type='video', selected_platform=None):
        platform = selected_platform if selected_platform and selected_platform != "Auto-Detect (Clipboard)" else self.detect_platform(url)
        display_info(f"Target Platform: [bold yellow]{platform}[/bold yellow]")
        
        download_path = self.paths['videos'] if file_type == 'video' else self.paths['music']
        os.makedirs(download_path, exist_ok=True)
        
        self.ydl_opts['outtmpl'] = os.path.join(download_path, '%(title)s.%(ext)s')
        
        # Audio conversion if MP3 is selected
        if file_type == 'audio':
            self.ydl_opts['format'] = 'bestaudio/best'
            if self.ffmpeg_installed:
                self.ydl_opts['postprocessors'].insert(0, {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                })
            else:
                display_warning("FFmpeg not found. Downloading in original audio format instead of MP3.")
        
        # Inject metadata credits
        self.ydl_opts['postprocessor_args'] = [
            '-metadata', f'comment=Downloaded by PyDragonX (https://github.com/PyDragonX)',
            '-metadata', 'artist=PyDragonX Downloader'
        ]

        with progress:
            self.current_task_id = progress.add_task(
                f"[red]Downloading from {platform}[/red]", 
                total=None, 
                downloaded_size="0.00MB", 
                total_size="Calculating..."
            )
            try:
                with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                    ydl.download([url])
                display_success(f"Successfully saved to: {download_path}")
            except Exception as e:
                display_error(f"Download failed: {e}")
                if self.current_task_id:
                    progress.remove_task(self.current_task_id)
                self.current_task_id = None
