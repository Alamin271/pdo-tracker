import os
import time
import requests
from bs4 import BeautifulSoup
from threading import Thread
from flask import Flask

# Render Web Service-এর পোর্ট চালু রাখার জন্য ফ্ল্যাস্ক সার্ভার
app = Flask('')

@app.route('/')
def home():
    return "PDO Tracker is Running Successfully!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- আপনার ক্রেডেনশিয়াল ও কনফিগারেশন ---
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
    print("Starting PDO Tracking loop...")
    send_telegram("🚀 PDO Batch Tracker সফলভাবে Render-এ চালু হয়েছে!")
    seen_batches = set()

    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    # লগইন প্রসেস
    try:
        login_payload = {
            'username': USERNAME,
            'password': PASSWORD
        }
        login_res = session.post(LOGIN_URL, data=login_payload, headers=headers, timeout=15)
        print(f"Login Response Status: {login_res.status_code}")
    except Exception as e:
        print(f"Login Attempt Error: {e}")

    # ব্যাকগ্রাউন্ড মনিটরিং লুপ
    while True:
        try:
            response = session.get(BATCH_URL, headers=headers, timeout=15)
            print(f"Target Site Fetch Status: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                rows = soup.find_all('tr')
                for row in rows:
                    text = row.get_text().strip()
                    if text and text not in seen_batches:
                        seen_batches.add(text)
                        # নতুন ডাটা খুঁজে পেলে টেলিগ্রামে পাঠাবে
            else:
                print(f"Site Warning - Status Code: {response.status_code}")
        except Exception as e:
            print(f"Fetch Error: {e}")
        
        # প্রতি ৫ মিনিট (৩০০ সেকেন্ড) পরপর চেক করবে
        time.sleep(300)

if __name__ == "__main__":
    # ট্র্যাকার ব্যাকগ্রাউন্ড থ্রেডে চলবে
    tracker_thread = Thread(target=track_pdo)
    tracker_thread.daemon = True
    tracker_thread.start()
    
    # পোর্ট বাইন্ডিং নিশ্চিত করতে মেইন থ্রেডে ফ্ল্যাস্ক সার্ভার চলবে
    run_web_server()
