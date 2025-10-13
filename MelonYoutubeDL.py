from pytubefix import YouTube
from pytubefix.cli import on_progress

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.theme import Theme

import os
import sys
import time
import subprocess
import ffmpeg
import datetime
import re
import urllib.request

# --- Color Palette ---
MELON_GREEN = "#90EE90"  # A nice light green
DARK_MELON = "#3CB371"   # A darker green for contrast
INFO_BLUE = "cyan"
WARNING_YELLOW = "yellow"
ERROR_RED = "red"

custom_theme = Theme({
    "primary": MELON_GREEN,
    "secondary": DARK_MELON,
    "info": INFO_BLUE,
    "warning": WARNING_YELLOW,
    "error": ERROR_RED,
})

console = Console(theme=custom_theme)

def print_ok(text):
    console.print(f"[primary]V {text}")

def print_info(text):
    console.print(f"[info]i {text}")

def print_warning(text):
    console.print(f"[warning]! {text}")

def print_error(text):
    console.print(f"[error]X {text}")

def print_rule(text):
    console.rule(text, style=f"bold {DARK_MELON}")

def sanitize_filename(filename):
    """
    Removes invalid characters from a filename.
    """
    return re.sub(r'[\\/*?"<>|]',"", filename)

def download_thumbnail(yt):
    print_rule("Downloading Thumbnail")
    thumbnail_url = yt.thumbnail_url
    sanitized_title = sanitize_filename(yt.title)
    output_dir = os.path.join(os.getcwd(), 'output')
    os.makedirs(output_dir, exist_ok=True)
    thumbnail_path = os.path.join(output_dir, f'{sanitized_title}_thumbnail.jpg')

    try:
        urllib.request.urlretrieve(thumbnail_url, thumbnail_path)
        print_ok(f"Thumbnail saved to: {thumbnail_path}")
    except Exception as e:
        print_error(f"Failed to download thumbnail: {e}")

def display_banner():
    banner_text = Text("MelonYoutubeDL", style=f"bold {DARK_MELON}", justify="center")
    sub_text = Text("Your Fresh Video Downloader", style="primary", justify="center")
    panel = Panel(
        Text.assemble(banner_text, "\n", sub_text),
        border_style="secondary",
        padding=(1, 4)
    )
    console.print(panel)

def get_youtube_url():
    print_info("Please enter a YouTube video URL.")
    url = Prompt.ask("[secondary]URL[/secondary]")
    if not url:
        print_warning("No URL entered. Using a default 4K video for demonstration.")
        return 'https://www.youtube.com/watch?v=R3GfuzLMPkA'
    return url

def select_resolution(yt):
    resolutions = [
        {"id": 0, "label": "8K", "resv": "4320p", "size": "0", "stream": None},
        {"id": 1, "label": "4K", "resv": "2160p", "size": "0", "stream": None},
        {"id": 2, "label": "2.5K", "resv": "1440p", "size": "0", "stream": None},
        {"id": 3, "label": "2K", "resv": "1080p", "size": "0", "stream": None},
        {"id": 4, "label": "1K", "resv": "720p", "size": "0", "stream": None},
        {"id": 5, "label": "DV", "resv": "480p", "size": "0", "stream": None},
        {"id": 6, "label": "CD", "resv": "320p", "size": "0", "stream": None},
    ]

    for i, res in enumerate(resolutions):
        stream = yt.streams.filter(res=res["resv"], progressive=False, file_extension='mp4').first()
        if stream:
            resolutions[i]["size"] = f"{stream.filesize_mb:.2f}"
            resolutions[i]["stream"] = stream

    available_resolutions = [res for res in resolutions if res["stream"]]

    if not available_resolutions:
        print_error("No video streams found for this URL.")
        return None

    table = Table(show_header=True, header_style=f"bold {DARK_MELON}", border_style=DARK_MELON)
    table.add_column("Option", style="primary", justify="center")
    table.add_column("Resolution", style="info")
    table.add_column("Size (MB)", style="primary", justify="right")

    for i, res in enumerate(available_resolutions):
        table.add_row(str(i + 1), f"{res['label']} ({res['resv']})", res["size"])

    console.print(table)

    choice = Prompt.ask(
        "[secondary]Choose a resolution to download (default is 1)[/secondary]",
        choices=[str(i + 1) for i in range(len(available_resolutions))],
        default="1"
    )
    return available_resolutions[int(choice) - 1]

def download_and_merge(yt, selected_resolution):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(os.getcwd(), 'output')
    os.makedirs(output_dir, exist_ok=True)

    temp_audio_path = os.path.join(output_dir, f'temp_audio_{timestamp}.mp3')
    temp_video_path = os.path.join(output_dir, f'temp_video_{timestamp}.mp4')
    sanitized_title = sanitize_filename(yt.title)
    final_output_path = os.path.join(output_dir, f'{sanitized_title}.mp4')

    # --- Download Audio ---
    print_rule("Step 1/3: Downloading Audio")
    audio_stream = yt.streams.get_audio_only()
    if not audio_stream:
        print_error("No audio stream found.")
        return

    print_info(f"Audio size: {audio_stream.filesize_mb:.2f} MB")
    audio_stream.download(output_path=output_dir, filename=os.path.basename(temp_audio_path))
    print_ok("Audio download complete.")

    # --- Download Video ---
    print_rule("Step 2/3: Downloading Video")
    video_stream = selected_resolution["stream"]
    print_info(f"Video resolution: {selected_resolution['label']} ({selected_resolution['resv']})")
    print_info(f"Video size: {video_stream.filesize_mb:.2f} MB")
    video_stream.download(output_path=output_dir, filename=os.path.basename(temp_video_path))
    print_ok("Video download complete.")

    # --- Merge Files ---
    print_rule("Step 3/3: Merging Files with ffmpeg")
    try:
        print_info("Starting merge process...")
        input_video = ffmpeg.input(temp_video_path)
        input_audio = ffmpeg.input(temp_audio_path)
        ffmpeg.concat(input_video, input_audio, v=1, a=1).output(final_output_path).run(overwrite_output=True, quiet=True)
        print_ok(f"Successfully merged video and audio.")
        print_info(f"Final file saved to: {final_output_path}")

    except ffmpeg.Error as e:
        print_error("ffmpeg error during merge:")
        print_error(e.stderr.decode())
    finally:
        # --- Cleanup ---
        print_info("Cleaning up temporary files...")
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
        print_ok("Cleanup complete.")


def main():
    display_banner()
    url = get_youtube_url()

    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        print_rule(f"Fetching Video: [info]{yt.title}")

        # Ask to download thumbnail
        download_thumb = Prompt.ask("[secondary]Download thumbnail? (y/n)[/secondary]", choices=["y", "n"], default="n")
        if download_thumb == 'y':
            download_thumbnail(yt)

        selected_resolution = select_resolution(yt)

        if selected_resolution:
            download_and_merge(yt, selected_resolution)
            print_ok("All done!")

    except Exception as e:
        print_error(f"An error occurred: {e}")

    print_info("Press Enter to exit.")
    input()

if __name__ == "__main__":
    main()
