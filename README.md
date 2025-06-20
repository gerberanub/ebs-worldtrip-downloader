# ebs-worldtrip-downloader

This repository contains a simple script to log in to the EBS Worldtrip site and download a replay video using `ffmpeg`.

## Requirements

- Python 3
- `requests` and `beautifulsoup4` packages
- `ffmpeg` executable available in your PATH

Install Python dependencies with:

```bash
pip install requests beautifulsoup4
```

## Usage

Run the script directly:

```bash
python worldtrip_downloader.py
```

The script logs in with the provided credentials, fetches the video page, extracts the streaming MP4 URL, and downloads it using `ffmpeg`. The output filename is derived from the page title.
