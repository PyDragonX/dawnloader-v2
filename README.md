# 🐉 PyDragonX Dawnloader

> **Professional All-in-One Media Downloader powered by yt-dlp and Rich**
>
> **أداة احترافية شاملة لتنزيل الوسائط باستخدام yt-dlp وRich**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Powered by yt-dlp](https://img.shields.io/badge/Powered%20by-yt--dlp-red)](https://github.com/yt-dlp/yt-dlp)
[![Platforms](https://img.shields.io/badge/Platforms-Linux%20%7C%20Windows%20%7C%20Termux-success)](https://github.com/PyDragonX/dawnloader-v2)
[![License](https://img.shields.io/badge/License-Check%20repository-lightgrey)](https://github.com/PyDragonX/dawnloader-v2)

---

## English

### Overview

**PyDragonX Dawnloader** is a professional command-line media downloader built with Python, `yt-dlp`, and `Rich`. It provides a clean terminal workflow, automatic platform detection, organized download folders, reliable retries, and audio conversion through FFmpeg.

The project is designed for Linux, Windows, macOS, and Android/Termux users while keeping the code modular and easy to extend.

### Key Features

- **Video downloads:** Best available video and audio quality with automatic merging.
- **Audio downloads:** MP3 for compressed audio and WAV for lossless audio.
- **Multi-platform support:** YouTube, Instagram, Facebook, TikTok, X/Twitter, Kwai, and SoundCloud, depending on the URL and current `yt-dlp` support.
- **YouTube improvements:** Separate best video/audio streams, MP4 merging, retries, fragment retries, continued downloads, and better error handling.
- **Smart clipboard mode:** Detects copied media links and offers an immediate download workflow.
- **Cross-platform paths:** Automatically uses `Music` and `Videos` on desktop systems and shared storage paths on Termux.
- **Rich terminal UI:** Progress bars, transfer speed, file size, ETA, status messages, and platform tables.
- **Metadata:** Adds PyDragonX metadata to processed media when FFmpeg is available.
- **Safe updates:** Checks GitHub releases and updates clean Git copies with fast-forward Git operations.
- **Modular architecture:** Separate engine, UI, configuration, path management, clipboard, dependency, and update modules.

### Supported output formats

| Type | Output | FFmpeg | Use case |
|---|---|---:|---|
| Video | MP4 / best available | Recommended | Video with merged audio |
| Audio | MP3 | Required for conversion | Small, compatible audio files |
| Audio | WAV | Required for conversion | Lossless audio editing and archiving |

### Requirements

- Python **3.10 or newer**
- FFmpeg recommended, and required for:
  - merging separate YouTube video/audio streams;
  - converting audio to MP3;
  - converting audio to WAV;
  - embedding metadata.
- Internet connection

### Installation

#### Linux / macOS

```bash
git clone https://github.com/PyDragonX/dawnloader-v2.git
cd dawnloader-v2

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python main.py
```

Install FFmpeg on Debian/Ubuntu:

```bash
sudo apt update
sudo apt install ffmpeg
```

Install FFmpeg on Arch:

```bash
sudo pacman -S ffmpeg
```

#### Windows

```powershell
git clone https://github.com/PyDragonX/dawnloader-v2.git
cd dawnloader-v2

py -m venv .venv
.venv\Scripts\activate
py -m pip install --upgrade pip
py -m pip install -r requirements.txt

py main.py
```

Install FFmpeg with [winget](https://learn.microsoft.com/windows/package-manager/winget/):

```powershell
winget install Gyan.FFmpeg
```

#### Android / Termux

```bash
pkg update
pkg install python ffmpeg git

git clone https://github.com/PyDragonX/dawnloader-v2.git
cd dawnloader-v2

termux-setup-storage
python -m pip install -r requirements.txt
python main.py
```

### Updating without deleting the project

PyDragonX is designed to be updated through Git. Your local files do not need to be deleted:

```bash
cd dawnloader-v2
git status
git pull --ff-only origin main
python -m pip install -r requirements.txt
python main.py
```

If you have local changes, save them first:

```bash
git add .
git commit -m "Save local changes"
git pull --ff-only origin main
```

Or temporarily stash them:

```bash
git stash push -m "Local PyDragonX changes"
git pull --ff-only origin main
git stash pop
```

The built-in updater refuses to overwrite a working tree with uncommitted changes.

### YouTube troubleshooting

1. Update `yt-dlp`:

   ```bash
   python -m pip install --upgrade yt-dlp
   ```

2. Make sure FFmpeg is installed and available in `PATH`:

   ```bash
   ffmpeg -version
   ```

3. For 1080p and higher, YouTube commonly provides video and audio separately. FFmpeg is required to merge them.
4. A private, age-restricted, region-restricted, or login-only video may require an authorized browser session. Only use access you are legally permitted to use.
5. If a video was removed or made private, no downloader can retrieve it through a normal public URL.
6. Do not commit passwords, tokens, or Cookies files to GitHub.

### Project structure

```text
main.py                    Application entry point and workflow
core/
  engine.py                Isolated yt-dlp download engine
ui/
  display.py               Rich UI, prompts, URL validation, progress
utils/
  config.py                Persistent user configuration
  path_manager.py          Cross-platform download paths
  clipboard_monitor.py     Clipboard link detection
  dependency_checker.py    FFmpeg checks
  updater.py               GitHub and Git update logic
requirements.txt            Python dependencies
.gitignore                  Local, cache, and downloaded-file exclusions
README.md                   Project documentation
```

### Roadmap

- Download queue with pause, resume, retry, and cancellation.
- Resolution, codec, container, bitrate, and subtitle selectors.
- Playlist and channel downloads with duplicate detection.
- Download history backed by SQLite.
- Optional authorized Cookies-file support with local-only storage.
- Structured logs and exportable error reports.
- Automated tests and CI for Linux, Windows, and Termux.
- Optional TUI dashboard or local web API.

### Legal and responsible use

Use PyDragonX only for media you own, have permission to download, or that the platform explicitly makes available for download. Respect copyright, privacy, platform terms, and local laws.

---

## العربية

### نبذة عن المشروع

**PyDragonX Dawnloader** هي أداة احترافية تعمل من سطر الأوامر لتنزيل الوسائط باستخدام Python و`yt-dlp` و`Rich`. توفر الأداة واجهة طرفية منظمة، واكتشافًا تلقائيًا للمنصة، ومجلدات مرتبة، ومحاولات إعادة تلقائية، وتحويلًا للصوت بواسطة FFmpeg.

تم تصميم المشروع ليعمل على Linux وWindows وmacOS وAndroid/Termux، مع بنية برمجية منظمة وسهلة التطوير.

### أهم الميزات

- **تنزيل الفيديو:** الحصول على أفضل جودة متاحة مع دمج الفيديو والصوت تلقائيًا.
- **تنزيل الصوت:** دعم MP3 للصوت المضغوط وWAV للصوت غير المضغوط.
- **دعم منصات متعددة:** YouTube وInstagram وFacebook وTikTok وX/Twitter وKwai وSoundCloud، بحسب الرابط ودعم `yt-dlp` الحالي.
- **تحسينات YouTube:** اختيار أفضل مساري فيديو وصوت، دمج MP4، إعادة المحاولة، إعادة محاولة الأجزاء، واستكمال التنزيلات المتوقفة.
- **مراقبة الحافظة:** اكتشاف الرابط الذي تنسخه وبدء عملية التنزيل بسهولة.
- **مسارات متعددة الأنظمة:** استخدام مجلدي `Music` و`Videos` على الحاسوب ومسارات التخزين المشترك في Termux.
- **واجهة Rich احترافية:** شريط تقدم، السرعة، الحجم، الوقت المتبقي، رسائل الحالة، وجدول المنصات.
- **إضافة البيانات الوصفية:** إضافة بيانات PyDragonX للملفات المعالجة عند توفر FFmpeg.
- **تحديث آمن:** فحص إصدارات GitHub والتحديث باستخدام Git دون حذف المشروع.
- **بنية منظمة:** فصل المحرك والواجهة والإعدادات والمسارات والحافظة والاعتماديات والتحديثات.

### صيغ الإخراج

| النوع | الناتج | FFmpeg | الاستخدام |
|---|---|---:|---|
| فيديو | MP4 / أفضل جودة متاحة | موصى به | فيديو مع دمج الصوت |
| صوت | MP3 | مطلوب للتحويل | ملفات صوتية صغيرة ومتوافقة |
| صوت | WAV | مطلوب للتحويل | المونتاج والأرشفة بجودة غير مضغوطة |

### المتطلبات

- Python إصدار **3.10 أو أحدث**.
- يوصى بتثبيت FFmpeg، وهو مطلوب من أجل:
  - دمج مسارات الفيديو والصوت في YouTube؛
  - التحويل إلى MP3؛
  - التحويل إلى WAV؛
  - إضافة البيانات الوصفية.
- اتصال بالإنترنت.

### التثبيت

#### Linux / macOS

```bash
git clone https://github.com/PyDragonX/dawnloader-v2.git
cd dawnloader-v2

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python main.py
```

تثبيت FFmpeg على Ubuntu/Debian:

```bash
sudo apt update
sudo apt install ffmpeg
```

تثبيت FFmpeg على Arch:

```bash
sudo pacman -S ffmpeg
```

#### Windows

```powershell
git clone https://github.com/PyDragonX/dawnloader-v2.git
cd dawnloader-v2

py -m venv .venv
.venv\Scripts\activate
py -m pip install --upgrade pip
py -m pip install -r requirements.txt

py main.py
```

تثبيت FFmpeg باستخدام winget:

```powershell
winget install Gyan.FFmpeg
```

#### Android / Termux

```bash
pkg update
pkg install python ffmpeg git

git clone https://github.com/PyDragonX/dawnloader-v2.git
cd dawnloader-v2

termux-setup-storage
python -m pip install -r requirements.txt
python main.py
```

### تحديث الأداة دون حذفها

يمكن تحديث PyDragonX عن طريق Git دون حذف المشروع أو إعادة تثبيته:

```bash
cd dawnloader-v2
git status
git pull --ff-only origin main
python -m pip install -r requirements.txt
python main.py
```

إذا كان لديك تعديل محلي، احفظه أولًا:

```bash
git add .
git commit -m "Save local changes"
git pull --ff-only origin main
```

أو خزّنه مؤقتًا:

```bash
git stash push -m "Local PyDragonX changes"
git pull --ff-only origin main
git stash pop
```

التحديث الداخلي لا يستبدل الملفات التي تحتوي على تعديلات محلية غير محفوظة.

### حل مشاكل تنزيل YouTube

1. حدّث `yt-dlp`:

   ```bash
   python -m pip install --upgrade yt-dlp
   ```

2. تأكد من تثبيت FFmpeg:

   ```bash
   ffmpeg -version
   ```

3. عند اختيار جودة 1080p أو أعلى، غالبًا يقدم YouTube الفيديو والصوت في مسارين منفصلين؛ لذلك يجب تثبيت FFmpeg لدمجهما.
4. الفيديو الخاص أو المقيد بالعمر أو المنطقة أو الذي يتطلب تسجيل دخول قد يحتاج إلى جلسة مصرح بها. استخدم فقط الصلاحيات المسموح لك بها قانونيًا.
5. إذا كان الفيديو محذوفًا أو أصبح خاصًا فلن يمكن تنزيله من الرابط العام.
6. لا ترفع كلمات المرور أو الرموز السرية أو ملفات Cookies إلى GitHub.

### هيكل المشروع

```text
main.py                    نقطة تشغيل البرنامج وسير العمل
core/
  engine.py                محرك تنزيل yt-dlp معزول لكل مهمة
ui/
  display.py               واجهة Rich والتحقق من الروابط والتقدم
utils/
  config.py                حفظ إعدادات المستخدم
  path_manager.py          إدارة المسارات لكل نظام
  clipboard_monitor.py     اكتشاف روابط الحافظة
  dependency_checker.py    فحص FFmpeg
  updater.py               منطق فحص وتحديث GitHub وGit
requirements.txt            مكتبات Python المطلوبة
.gitignore                  استثناء الملفات المؤقتة والتنزيلات
README.md                   توثيق المشروع
```

### خارطة التطوير المستقبلية

- طابور تنزيلات يدعم الإيقاف المؤقت والاستكمال وإعادة المحاولة والإلغاء.
- اختيار الدقة والترميز والحاوية ومعدل البت والترجمة.
- تنزيل القوائم والقنوات مع منع تكرار الملفات.
- سجل تنزيلات باستخدام SQLite.
- دعم اختياري لملفات Cookies المصرح بها مع حفظها محليًا فقط.
- سجلات أخطاء منظمة وتقارير قابلة للتصدير.
- اختبارات آلية وCI لأنظمة Linux وWindows وTermux.
- لوحة TUI متقدمة أو API محلي اختياري.

### الاستخدام المسؤول والقانوني

استخدم PyDragonX فقط مع الوسائط التي تملكها أو لديك إذن بتنزيلها أو التي تسمح المنصة بتنزيلها صراحةً. احترم حقوق النشر والخصوصية وشروط المنصات والقوانين المحلية.

---

**PyDragonX: Precision, Power, and Professionalism in Your Terminal.**  
**PyDragonX: الدقة والقوة والاحترافية في الطرفية.**

- **GitHub:** [github.com/PyDragonX/dawnloader-v2](https://github.com/PyDragonX/dawnloader-v2)
- **Developer:** PyDragonX
- **Environment:** CLI / Terminal / Termux
- **Current version:** `2.0.0`
