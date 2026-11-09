import os
from flask import Flask

app = Flask(__name__)

# CANLI MUM GRAFİKLERİ VE 200 SMA GÖSTERGELİ PANEL
@app.route('/', methods=['GET'])
def home():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DijitalTrade - Canlı Mum ve 200 SMA</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #0f172a;
                color: #ffffff;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                height: 100vh;
            }
            header {
                background-color: #1e293b;
                padding: 12px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid #334155;
                flex-wrap: wrap;
                gap: 10px;
            }
            h1 { color: #38bdf8; font-size: 18px; margin: 0; }
            .coin-selector {
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
            }
            button {
                background-color: #334155;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 6px;
                cursor: pointer;
                font-weight: bold;
                font-size: 13px;
            }
            button:hover, button.active {
                background-color: #38bdf8;
                color: #0f172a;
            }
            .chart-container {
                flex: 1;
                width: 100%;
                height: calc(100vh - 60px);
            }
        </style>
    </head>
    <body>
        <header>
            <h1>DijitalTrade (Tüm Coinler + SMA 200)</h1>
            <div class="coin-selector">
                <button onclick="changeCoin('BINANCE:BTCUSDT', this)" class="active">BTC</button>
                <button onclick="changeCoin('BINANCE:ETHUSDT', this)">ETH</button>
                <button onclick="changeCoin('BINANCE:SOLUSDT', this)">SOL</button>
                <button onclick="changeCoin('BINANCE:AVAXUSDT', this)">AVAX</button>
                <button onclick="changeCoin('BINANCE:XRPUSDT', this)">XRP</button>
                <button onclick="changeCoin('BINANCE:DOGEUSDT', this)">DOGE</button>
            </div>
        </header>
        
        <div class="chart-container" id="tradingview_widget"></div>

        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
            let tvWidget;

            function initChart(symbol) {
                document.getElementById('tradingview_widget').innerHTML = "";
                
                tvWidget = new TradingView.widget({
                    "width": "100%",
                    "height": "100%",
                    "symbol": symbol,
                    "interval": "60",
                    "timezone": "Europe/Istanbul",
                    "theme": "dark",
                    "style": "1",
                    "locale": "tr",
                    "toolbar_bg": "#1e293b",
                    "enable_publishing": false,
                    "hide_side_toolbar": false,
                    "allow_symbol_change": true, // Buradan dilediğin tüm coinleri aratabilirsin
                    "studies": [
                        {
                            "id": "MASimple@tv-basicstudies",
                            "inputs": {
                                "length": 200
                            }
                        }
                    ],
                    "container_id": "tradingview_widget"
                });
            }

            function changeCoin(symbol, btn) {
                document.querySelectorAll('.coin-selector button').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                initChart(symbol);
            }

            initChart('BINANCE:BTCUSDT');
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
