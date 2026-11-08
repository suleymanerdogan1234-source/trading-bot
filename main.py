import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# 1. ANA SAYFA ROTASI (Tarayıcıda açıldığında görünen panel)
@app.route('/', methods=['GET'])
def home():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DijitalTrade Bot</title>
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
            <h1>DijitalTrade</h1>
            <p>Çoklu Kripto Trading Bot ve Webhook Sunucusu Aktif</p>
            <div class="coins">Sistem: Tüm Coinler (BTC, ETH, SOL, XRP...) Destekleniyor</div>
            <div class="status">● Canlı / Dinamik Mod</div>
        </div>
    </body>
    </html>
    """

# 2. TÜM KRİPTOLAR İÇİN TEK VE ORTAK WEBHOOK ROTASI
@app.route('/webhook', methods=['POST'])
def webhook_crypto():
    try:
        data = request.get_json(force=True)
        
        # Gelen veriden coin adını, işlem türünü (BUY/SELL) ve fiyatı dinamik olarak alıyoruz
        symbol = data.get('symbol', 'UNKNOWN').upper()
        action = data.get('action', 'NEUTRAL').upper()
        price = data.get('price', 0)
        strategy = data.get('strategy', 'Genel Strateji')
        
        print(f"--- YENİ KRİPTO SİNYALİ ---")
        print(f"Coin / Parite : {symbol}")
        print(f"İşlem (Yön)   : {action}")
        print(f"Fiyat         : {price}")
        print(f"Strateji      : {strategy}")
        print(f"Tüm Veri      : {data}")
        print(f"---------------------------")
        
        # Buraya istediğin borsa API entegrasyonunu (Binance vb.) bağlayabilirsin
        
        return jsonify({
            "status": "success", 
            "message": f"{symbol} için {action} sinyali başarıyla işlendi",
            "symbol": symbol,
            "action": action,
            "price": price
        }), 200
        
    except Exception as e:
        print("Webhook Hata:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 400

# 3. SAĞLIK KONTROLÜ
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
