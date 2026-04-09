import yt_dlp
import os
from ui.display import progress, console, display_error, display_success
from utils.path_manager import get_download_path

class MediaDownloader:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'noplaylist': True,
            'progress_hooks': [self.progress_hook],
            'outtmpl': {'default': '%(title)s.%(ext)s'},
            'postprocessors': [{
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            }],
        }
        self.current_task_id = None

    def progress_hook(self, d):
        if self.current_task_id is None:
            return

        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes', 0)
            
            # Prepare fields for Rich progress bar
            downloaded_size = f"{downloaded_bytes / (1024*1024):.2f}MB"
            total_size = f"{total_bytes / (1024*1024):.2f}MB" if total_bytes else "Unknown"

            if total_bytes:
                progress.update(
                    self.current_task_id,
                    total=total_bytes,
                    completed=downloaded_bytes,
                    downloaded_size=downloaded_size,
                    total_size=total_size
                )
            else:
                progress.update(
                    self.current_task_id,
                    completed=downloaded_bytes,
                    downloaded_size=downloaded_size,
                    total_size=total_size
                )
        elif d['status'] == 'finished':
            # Ensure the progress bar reaches 100%
            progress.update(self.current_task_id, description="[bold green]Download Complete[/bold green]")
            display_success(f"Download finished for {d['filename']}")
            self.current_task_id = None

    def download(self, url, file_type='video'):
        download_path = get_download_path(file_type)
        self.ydl_opts['outtmpl']['default'] = os.path.join(download_path, '%(title)s.%(ext)s')

        with progress:
            # Initialize task with default values for fields to avoid KeyError
            self.current_task_id = progress.add_task(
                "[red]Downloading[/red]", 
                total=None, 
                downloaded_size="0.00MB", 
                total_size="Calculating..."
            )
            try:
                with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                    ydl.download([url])
            except Exception as e:
                display_error(f"Download failed: {e}")
                if self.current_task_id:
                    progress.remove_task(self.current_task_id)
                self.current_task_id = None
