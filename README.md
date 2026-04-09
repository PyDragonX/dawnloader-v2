# 🐉 PyDragonX - The Professional All-in-One Media Downloader Tool

**Version:** `1.1.0` | **Developer:** `PyDragonX` | **Environment:** `Command Line Interface (Terminal/Termux)`

---

## 📋 Overview
PyDragonX is a powerful, professional-grade media downloader built with Python. It leverages the robust `yt-dlp` engine to provide high-speed downloads from various platforms while offering a sophisticated and user-friendly terminal interface.

## ✨ Key Features
*   **📱 Device Selection:** Choose between Phone (Android/Termux, iOS) or Laptop/PC (Windows, Linux, macOS) for tailored environment setup.
*   **🔍 Smart Clipboard Monitor:** Automatically detects media links in your clipboard for instant download prompts.
*   **🌐 Platform Detection:** Automatically identifies links from YouTube, Instagram, Facebook, and TikTok.
*   **📁 Auto-Sorting:** Automatically organizes downloads into `Music` and `Videos` folders based on file type and OS.
*   **📊 Advanced Progress UI:** Beautiful, color-coded progress bars showing speed, size, and ETA.
*   **🛡️ Metadata Injection:** Automatically adds developer credits and metadata to downloaded files.
*   **🚀 Auto-Updater:** Built-in system to check for the latest versions from the official repository.

## 🛠️ Installation

### Prerequisites
*   Python 3.10 or higher
*   FFmpeg (for high-quality merging and conversion)

### Setup
1.  Clone the repository:
    ```bash
    git clone https://github.com/PyDragonX/dawnloader-v2
    cd dawnloader-v2
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the tool:
    ```bash
    python main.py
    ```

## 📂 Project Structure
*   `core/`: The heart of the downloader engine and processing logic.
*   `ui/`: Handles the rich terminal interface, banners, and tables.
*   `utils/`: Contains helper modules for clipboard monitoring, path management, configuration, and updates.
*   `main.py`: The main entry point of the application.

---
**PyDragonX: Precision, Power, and Professionalism in Your Terminal.**
[GitHub Repository](https://github.com/PyDragonX/dawnloader-v2)
