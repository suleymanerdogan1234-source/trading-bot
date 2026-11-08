import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# 1. ANA SAYFA ROTASI (Tarayıcıda https://dijitaltrade.onrender.com açıldığında görünen sayfa)
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
                max-width: 400px;
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
        </style>
    </head>
    <body>
        <div class="card">
            <h1>DijitalTrade</h1>
            <p>Trading Bot ve Webhook Sunucusu Aktif</p>
            <div class="status">● Sunucu Çalışıyor</div>
        </div>
    </body>
    </html>
    """

# 2. WEBHOOK ROTASI (TradingView veya sinyal sistemlerinden al-sat bildirimi almak için)
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        print("Gelen Sinyal Verisi:", data)
        
        # Sinyal işleme mantığı buraya gelir
        return jsonify({"status": "success", "message": "Sinyal başarıyla alındı", "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# 3. SAĞLIK KONTROLÜ ROTASI (Render canlılık kontrolü için)
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
