
```markdown
# 🎥 YouTube Downloader Tool (yt.py)

A powerful, interactive, terminal-based YouTube downloader tool built with Python. Supports downloading videos, audios, descriptions, comments, and titles — either individually or in batch. It provides total control over the format and destination of downloads, including optional saving to SD card (Android Termux support).

---

## 🚀 Features

- ✅ **Interactive Menu System** — Easy-to-use options categorized into Combo, Single, and Multi modes.
- 🎬 **Video + Audio Downloads** — Select from any available format (e.g. 137+140).
- 🎧 **Audio-only Extraction** — Download MP3 audio files from any YouTube video.
- 📄 **Description & Title Saver** — Save the video’s description or title as a `.txt` file.
- 💬 **Download YouTube Comments** — Extract comments into readable `.txt` files using `jq`.
- 🔁 **Multi-link Batch Processing** — Process multiple links at once with a progress bar.
- 📦 **Download to SD Card** — Android-friendly, with option to move downloads to `/sdcard/Movies/`.
- 📦 **Metadata Extraction** — Title, description, and comments can be saved independently.

---

## 📁 Repository Structure

```

yt/
├── yt.py           # Main downloader script
├── README.md       # Usage guide (this file)
└── requirements.txt (optional, if added later)

````

---

## ⚙️ Requirements

The tool automatically checks and installs:

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [ffmpeg](https://ffmpeg.org/) (must be installed manually if not available)

Additionally, to extract comments:

- [`jq`](https://stedolan.github.io/jq/) (used for processing `.info.json` comment files)

On **Termux (Android)**, you can install dependencies like this:

```bash
pkg update && pkg install python ffmpeg jq
pip install yt-dlp
````

---

## ▶️ How to Run

1. **Clone the Repository:**

```bash
git clone https://github.com/MasHunterOfficial/yt
cd yt
```

2. **Run the Tool:**

```bash
python yt.py
```

3. **Follow the On-Screen Menu:**

Choose an option from the menu (1–12), then enter one or more YouTube video links (comma-separated).

---

## 🧠 Menu Overview

```
========= YouTube Downloader Tool =========
Combo:
 1. Download video with audio
 2. Download audio + description
 3. Download video/audio + comments

Single:
 4. Only title
 5. Only audio
 6. Only description
 7. Only comments

Multi:
 8. Multi-link video+audio download
 9. Multi-link only titles
10. Multi-link only descriptions
11. Multi-link only comments
12. Multi-link only audio
==========================================
```

---

## 💡 Example Usage

* Download audio from a video:

  > Select option 5, then enter:
  > `https://www.youtube.com/watch?v=example`

* Download comments in bulk:

  > Select option 11, then enter:
  > `https://youtu.be/abc123, https://youtu.be/xyz789`

* Save video + audio to your SD card:

  > Choose option 1, select format (e.g. `137+140`), then type `y` when prompted.

---

## ❗ Notes

* `ffmpeg` must be installed for video/audio merging.
* `jq` is required to extract and save comments properly.
* The tool runs well on Linux, Termux (Android), and Windows with Python support.

---

## 📜 License

This project is open-source under the [MIT License](LICENSE).

---

## 👤 Author

Developed by [MasHunterOfficial](https://github.com/MasHunterOfficial)
👉 Feel free to star ⭐ the repository if you find it useful!

```

