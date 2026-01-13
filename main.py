import requests
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ABC Proxy কনফিগারেশন (আপনার প্রক্সি ডিটেইলস এখানে বসান)
# Format: user:pass@ip:port
PROXY_DATA = "your_username:your_password@your_ip:your_port" 

proxies = {
    "http": f"http://{PROXY_DATA}",
    "https": f"http://{PROXY_DATA}"
}

def check_fb(phone):
    session = requests.Session()
    session.proxies = proxies # প্রক্সি কানেক্ট করা হলো
    
    url = "https://m.facebook.com/recover/initiate/"
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'referer': 'https://m.facebook.com/recover/initiate/',
        'origin': 'https://m.facebook.com',
        'content-type': 'application/x-www-form-urlencoded'
    }

    try:
        # ১. সেশন তৈরি
        session.get(url, headers=headers, timeout=15)
        
        # ২. সার্চ রিকোয়েস্ট
        payload = {
            'email': phone,
            'did_submit': 'Search'
        }
        
        response = session.post(url, data=payload, headers=headers, timeout=15)

        # রেজাল্ট লজিক
        if "send_code" in response.text or "password_reset_methods" in response.text:
            return {"status": "LIVE", "msg": "OTP Sent Successfully ✅"}
        elif "captcha" in response.text:
            return {"status": "CAPTCHA", "msg": "Captcha Detected! ⚠️"}
        elif "checkpoint" in response.text:
            return {"status": "DIE", "msg": "Proxy/IP Blocked by FB"}
        else:
            return {"status": "DIE", "msg": "No Account Found ❌"}

    except Exception as e:
        return {"status": "ERROR", "msg": "Proxy Connection Failed"}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def api():
    phone = request.json.get('phone')
    return jsonify(check_fb(phone))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)