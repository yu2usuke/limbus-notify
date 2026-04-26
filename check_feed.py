import os
import feedparser
import requests

FEED_URL = "https://rsshub.app/twitter/user/LimbusCompany_"
WEBHOOK  = os.environ["DISCORD_WEBHOOK"]
ID_FILE  = "last_id.txt"

# 前回の最終IDを読み込み
last_id = ""
if os.path.exists(ID_FILE):
    last_id = open(ID_FILE).read().strip()

# RSSフィードを取得
feed = feedparser.parse(FEED_URL)
if not feed.entries:
    print("フィード取得失敗 or 空")
    exit(0)

# 新着エントリを抽出（新しい順に並んでいる前提）
new_entries = []
for entry in feed.entries:
    if entry.get("id", entry.link) == last_id:
        break
    new_entries.append(entry)

if not new_entries:
    print("新着なし")
    exit(0)

# 古い順に通知（新しいものが後に来るように）
for entry in reversed(new_entries):
    payload = {
        "username": "リンバスカンパニー通知",
        "embeds": [{
            "title": "📢 新着ツイート",
            "description": entry.get("summary", "（本文なし）"),
            "url": entry.link,
            "color": 0xFF2222,
            "footer": {"text": "@LimbusCompany_"}
        }]
    }
    r = requests.post(WEBHOOK, json=payload)
    print(f"送信: {entry.link} → {r.status_code}")

# 最新IDを保存
latest_id = feed.entries[0].get("id", feed.entries[0].link)
open(ID_FILE, "w").write(latest_id)
print(f"最新ID保存: {latest_id}")
