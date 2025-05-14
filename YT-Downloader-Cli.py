import os
import subprocess


def download_video(url, path, format_selected):
    """Downloads a video or audio using yt-dlp."""
    if not url or not path:
        print("Error: Please provide both a URL and a download location.")
        return

    sanitized_path = os.path.normpath(path)
    output_template = os.path.join(sanitized_path, '%(title)s.%(ext)s')

    command = [
        'yt-dlp',
        url,
        '-o', output_template
    ]

    if format_selected == 'MP4':
        command += ['-f', 'bestvideo+bestaudio', '--merge-output-format', 'mp4']
    elif format_selected == 'MP3':
        command += ['-f', 'bestaudio', '--extract-audio', '--audio-format', 'mp3', '--audio-quality', '192']
    elif format_selected == 'Original':
        command += ['-f', 'best']

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print("\nDownload Logs:")
        for line in process.stdout:
            print(line.strip())

        process.wait()

        if process.returncode == 0:
            print("\nDownload completed successfully!")
        else:
            print("\nDownload failed with errors.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    print("Welcome to YouTube Downloader CLI")

    url = input("Enter the YouTube URL: ").strip()

    print("\nChoose a format:")
    print("1. MP4")
    print("2. MP3")

    format_choice = input("Enter your choice (1 or 2): ").strip()
    if format_choice == '1':
        format_selected = 'MP4'
    elif format_choice == '2':
        format_selected = 'MP3'
    else:
        print("Invalid choice. Defaulting to MP4.")
        format_selected = 'MP4'

    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_path = os.path.join(script_dir, 'YT-Downloads')

    if not os.path.exists(default_path):
        os.makedirs(default_path)

    print(f"\nDownloading to default location: {default_path}\n")
    download_video(url, default_path, format_selected)

if __name__ == '__main__':
    main()
