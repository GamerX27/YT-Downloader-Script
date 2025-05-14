
# YouTube Downloader CLI

This project is a Python-based CLI tool for downloading YouTube videos and playlists in various formats (MP4 or MP3). It leverages the powerful `yt-dlp` tool to ensure high-quality downloads and flexibility.

---

## Features
- **Single Video Download**: Download any YouTube video as MP4 or MP3.
- **Playlist Download**: Automatically download entire playlists into organized folders named after the playlist.
- **Format Selection**: Choose between MP4 (video) and MP3 (audio).

---

## Installation

### Prerequisites
Ensure Python (version 3.6 or higher) is installed on your system.

### Dependencies
This tool depends on `yt-dlp` and `ffmpeg`. Install them based on your Linux distribution:

#### Debian/Ubuntu:
```bash
sudo apt update
sudo apt install -y python3 python3-pip ffmpeg
pip3 install yt-dlp
```

#### Fedora:
```bash
sudo dnf install -y python3 python3-pip ffmpeg
pip3 install yt-dlp
```

#### Arch/Manjaro:
```bash
sudo pacman -Syu python python-pip ffmpeg
pip install yt-dlp
```

---

## Usage

### Clone the Repository
```bash
git clone <repository_url>
cd <repository_folder>
```

### Run the Script
```bash
python3 YT-Downloader-Cli.py
```

### Options
1. **Choose Single Video or Playlist**:
   - Enter `1` to download a single video.
   - Enter `2` to download an entire playlist.

2. **Provide the YouTube URL**:
   - Paste the video or playlist URL.

3. **Select Format**:
   - Enter `1` for MP4 (video).
   - Enter `2` for MP3 (audio).

4. **Download Location**:
   - The downloads are saved in the `YT-Downloads` folder within the script's directory.

---

## Functions

### `download_video(url, path, format_selected)`
Downloads a single video.
- **url**: The YouTube URL.
- **path**: The directory to save the download.
- **format_selected**: Format of the download (MP4 or MP3).

### `download_playlist(playlist_url, path, format_selected)`
Downloads all videos in a playlist.
- **playlist_url**: The YouTube playlist URL.
- **path**: The directory to save the playlist folder.
- **format_selected**: Format of the download (MP4 or MP3).

### `main()`
The entry point of the script. Handles user inputs and calls the appropriate download function.

---

## Known Issues
- **Long Playlist Names**: Extremely long playlist titles are truncated to prevent file system errors.
- **Dependencies**: Ensure `yt-dlp` and `ffmpeg` are installed and accessible in the system PATH.

---

## Contributing
Feel free to fork this repository and submit pull requests. All contributions are welcome!

---

## License
MIT License
