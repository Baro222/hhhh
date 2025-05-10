import os, time, json, requests
from modules.twitter import TwitterUserScraper
from utils import send_telegram, translate

ACCOUNTS_FILE = "accounts.txt"
CACHE_FILE = "sent_cache.json"
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        sent = set(json.load(f))
else:
    sent = set()

def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(list(sent), f)

with open(ACCOUNTS_FILE) as f:
    ACCOUNTS = [line.strip() for line in f if line.strip()]

print("🚀 트윗 감지 봇 시작됨 (Railway 배포용)...")

while True:
    for user in ACCOUNTS:
        try:
            for tweet in TwitterUserScraper(user).get_items():
                if tweet.id not in sent:
                    text = tweet.content
                    translated = translate(text)
                    msg = f"🐦 @{user}\n{text}\n📘 {translated}\n\n🔗 https://x.com/{user}/status/{tweet.id}"
                    media = tweet.media[0].fullUrl if tweet.media else None
                    send_telegram(msg, media)
                    sent.add(tweet.id)
                    save_cache()
                break
        except Exception as e:
            send_telegram(f"[ERROR] {user}: {str(e)}")
    time.sleep(30)
