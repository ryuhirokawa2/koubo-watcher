import requests
import hashlib
import os

URL = "https://example.com"  # ← 公募を載せてそうなページ
WEBHOOK = os.environ["DISCORD_WEBHOOK"]

res = requests.get(URL, timeout=20)
res.raise_for_status()

text = res.text
hash_now = hashlib.md5(text.encode("utf-8")).hexdigest()

hash_file = "last_hash.txt"

if os.path.exists(hash_file):
    with open(hash_file, "r") as f:
        last = f.read().strip()
else:
    last = ""

if hash_now != last:
    requests.post(
        WEBHOOK,
        json={
            "content": f"🔔 公募ページに更新があった可能性があります\n{URL}"
        }
    )
    with open(hash_file, "w") as f:
        f.write(hash_now)
