import os
import time
import requests
from bs4 import BeautifulSoup
from threading import Thread
from flask import Flask

app = Flask('')

@app.route('/')
def home():
    return "PDO Tracker is Running Successfully!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

TELEGRAM_TOKEN = "8829341019:AAE0NcgoQdwMT6GsRV_qUPisJPO5_wggRiE"
CHAT_ID = "6058817369"

USERNAME = "01339976130@demo.com"
PASSWORD = "Shawon@777"

LOGIN_URL = "https://training.oep.gov.bd/login"
BATCH_URL = "https://training.oep.gov.bd/pdo-training"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        res = requests.post(url, json=payload, timeout=10)
        print(f"Telegram API Response: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"Telegram Exception: {e}")

def track_pdo():
    # সার্ভার পুরোপুরি চালু হওয়ার জন্য ৫ সেকেন্ড অপেক্ষা করবে
    time.sleep(5)
    
    print("Sending welcome message...")
    send_telegram("🚀 PDO Batch Tracker সফলভাবে Render-এ চালু হয়েছে এবং মনিটরিং শুরু করেছে!")
    
    seen_batches = set()
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    # লগইন প্রসেস
    try:
        login_payload = {
            'username': USERNAME,
            'password': PASSWORD
        }
        session.post(LOGIN_URL, data=login_payload, headers=headers, timeout=15)
    except Exception as e:
        print(f"Login Error: {e}")

    # ব্যাকগ্রাউন্ড লুপ
    while True:
        try:
            response = session.get(BATCH_URL, headers=headers, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                rows = soup.find_all('tr')
                for row in rows:
                    text = row.get_text().strip()
                    if text and text not in seen_batches:
                        seen_batches.add(text)
                        # নতুন ডাটা পাওয়া গেলে টেলিগ্রামে অ্যালার্ট পাঠাবে
            else:
                print(f"Site Status: {response.status_code}")
        except Exception as e:
            print(f"Fetch Error: {e}")
        
        time.sleep(300)

if __name__ == "__main__":
    tracker_thread = Thread(target=track_pdo)
    tracker_thread.daemon = True
    tracker_thread.start()
    
    run_web_server()
