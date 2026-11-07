import os
import threading
import time
from flask import Flask, jsonify

app = Flask(__name__)

# Çevre değişkenlerinden API anahtarlarını alıyoruz
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")

# Botun arka plan döngü durumu
bot_status = {
    "running": False,
    "last_action": "Beklemede",
    "loop_count": 0,
}


def trading_background_loop():
  """Arka planda sürekli çalışacak trading döngüsü"""
  global bot_status
  bot_status["running"] = True

  while bot_status["running"]:
    try:
      # --- BURAYA TRADING STRATEJİNİ VE BİNANCE İŞLEMLERİNİ EKLEYEBİLİRSİN ---
      bot_status["loop_count"] += 1
      bot_status["last_action"] = (
          f"Piyasa tarandı, döngü #{bot_status['loop_count']} aktif."
      )
      print(f"Bot Döngüsü Çalışıyor: {bot_status['last_action']}")
      # ---------------------------------------------------------------------
    except Exception as e:
      bot_status["last_action"] = f"Hata oluştu: {str(e)}"
      print(f"Trading Bot Hatası: {e}")

    # Her 60 saniyede bir piyasayı kontrol eder (Süreyi ihtiyacına göre değiştirebilirsin)
    time.sleep(60)


# Botu arka planda thread olarak başlatıyoruz
def start_bot_thread():
  if API_KEY and API_SECRET:
    t = threading.Thread(target=trading_background_loop, daemon=True)
    t.start()


# Uygulama başlarken botu tetikle
start_bot_thread()


@app.route("/")
def home():
  if not API_KEY or not API_SECRET:
    return jsonify({
        "status": "error",
        "message": (
            "Binance API anahtarları henüz Render çevre değişkenlerine"
            " eklenmemiş."
        ),
    }), 400

  return jsonify({
      "status": "success",
      "message": "Ticaret botu başarıyla çalışıyor ve arka planda devrede!",
      "bot_details": bot_status,
  })


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=10000)
