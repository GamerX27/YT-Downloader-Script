import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from yt_dlp import YoutubeDL
import threading
import subprocess
import sys
import io
import signal

class YTDlpApp:
    def __init__(self, root):
        self.root = root
        self.root.title('YouTube Downloader')
        self.root.geometry('800x600')
        self.root.configure(bg='#121212')  # Dark mode background

        # Configure styles for Material You theme
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#121212', foreground='#E0E0E0', font=('Roboto', 12))
        style.configure('TButton', background='#37474F', foreground='#E0E0E0', font=('Roboto', 12, 'bold'), borderwidth=0, focusthickness=3, focuscolor='#6200EE')
        style.map('TButton', background=[('active', '#546E7A')])
        style.configure('TCombobox', background='#37474F', foreground='#E0E0E0', font=('Roboto', 12))

        # Main Frame with rounded corners using Canvas
        self.main_frame = tk.Canvas(root, bg='#1E1E1E', highlightthickness=0, borderwidth=0)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create rounded rectangle
        self.rounded_rectangle(self.main_frame, 0, 0, 760, 560, radius=20, fill='#1E1E1E')

        # URL Entry
        self.url_label = ttk.Label(self.main_frame, text='YouTube URL:')
        self.url_label.place(x=20, y=20)
        self.url_entry = ttk.Entry(self.main_frame, width=50, font=('Roboto', 12))
        self.url_entry.place(x=150, y=20)

        # Path Entry
        self.path_label = ttk.Label(self.main_frame, text='Download Location:')
        self.path_label.place(x=20, y=70)
        self.path_entry = ttk.Entry(self.main_frame, width=50, font=('Roboto', 12))
        self.path_entry.insert(0, os.path.join(os.path.expanduser('~'), 'Downloads'))
        self.path_entry.place(x=150, y=70)
        self.browse_button = ttk.Button(self.main_frame, text='Browse', command=self.browse_location)
        self.browse_button.place(x=650, y=65)

        # Format Selection
        self.format_label = ttk.Label(self.main_frame, text='Select Format:')
        self.format_label.place(x=20, y=120)
        self.format_var = tk.StringVar()
        self.format_combobox = ttk.Combobox(self.main_frame, textvariable=self.format_var, values=['MP4', 'MP3', 'Original'], font=('Roboto', 12))
        self.format_combobox.place(x=150, y=120)
        self.format_var.set('MP4')

        # Download Button
        self.download_button = ttk.Button(self.main_frame, text='Download!', command=self.start_download)
        self.download_button.place(x=300, y=170)

        # Force Stop Button
        self.stop_button = ttk.Button(self.main_frame, text='Force Stop', command=self.stop_download)
        self.stop_button.place(x=450, y=170)
        self.stop_button.config(state=tk.DISABLED)

        # Logs Section
        self.log_label = ttk.Label(self.main_frame, text='Logs:')
        self.log_label.place(x=20, y=220)
        self.log_text = scrolledtext.ScrolledText(self.main_frame, width=90, height=15, state='normal', bg='#263238', fg='#E0E0E0', font=('Courier', 10), relief=tk.FLAT, wrap=tk.WORD)
        self.log_text.place(x=20, y=250)

        # Auto Scroll Logs
        self.log_text.bind("<1>", lambda event: self.log_text.see(tk.END))

        # Download thread reference
        self.download_thread = None
        self.downloading = False
        self.ydl = None
        self.download_process = None

    def rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]

        return canvas.create_polygon(points, **kwargs, smooth=True)

    def browse_location(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_selected)

    def start_download(self):
        if not self.downloading:
            self.download_thread = threading.Thread(target=self.download)
            self.download_thread.start()
            self.stop_button.config(state=tk.NORMAL)

    def stop_download(self):
        if self.downloading and self.download_process:
            self.downloading = False
            self.download_process.terminate()  # Kill the yt-dlp process
            self.log_message('Download stopped by user.')
            self.stop_button.config(state=tk.DISABLED)

    def download(self):
        self.downloading = True
        url = self.url_entry.get()
        path = self.path_entry.get()
        format_selected = self.format_var.get()
        if not url or not path:
            messagebox.showerror('Error', 'Please provide both URL and download location.')
            self.stop_button.config(state=tk.DISABLED)
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
            # Start the download process
            self.download_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            for line in self.download_process.stdout:
                self.log_message(line.strip())

            self.download_process.wait()

            if self.downloading:
                if self.download_process.returncode == 0:
                    self.log_message('Download completed successfully!')
                    self.root.after(0, lambda: messagebox.showinfo('Success', 'Download completed successfully!'))
                else:
                    self.log_message('Download failed with errors.')
                    self.root.after(0, lambda: messagebox.showerror('Error', 'Download failed.'))
        except Exception as e:
            if self.downloading:
                self.log_message(f'An error occurred: {str(e)}')
                self.root.after(0, lambda: messagebox.showerror('Error', f'An error occurred: {str(e)}'))
        finally:
            self.downloading = False
            self.stop_button.config(state=tk.DISABLED)

    def log_message(self, message):
        self.log_text.insert(tk.END, f'{message}\n')
        self.log_text.see(tk.END)  # Auto-scroll to the end of the log
        self.root.update_idletasks()  # Update the GUI to make it responsive during the download

    def debug(self, msg):
        self.log_message(f'DEBUG: {msg}')

    def info(self, msg):
        self.log_message(f'INFO: {msg}')

    def warning(self, msg):
        self.log_message(f'WARNING: {msg}')

    def error(self, msg):
        self.log_message(f'ERROR: {msg}')

if __name__ == '__main__':
    root = tk.Tk()
    app = YTDlpApp(root)
    root.mainloop()
