#!/usr/bin/env python3
"""
mp3dl - Convert a YouTube video to an MP3 file using yt-dlp.

Usage:
    ./mp3dl.py <youtube-url> [-o OUTPUT_DIR] [-q {128,192,256,320}]

Examples:
    ./mp3dl.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
    ./mp3dl.py https://youtu.be/dQw4w9WgXcQ -o ~/Music -q 320
"""

import argparse
import shutil
import sys

from yt_dlp import YoutubeDL


def check_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None


def progress_hook(d: dict) -> None:
    if d["status"] == "downloading":
        pct = d.get("_percent_str", "").strip()
        speed = d.get("_speed_str", "").strip()
        sys.stdout.write(f"\rDownloading... {pct} ({speed})   ")
        sys.stdout.flush()
    elif d["status"] == "finished":
        sys.stdout.write("\rDownload complete, converting to MP3...\n")
        sys.stdout.flush()


def convert(url: str, output_dir: str, quality: str) -> str:
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": quality,
            }
        ],
        "progress_hooks": [progress_hook],
        "noplaylist": True,
        "quiet": False,
        "no_warnings": False,
        # Use yt-dlp's default player clients: as of yt-dlp 2026.8.19 they
        # reach the ~130-160 kbps audio-only streams without a PO token.
        # (Forcing the "android" client limits you to a ~48 kbps combined
        # format.) If YouTube starts demanding PO tokens again, the
        # bgutil-ytdlp-pot-provider plugin + its Docker server fixes it.
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        # prepare_filename returns the pre-postprocessing name (e.g. .webm/.m4a);
        # the actual output after FFmpegExtractAudio is the same base with .mp3
        mp3_path = f"{filename.rsplit('.', 1)[0]}.mp3"
        return mp3_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a YouTube video to MP3 using yt-dlp.")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "-o", "--output", default="./downloads", help="Output directory (default: ./downloads)"
    )
    parser.add_argument(
        "-q",
        "--quality",
        default="192",
        choices=["128", "192", "256", "320"],
        help="MP3 bitrate in kbps (default: 192)",
    )
    args = parser.parse_args()

    if not check_ffmpeg():
        print(
            "Error: ffmpeg not found on PATH. Install it with 'brew install ffmpeg' and try again.",
            file=sys.stderr,
        )
        sys.exit(1)

    import os

    os.makedirs(args.output, exist_ok=True)

    try:
        mp3_path = convert(args.url, args.output, args.quality)
    except Exception as exc:  # yt-dlp raises its own DownloadError, etc.
        print(f"\nError: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"\nSaved: {mp3_path}")


if __name__ == "__main__":
    main()
