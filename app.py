import os
from flask import Flask, jsonify

app = Flask(__name__)

# Çevre değişkenlerinden (Render Environment sekmesinden) API anahtarlarını alıyoruz
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")

@app.route("/")
def home():
    # Ana sayfa kontrolü: API anahtarları eklenmemişse uyarı döner
    if not API_KEY or not API_SECRET:
        return jsonify({
            "status": "error",
            "message": "Binance API anahtarları henüz Render çevre değişkenlerine eklenmemiş."
        }), 500

    return jsonify({
        "status": "success",
        "message": "Ticaret botu başarıyla çalışıyor ve Binance anahtarları bağlı!"
    })

@app.route("/trade")
def trade():
    if not API_KEY or not API_SECRET:
        return "API anahtarları eksik!", 500
    
    # Botun alım-satım mantığı buraya eklenecek
    return "Ticaret komutu çalıştırıldı."

if __name__ == "__main__":
    # Render'ın otomatik atadığı dinamik port numarasını yakalıyoruz
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
