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
        <title>DijitalTrade - Sağ Panel Coin Listesi & SMA 200</title>
        <style>
            * {
                box-sizing: border-box;
            }
            html, body {
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                background-color: #0b0f19;
                color: #f8fafc;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                overflow: hidden;
            }
            .main-layout {
                display: flex;
                width: 100vw;
                height: 100vh;
            }
            .chart-area {
                flex: 1;
                height: 100%;
            }
            .sidebar {
                width: 280px;
                background-color: #111827;
                border-left: 1px solid #1f2937;
                display: flex;
                flex-direction: column;
                height: 100%;
            }
            .sidebar-header {
                padding: 14px;
                border-bottom: 1px solid #1f2937;
                background-color: #0f172a;
            }
            .sidebar-header h2 {
                font-size: 14px;
                color: #38bdf8;
                margin: 0 0 10px 0;
                font-weight: 700;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .badge {
                background-color: #065f46;
                color: #34d399;
                font-size: 10px;
                padding: 2px 6px;
                border-radius: 4px;
            }
            .search-input {
                width: 100%;
                background-color: #1f2937;
                color: white;
                border: 1px solid #374151;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 13px;
                outline: none;
            }
            .search-input:focus {
                border-color: #38bdf8;
            }
            .coin-list {
                flex: 1;
                overflow-y: auto;
                padding: 8px;
            }
            .coin-item {
                padding: 10px 12px;
                margin-bottom: 4px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 13px;
                font-weight: 500;
                color: #cbd5e1;
                display: flex;
                justify-content: space-between;
                align-items: center;
                transition: background 0.2s, color 0.2s;
            }
            .coin-item:hover {
                background-color: #1f2937;
                color: #ffffff;
            }
            .coin-item.active {
                background-color: #38bdf8;
                color: #0f172a;
                font-weight: 700;
            }
            .coin-symbol {
                font-size: 11px;
                color: #94a3b8;
            }
            .coin-item.active .coin-symbol {
                color: #0f172a;
            }
            /* Kaydırma çubuğu tasarımı */
            ::-webkit-scrollbar {
                width: 6px;
            }
            ::-webkit-scrollbar-track {
                background: #111827;
            }
            ::-webkit-scrollbar-thumb {
                background: #374151;
                border-radius: 3px;
            }
        </style>
    </head>
    <body>
        <div class="main-layout">
            <!-- Sol Taraf: Dev Ekran Mum Grafiği -->
            <div class="chart-area" id="tradingview_widget"></div>

            <!-- Sağ Taraf: Coin Arama ve Seçim Paneli -->
            <div class="sidebar">
                <div class="sidebar-header">
                    <h2>DijitalTrade <span class="badge">SMA 200</span></h2>
                    <input type="text" id="searchInput" class="search-input" placeholder="Coin ara (Örn: AVAX)..." onkeyup="filterCoins()">
                </div>
                <div class="coin-list" id="coinList">
                    <div class="coin-item active" onclick="changeCoin('BINANCE:BTCUSDT', this)"><span>Bitcoin</span><span class="coin-symbol">BTC</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:ETHUSDT', this)"><span>Ethereum</span><span class="coin-symbol">ETH</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:SOLUSDT', this)"><span>Solana</span><span class="coin-symbol">SOL</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:AVAXUSDT', this)"><span>Avalanche</span><span class="coin-symbol">AVAX</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:XRPUSDT', this)"><span>Ripple</span><span class="coin-symbol">XRP</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:DOGEUSDT', this)"><span>Dogecoin</span><span class="coin-symbol">DOGE</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:BNBUSDT', this)"><span>Binance Coin</span><span class="coin-symbol">BNB</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:ADAUSDT', this)"><span>Cardano</span><span class="coin-symbol">ADA</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:TRXUSDT', this)"><span>Tron</span><span class="coin-symbol">TRX</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:NEARUSDT', this)"><span>Near Protocol</span><span class="coin-symbol">NEAR</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:LINKUSDT', this)"><span>Chainlink</span><span class="coin-symbol">LINK</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:SUIUSDT', this)"><span>Sui</span><span class="coin-symbol">SUI</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:ARBUSDT', this)"><span>Arbitrum</span><span class="coin-symbol">ARB</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:OPUSDT', this)"><span>Optimism</span><span class="coin-symbol">OP</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:POLUSDT', this)"><span>Polygon</span><span class="coin-symbol">POL</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:DOTUSDT', this)"><span>Polkadot</span><span class="coin-symbol">DOT</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:ATOMUSDT', this)"><span>Cosmos</span><span class="coin-symbol">ATOM</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:RENDERUSDT', this)"><span>Render</span><span class="coin-symbol">RENDER</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:INJUSDT', this)"><span>Injective</span><span class="coin-symbol">INJ</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:TIAUSDT', this)"><span>Celestia</span><span class="coin-symbol">TIA</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:SEIUSDT', this)"><span>Sei</span><span class="coin-symbol">SEI</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:PEPEUSDT', this)"><span>Pepe</span><span class="coin-symbol">PEPE</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:SHIBUSDT', this)"><span>Shiba Inu</span><span class="coin-symbol">SHIB</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:WIFUSDT', this)"><span>Dogwifhat</span><span class="coin-symbol">WIF</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:FLOKIUSDT', this)"><span>Floki</span><span class="coin-symbol">FLOKI</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:BONKUSDT', this)"><span>Bonk</span><span class="coin-symbol">BONK</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:FTMUSDT', this)"><span>Fantom</span><span class="coin-symbol">FTM</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:APTUSDT', this)"><span>Aptos</span><span class="coin-symbol">APT</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:FILUSDT', this)"><span>Filecoin</span><span class="coin-symbol">FIL</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:UNIUSDT', this)"><span>Uniswap</span><span class="coin-symbol">UNI</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:ICPUSDT', this)"><span>Internet Computer</span><span class="coin-symbol">ICP</span></div>
                </div>
            </div>
        </div>

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

            function changeCoin(symbol, element) {
                // Aktif sınıfını değiştir
                document.querySelectorAll('.coin-item').forEach(el => el.classList.remove('active'));
                element.classList.add('active');
                
                // Grafiği yükle
                initChart(symbol);
            }

            function filterCoins() {
                let input = document.getElementById('searchInput').value.toUpperCase();
                let items = document.getElementsByClassName('coin-item');
                
                for (let i = 0; i < items.length; i++) {
                    let text = items[i].textContent || items[i].innerText;
                    if (text.toUpperCase().indexOf(input) > -1) {
                        items[i].style.display = "";
                    } else {
                        items[i].style.display = "none";
                    }
                }
            }

            // İlk açılışta Bitcoin ile başlat
            initChart('BINANCE:BTCUSDT');
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
