import os
import threading
import time
from flask import Flask, render_template, jsonify

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")

bot_status = {
    "running": False,
    "last_action": "Beklemede",
    "loop_count": 0
}

def trading_background_loop():
    global bot_status
    bot_status["running"] = True
    
    while bot_status["running"]:
        try:
            bot_status["loop_count"] += 1
            bot_status["last_action"] = f"Piyasa tarandı, döngü #{bot_status['loop_count']} aktif."
            print(f"Bot Döngüsü Çalışıyor: {bot_status['last_action']}")
        except Exception as e:
            bot_status["last_action"] = f"Hata oluştu: {str(e)}"
            print(f"Trading Bot Hatası: {e}")
            
        time.sleep(60)

def start_bot_thread():
    if API_KEY and API_SECRET:
        t = threading.Thread(target=trading_background_loop, daemon=True)
        t.start()

start_bot_thread()

# Ana sayfaya tıklandığında hazırladığımız TradingView grafik arayüzünü açar
@app.route('/')
def home():
    return render_template('index.html')

# Bot detaylarını JSON olarak görmek istersen /status adresini kullanabilirsin
@app.route('/status')
def status():
    return jsonify({
        "status": "success",
        "bot_details": bot_status
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
