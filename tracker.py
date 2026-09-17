import os
import time
import requests
from bs4 import BeautifulSoup
from threading import Thread
from flask import Flask

# Render Web Service-এর পোর্ট চালু রাখার জন্য একটি ফেইক ওয়েব সার্ভার
app = Flask('')

@app.route('/')
def home():
    return "PDO Tracker is Running Successfully!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- আপনার অরিজিনাল ট্র্যাকিং লজিক ---
TELEGRAM_TOKEN = "8829341019:AAE0NcgoQdwMT6GsRV_qUPisJPO5_wggRiE"
CHAT_ID = "6058817369"
TARGET_URL = "https://training.oep.gov.bd/pdo-training"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram Notification Error: {e}")

def track_pdo():
    send_telegram("🚀 PDO Batch Tracker সফলভাবে Render-এ চালু হয়েছে!")
    seen_batches = set()

    while True:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(TARGET_URL, headers=headers, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # সাইটের ডাটা অনুযায়ী ফিল্টার লজিক
                rows = soup.find_all('tr')
                for row in rows:
                    text = row.get_text()
                    if text not in seen_batches:
                        seen_batches.add(text)
                        # নতুন তথ্য পেলে টেলিগ্রামে অ্যালার্ট পাঠাবে
            else:
                print(f"Status Error: {response.status_code}")
        except Exception as e:
            print(f"Checking Error: {e}")
        
        # প্রতি ৫ মিনিট (৩০০ সেকেন্ড) পর পর চেক করবে
        time.sleep(300)

if __name__ == "__main__":
    # ব্যাকগ্রাউন্ডে ট্র্যাকার রান করবে
    tracker_thread = Thread(target=track_pdo)
    tracker_thread.daemon = True
    tracker_thread.start()
    
    # মেইন থ্রেডে ওয়েব সার্ভার রান করবে
    run_web_server()
