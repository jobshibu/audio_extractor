# mp4-to-mp3-converter

Convert a YouTube video to an MP3 file using [yt-dlp](https://github.com/yt-dlp/yt-dlp) + ffmpeg.



```bash
/opt/homebrew/bin/python3.13 -m venv venv   # yt-dlp needs Python >= 3.10; macOS system python3 is 3.9
./venv/bin/pip install -r requirements.txt
brew install ffmpeg
```

## Usage

```bash
./venv/bin/python mp3dl.py <youtube-url>
```

Options:

```bash
./venv/bin/python mp3dl.py <youtube-url> -o ~/Music -q 320
```

- `-o / --output` — output directory (default: `./downloads`)
- `-q / --quality` — MP3 bitrate: `128`, `192` (default), `256`, or `320`

## Example

```bash
./venv/bin/python mp3dl.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## Keeping yt-dlp up to date

YouTube changes frequently; if downloads start failing, update yt-dlp:

```bash
./venv/bin/pip install --upgrade yt-dlp
```

## Note on usage

Only download content you have the right to download (your own uploads, public domain, Creative Commons, or otherwise permitted under YouTube's Terms of Service and applicable copyright law).
