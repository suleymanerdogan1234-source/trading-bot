import os
import time
from flask import Flask, jsonify
import ccxt

app = Flask(__name__)

# Borsa Bağlantısı (Herkese açık veri çekmek için API anahtarına gerek yok)
exchange = ccxt.binance({
    'enableRateLimit': True,
})

# 1. ANA SAYFA ROTASI (Canlı Panel)
@app.route('/', methods=['GET'])
def home():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DijitalTrade Otonom Bot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #0f172a;
                color: #ffffff;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .card {
                background-color: #1e293b;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.5);
                text-align: center;
                max-width: 450px;
            }
            h1 { color: #38bdf8; margin-bottom: 10px; }
            p { color: #94a3b8; line-height: 1.5; }
            .status {
                display: inline-block;
                padding: 8px 16px;
                background-color: #16a34a;
                color: white;
                border-radius: 20px;
                font-weight: bold;
                margin-top: 15px;
            }
            .coins { margin-top: 15px; color: #38bdf8; font-size: 14px; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>DijitalTrade Otonom Bot</h1>
            <p>Kendi Canlı Mum Analizi ve Sinyal Üretim Motoru Aktif</p>
            <div class="coins">Analiz Modu: Kendi Mumlarımız (BTC, ETH, SOL...)</div>
            <div class="status">● Otomatik Analiz Aktif</div>
        </div>
    </body>
    </html>
    """

# 2. KENDİ MUMLARIMIZ ÜZERİNDEN ANALİZ YAPAN ROTA (/analiz/ETHUSDT gibi)
@app.route('/analiz/<symbol>', methods=['GET'])
def analyze_candles(symbol):
    try:
        # Parite formatını ayarlayalım (örneğin ETHUSDT -> ETH/USDT)
        formatted_symbol = symbol.upper()
        if "/" not in formatted_symbol and formatted_symbol.endswith("USDT"):
            formatted_symbol = formatted_symbol.replace("USDT", "/USDT")

        # Son 5 adet 1 dakikalık mumu çekiyoruz
        # OHLCV: [Zaman, Açılış, Yüksek, Düşük, Kapanış, Hacim]
        candles = exchange.fetch_ohlcv(formatted_symbol, timeframe='1m', limit=5)
        
        if not candles:
            return jsonify({"status": "error", "message": "Mum verisi alınamadı"}), 400

        # Son tamamlanan mum ve güncel fiyat
        last_candle = candles[-2]  # Kapanmış olan son mum
        current_candle = candles[-1] # Şu an hareket eden canlı mum
        
        open_price = last_candle[1]
        close_price = last_candle[4]
        current_price = current_candle[4]

        # --- KENDİ STRATEJİMİZ / MUM MANTIĞIMIZ ---
        # Örnek Kural: Son kapatan mum yeşilse ve fiyat yükseliyorsa AL, kırmızıysa SAT
        action = "WAIT"
        reason = "Belirgin bir şart oluşmadı"

        if close_price > open_price:
            action = "BUY"
            reason = f"Son mum YEŞİL kapandı ({open_price} -> {close_price})"
        elif close_price < open_price:
            action = "SELL"
            reason = f"Son mum KIRMIZI kapandı ({open_price} -> {close_price})"

        print(f"\n--- OTOMATİK MUM ANALİZİ [{formatted_symbol}] ---")
        print(f"Güncel Fiyat : {current_price}")
        print(f"Son Mum      : Açılış={open_price}, Kapanış={close_price}")
        print(f"Üretilen Karar: {action} ({reason})")
        print("--------------------------------------------------\n")

        return jsonify({
            "status": "success",
            "symbol": formatted_symbol,
            "current_price": current_price,
            "last_candle": {
                "open": open_price,
                "close": close_price
            },
            "signal": action,
            "reason": reason
        }), 200

    except Exception as e:
        print("Analiz Hatası:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 400

# 3. SAĞLIK KONTROLÜ
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
