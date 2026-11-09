import os
from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DijitalTrade - Profesyonel Grafik Terminali</title>
        <style>
            * {
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                background-color: #0b0f19;
                color: #f8fafc;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                height: 100vh;
                overflow: hidden;
            }
            header {
                background-color: #111827;
                padding: 12px 24px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid #1f2937;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                flex-wrap: wrap;
                gap: 15px;
                min-height: 65px;
            }
            .brand {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            h1 { 
                color: #38bdf8; 
                font-size: 17px; 
                margin: 0; 
                font-weight: 700;
                letter-spacing: 0.5px;
            }
            .badge {
                background-color: #065f46;
                color: #34d399;
                font-size: 11px;
                padding: 3px 8px;
                border-radius: 4px;
                font-weight: 600;
            }
            .search-box {
                display: flex;
                gap: 12px;
                align-items: center;
                flex-wrap: wrap;
            }
            select {
                background-color: #1f2937;
                color: white;
                border: 1px solid #374151;
                padding: 7px 14px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 500;
                outline: none;
                cursor: pointer;
                transition: border-color 0.2s;
            }
            select:hover, select:focus {
                border-color: #38bdf8;
            }
            .info-text {
                font-size: 12px; 
                color: #9ca3af;
            }
            .chart-container {
                flex: 1;
                width: 100%;
                height: calc(100vh - 65px);
            }
        </style>
    </head>
    <body>
        <header>
            <div class="brand">
                <h1>DijitalTrade Terminali</h1>
                <span class="badge">SMA 200 Aktif</span>
            </div>
            <div class="search-box">
                <span class="info-text">Hızlı Seçim:</span>
                <select id="coinSelect" onchange="changeCoinFromDropdown(this.value)">
                    <option value="BINANCE:BTCUSDT">Bitcoin (BTC)</option>
                    <option value="BINANCE:ETHUSDT">Ethereum (ETH)</option>
                    <option value="BINANCE:SOLUSDT">Solana (SOL)</option>
                    <option value="BINANCE:AVAXUSDT">Avalanche (AVAX)</option>
                    <option value="BINANCE:XRPUSDT">Ripple (XRP)</option>
                    <option value="BINANCE:DOGEUSDT">Dogecoin (DOGE)</option>
                    <option value="BINANCE:BNBUSDT">Binance Coin (BNB)</option>
                    <option value="BINANCE:ADAUSDT">Cardano (ADA)</option>
                    <option value="BINANCE:TRXUSDT">Tron (TRX)</option>
                    <option value="BINANCE:NEARUSDT">Near Protocol (NEAR)</option>
                    <option value="BINANCE:LINKUSDT">Chainlink (LINK)</option>
                    <option value="BINANCE:SUIUSDT">Sui (SUI)</option>
                </select>
                <span class="info-text">*(Grafik sol üstünden tüm coinleri aratabilirsin)*</span>
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
                    "toolbar_bg": "#111827",
                    "enable_publishing": false,
                    "hide_side_toolbar": false,
                    "allow_symbol_change": true,
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

            function changeCoinFromDropdown(symbol) {
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
