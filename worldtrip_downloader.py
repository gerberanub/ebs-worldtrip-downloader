import re
import subprocess
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def login(session: requests.Session, username: str, password: str) -> None:
    """Login to the EBS Worldtrip site using provided credentials."""
    login_url = "https://worldtrip.ebs.co.kr/worldtrip/sso/login"
    payload = {
        "loginId": username,
        "passwd": password,
        "returnUrl": "https://worldtrip.ebs.co.kr/worldtrip/index",
    }
    resp = session.post(login_url, data=payload, allow_redirects=True)
    resp.raise_for_status()


def fetch_video_info(session: requests.Session, page_url: str):
    """Retrieve the video title and mp4 url from a replay page."""
    resp = session.get(page_url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Title from page, fallback to slug if missing
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else "video"

    # Look for mp4 url in page source
    match = re.search(r"https://[^"]+\.mp4[^\"]*", resp.text)
    if not match:
        return title, None
    mp4_url = match.group(0)
    return title, mp4_url


def download_video(mp4_url: str, filename: str) -> None:
    """Use ffmpeg to download the given mp4 url to filename."""
    subprocess.run([
        "ffmpeg",
        "-i",
        mp4_url,
        "-c",
        "copy",
        filename,
    ], check=True)


def main():
    username = "eunchanglee"
    password = "UZ86uLY-Nm6T"
    page_url = (
        "https://worldtrip.ebs.co.kr/worldtrip/replayView?"
        "siteCd=KH&courseId=BP0PAPD0000000013&"
        "stepId=01BP0PAPD0000000013&lectId=60608885"
    )

    with requests.Session() as session:
        login(session, username, password)
        title, mp4_url = fetch_video_info(session, page_url)
        if not mp4_url:
            raise RuntimeError("Could not find mp4 url on the page")
        filename = f"{title}.mp4"
        print(f"Downloading {mp4_url} -> {filename}")
        download_video(mp4_url, filename)


if __name__ == "__main__":
    main()
