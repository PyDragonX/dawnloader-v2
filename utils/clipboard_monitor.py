import pyperclip
import re
import time

class ClipboardMonitor:
    def __init__(self):
        self.last_clipboard_content = ""
        self.url_pattern = re.compile(r'https?://[^"\s]+')

    def get_clipboard_content(self):
        try:
            return pyperclip.paste()
        except pyperclip.PyperclipException:
            return ""

    def check_for_media_link(self):
        current_clipboard_content = self.get_clipboard_content()
        if current_clipboard_content and current_clipboard_content != self.last_clipboard_content:
            self.last_clipboard_content = current_clipboard_content
            match = self.url_pattern.search(current_clipboard_content)
            if match:
                return match.group(0)
        return None

    def start_monitoring(self, interval=2):
        while True:
            url = self.check_for_media_link()
            if url:
                return url
            time.sleep(interval)
