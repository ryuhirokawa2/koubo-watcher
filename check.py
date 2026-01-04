import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

KEYWORDS = [
    "音楽 公募",
    "楽曲 募集",
    "作曲 募集",
    "サウンド 募集"
]

EXCLUDE_KEYWORDS = [
    "BMS",
    "BMSON",
    "BMSイベント"
]

SOURCES = {
    "KONAMI": [
        "https://www.konami.com/games/event/",
        "https://www.konami.com/amusement/"
    ],
    "SEGA": [
        "https://www.sega.jp/topics/",
        "https://www.sega.co.jp/recruit/"
    ],
    "X": [
        "https://nitter.net/search?f=tweets&q=音ゲー+公募",
        "https://nitter.net/search?f=tweets&q=楽曲+募集+音ゲー"
    ],
    "Threads": [
        "https://www.threads.net/search?q=音ゲー 公募"
    ],
    "Bluesky": [
        "https://bsky.app/search?q=音ゲー 公募"
    ]
}

def fetch(url):
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        return r.text
    except Exception:
        return None

def is_valid(text):
    for ex in EXCLUDE_KEYWORDS:
        if ex.lower() in text.lower():
            return False
    for kw in KEYWORDS:
        if kw.lower() in text.lower():
            return True
    return False

def notify(title, url, source):
    content = (
        f"🎮 **AC音ゲー 公募情報を検出！**\n\n"
        f"**{title}**\n"
        f"📍 Source: {source}\n"
        f"🔗 {url}\n\n"
        f"🗂 Notion用リンク: {url}\n"
        f"⏰ 検出日時: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

    requests.post(
        DISCORD_WEBHOOK,
        json={"content": content}
    )

def scan():
    for source, urls in SOURCES.items():
        for url in urls:
            html = fetch(url)
            if not html:
                continue

            soup = BeautifulSoup(html, "html.parser")
            links = soup.find_all("a")

            for a in links:
                title = a.get_text(strip=True)
                href = a.get("href")

                if not title or not href:
                    continue

                if not href.startswith("http"):
                    href = url.rstrip("/") + "/" + href.lstrip("/")

                text_blob = f"{title} {href}"

                if is_valid(text_blob):
                    notify(title, href, source)

if __name__ == "__main__":
    scan()
