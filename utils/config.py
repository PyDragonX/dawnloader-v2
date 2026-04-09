import json
import os
from pathlib import Path

CONFIG_FILE = Path.home() / ".pydragonx_config.json"

class ConfigManager:
    @staticmethod
    def save_config(device_type, os_type):
        config = {
            "device_type": device_type,
            "os_type": os_type,
            "version": "1.1.0"
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)

    @staticmethod
    def load_config():
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        return None

    @staticmethod
    def get_paths(device_type, os_type):
        home = str(Path.home())
        paths = {
            "music": os.path.join(home, "Music"),
            "videos": os.path.join(home, "Videos")
        }
        
        if device_type == "Phone" or os_type == "Android (Termux)":
            # Termux specific paths
            termux_storage = os.path.join(home, "storage")
            paths["music"] = os.path.join(termux_storage, "music")
            paths["videos"] = os.path.join(termux_storage, "shared", "Movies")
            
        return paths
