import os

def get_download_path(file_type):
    if os.environ.get('TERMUX_VERSION'):
        # Termux specific paths
        if file_type == 'audio':
            return os.path.join(os.path.expanduser('~'), 'storage', 'music')
        elif file_type == 'video':
            return os.path.join(os.path.expanduser('~'), 'storage', 'shared', 'Videos')
    else:
        # Windows/Linux specific paths
        if file_type == 'audio':
            return os.path.join(os.path.expanduser('~'), 'Music')
        elif file_type == 'video':
            return os.path.join(os.path.expanduser('~'), 'Videos')
    return os.path.join(os.path.expanduser('~'), 'Downloads') # Fallback

def create_download_directories():
    audio_path = get_download_path('audio')
    video_path = get_download_path('video')
    os.makedirs(audio_path, exist_ok=True)
    os.makedirs(video_path, exist_ok=True)
    return audio_path, video_path
