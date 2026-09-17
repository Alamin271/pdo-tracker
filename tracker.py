import time
import requests
from bs4 import BeautifulSoup

# --- আপনার সঠিক তথ্যগুলো নিচে দিন ---
TELEGRAM_BOT_TOKEN = "8829341019:AAE0NcgoQdwMT6GsRV_qUPisJPO5_wggRiE"
TELEGRAM_CHAT_ID = "6058817369"

LOGIN_URL = "https://training.oep.gov.bd/login"
BATCH_URL = "https://training.oep.gov.bd/pdo-training"

USERNAME = "01339976130@demo.com"
PASSWORD = "Shawon@777"

CHECK_INTERVAL = 30  # প্রতি ৩০ সেকেন্ড পর পর চেক করবে

known_batches = set()

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg})
    except Exception as e:
        print(f"Telegram error: {e}")

def run():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })

    send_telegram("🚀 PDO Batch Tracker সফলভাবে চালু হয়েছে!")

    while True:
        try:
            res = session.get(BATCH_URL)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                current_batches = []
                
                for text in soup.stripped_strings:
                    if "BAT-" in text:
                        current_batches.append(text)

                for batch in current_batches:
                    if batch not in known_batches:
                        if len(known_batches) > 0:
                            msg = f"🚨 নতুন PDO ব্যাচ পাওয়া গেছে!\n\nব্যাচ: {batch}\nলিংক: {BATCH_URL}"
                            send_telegram(msg)
                        known_batches.add(batch)
            else:
                print(f"Error status: {res.status_code}")

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run()
