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
        <title>DijitalTrade - Tüm Coinler & SMA 200</title>
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
                position: relative;
            }
            .chart-area {
                flex: 1;
                height: 100%;
            }
            /* Sağ Panel */
            .sidebar {
                width: 240px;
                background-color: #111827;
                border-left: 1px solid #1f2937;
                display: flex;
                flex-direction: column;
                height: 100%;
                z-index: 100;
                transition: transform 0.3s ease;
            }
            .sidebar-header {
                padding: 12px;
                border-bottom: 1px solid #1f2937;
                background-color: #0f172a;
            }
            .sidebar-header h2 {
                font-size: 13px;
                color: #38bdf8;
                margin: 0 0 8px 0;
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
                padding: 7px 10px;
                border-radius: 6px;
                font-size: 12px;
                outline: none;
            }
            .search-input:focus {
                border-color: #38bdf8;
            }
            .coin-list {
                flex: 1;
                overflow-y: auto;
                padding: 6px;
            }
            .coin-item {
                padding: 9px 10px;
                margin-bottom: 3px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 13px;
                font-weight: 600;
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
            }
            .coin-price {
                font-size: 12px;
                font-weight: 500;
                color: #34d399;
            }
            .coin-item.active .coin-price {
                color: #0f172a;
            }
            /* Mobil İçin Menü Butonu */
            .mobile-toggle {
                display: none;
                position: fixed;
                top: 10px;
                right: 10px;
                z-index: 1000;
                background-color: #38bdf8;
                color: #0f172a;
                border: none;
                padding: 8px 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
                cursor: pointer;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            }
            @media (max-width: 768px) {
                .mobile-toggle {
                    display: block;
                }
                .sidebar {
                    position: absolute;
                    right: 0;
                    top: 0;
                    transform: translateX(100%);
                }
                .sidebar.open {
                    transform: translateX(0);
                }
            }
            /* Kaydırma çubuğu */
            ::-webkit-scrollbar {
                width: 5px;
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
        <button class="mobile-toggle" onclick="toggleSidebar()">Menü / Coinler</button>

        <div class="main-layout">
            <!-- Sol Taraf: Dev Ekran Mum Grafiği -->
            <div class="chart-area" id="tradingview_widget"></div>

            <!-- Sağ Taraf: Tüm Coinler ve Canlı Fiyatlar -->
            <div class="sidebar" id="sidebar">
                <div class="sidebar-header">
                    <h2>DijitalTrade <span class="badge">SMA 200</span></h2>
                    <input type="text" id="searchInput" class="search-input" placeholder="Coin ara (Örn: BTC)..." onkeyup="filterCoins()">
                </div>
                <div class="coin-list" id="coinList">
                    <!-- Tüm Popüler ve Genişletilmiş Coin Listesi -->
                    <div class="coin-item active" onclick="changeCoin('BINANCE:BTCUSDT', 'BTCUSDT', this)"><span>BTC</span><span class="coin-price" id="price_BTCUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:ETHUSDT', 'ETHUSDT', this)"><span>ETH</span><span class="coin-price" id="price_ETHUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:SOLUSDT', 'SOLUSDT', this)"><span>SOL</span><span class="coin-price" id="price_SOLUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:BNBUSDT', 'BNBUSDT', this)"><span>BNB</span><span class="coin-price" id="price_BNBUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:XRPUSDT', 'XRPUSDT', this)"><span>XRP</span><span class="coin-price" id="price_XRPUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:ADAUSDT', 'ADAUSDT', this)"><span>ADA</span><span class="coin-price" id="price_ADAUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:DOGEUSDT', 'DOGEUSDT', this)"><span>DOGE</span><span class="coin-price" id="price_DOGEUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:AVAXUSDT', 'AVAXUSDT', this)"><span>AVAX</span><span class="coin-price" id="price_AVAXUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:TRXUSDT', 'TRXUSDT', this)"><span>TRX</span><span class="coin-price" id="price_TRXUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:LINKUSDT', 'LINKUSDT', this)"><span>LINK</span><span class="coin-price" id="price_LINKUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:SUIUSDT', 'SUIUSDT', this)"><span>SUI</span><span class="coin-price" id="price_SUIUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:NEARUSDT', 'NEARUSDT', this)"><span>NEAR</span><span class="coin-price" id="price_NEARUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:ARBUSDT', 'ARBUSDT', this)"><span>ARB</span><span class="coin-price" id="price_ARBUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:OPUSDT', 'OPUSDT', this)"><span>OP</span><span class="coin-price" id="price_OPUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:POLUSDT', 'POLUSDT', this)"><span>POL</span><span class="coin-price" id="price_POLUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:DOTUSDT', 'DOTUSDT', this)"><span>DOT</span><span class="coin-price" id="price_DOTUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:ATOMUSDT', 'ATOMUSDT', this)"><span>ATOM</span><span class="coin-price" id="price_ATOMUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:RENDERUSDT', 'RENDERUSDT', this)"><span>RENDER</span><span class="coin-price" id="price_RENDERUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:INJUSDT', 'INJUSDT', this)"><span>INJ</span><span class="coin-price" id="price_INJUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:TIAUSDT', 'TIAUSDT', this)"><span>TIA</span><span class="coin-price" id="price_TIAUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:SEIUSDT', 'SEIUSDT', this)"><span>SEI</span><span class="coin-price" id="price_SEIUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:PEPEUSDT', 'PEPEUSDT', this)"><span>PEPE</span><span class="coin-price" id="price_PEPEUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:SHIBUSDT', 'SHIBUSDT', this)"><span>SHIB</span><span class="coin-price" id="price_SHIBUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:WIFUSDT', 'WIFUSDT', this)"><span>WIF</span><span class="coin-price" id="price_WIFUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:FLOKIUSDT', 'FLOKIUSDT', this)"><span>FLOKI</span><span class="coin-price" id="price_FLOKIUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:BONKUSDT', 'BONKUSDT', this)"><span>BONK</span><span class="coin-price" id="price_BONKUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:FTMUSDT', 'FTMUSDT', this)"><span>FTM</span><span class="coin-price" id="price_FTMUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:APTUSDT', 'APTUSDT', this)"><span>APT</span><span class="coin-price" id="price_APTUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:FILUSDT', 'FILUSDT', this)"><span>FIL</span><span class="coin-price" id="price_FILUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:UNIUSDT', 'UNIUSDT', this)"><span>UNI</span><span class="coin-price" id="price_UNIUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:ICPUSDT', 'ICPUSDT', this)"><span>ICP</span><span class="coin-price" id="price_ICPUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:FETUSDT', 'FETUSDT', this)"><span>FET</span><span class="coin-price" id="price_FETUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:GRTUSDT', 'GRTUSDT', this)"><span>GRT</span><span class="coin-price" id="price_GRTUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:RUNEUSDT', 'RUNEUSDT', this)"><span>RUNE</span><span class="coin-price" id="price_RUNEUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:AAVEUSDT', 'AAVEUSDT', this)"><span>AAVE</span><span class="coin-price" id="price_AAVEUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:MKRUSDT', 'MKRUSDT', this)"><span>MKR</span><span class="coin-price" id="price_MKRUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:STXUSDT', 'STXUSDT', this)"><span>STX</span><span class="coin-price" id="price_STXUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:IMXUSDT', 'IMXUSDT', this)"><span>IMX</span><span class="coin-price" id="price_IMXUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:LDOUSDT', 'LDOUSDT', this)"><span>LDO</span><span class="coin-price" id="price_LDOUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:CRVUSDT', 'CRVUSDT', this)"><span>CRV</span><span class="coin-price" id="price_CRVUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:SNXUSDT', 'SNXUSDT', this)"><span>SNX</span><span class="coin-price" id="price_SNXUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:LTCUSDT', 'LTCUSDT', this)"><span>LTC</span><span class="coin-price" id="price_LTCUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:BCHUSDT', 'BCHUSDT', this)"><span>BCH</span><span class="coin-price" id="price_BCHUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:ETCUSDT', 'ETCUSDT', this)"><span>ETC</span><span class="coin-price" id="price_ETCUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:XLMUSDT', 'XLMUSDT', this)"><span>XLM</span><span class="coin-price" id="price_XLMUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:ALGOUSDT', 'ALGOUSDT', this)"><span>ALGO</span><span class="coin-price" id="price_ALGOUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:HBARUSDT', 'HBARUSDT', this)"><span>HBAR</span><span class="coin-price" id="price_HBARUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:VETUSDT', 'VETUSDT', this)"><span>VET</span><span class="coin-price" id="price_VETUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:SANDUSDT', 'SANDUSDT', this)"><span>SAND</span><span class="coin-price" id="price_SANDUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:MANAUSDT', 'MANAUSDT', this)"><span>MANA</span><span class="coin-price" id="price_MANAUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:AXSUSDT', 'AXSUSDT', this)"><span>AXS</span><span class="coin-price" id="price_AXSUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:GALAUSDT', 'GALAUSDT', this)"><span>GALA</span><span class="coin-price" id="price_GALAUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:CHZUSDT', 'CHZUSDT', this)"><span>CHZ</span><span class="coin-price" id="price_CHZUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:ENJUSDT', 'ENJUSDT', this)"><span>ENJ</span><span class="coin-price" id="price_ENJUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:THETAUSDT', 'THETAUSDT', this)"><span>THETA</span><span class="coin-price" id="price_THETAUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:EGLDUSDT', 'EGLDUSDT', this)"><span>EGLD</span><span class="coin-price" id="price_EGLDUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:ZILUSDT', 'ZILUSDT', this)"><span>ZIL</span><span class="coin-price" id="price_ZILUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:KASUSDT', 'KASUSDT', this)"><span>KAS</span><span class="coin-price" id="price_KASUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:JUPUSDT', 'JUPUSDT', this)"><span>JUP</span><span class="coin-price" id="price_JUPUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:PYTHUSDT', 'PYTHUSDT', this)"><span>PYTH</span><span class="coin-price" id="price_PYTHUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:JTOUSDT', 'JTOUSDT', this)"><span>JTO</span><span class="coin-price" id="price_JTOUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:STRKUSDT', 'STRKUSDT', this)"><span>STRK</span><span class="coin-price" id="price_STRKUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:PORTALUSDT', 'PORTALUSDT', this)"><span>PORTAL</span><span class="coin-price" id="price_PORTALUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:AEVOUSDT', 'AEVOUSDT', this)"><span>AEVO</span><span class="coin-price" id="price_AEVOUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:BBUSDT', 'BBUSDT', this)"><span>BB</span><span class="coin-price" id="price_BBUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:NOTUSDT', 'NOTUSDT', this)"><span>NOT</span><span class="coin-price" id="price_NOTUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:IOUSDT', 'IOUSDT', this)"><span>IO</span><span class="coin-price" id="price_IOUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:ZKUSDT', 'ZKUSDT', this)"><span>ZK</span><span class="coin-price" id="price_ZKUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:ZROUSDT', 'ZROUSDT', this)"><span>ZRO</span><span class="coin-price" id="price_ZROUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:REZUSDT', 'REZUSDT', this)"><span>REZ</span><span class="coin-price" id="price_REZUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:SAGAUSDT', 'SAGAUSDT', this)"><span>SAGA</span><span class="coin-price" id="price_SAGAUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:OMUSDT', 'OMUSDT', this)"><span>OM</span><span class="coin-price" id="price_OMUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:BOMEUSDT', 'BOMEUSDT', this)"><span>BOME</span><span class="coin-price" id="price_BOMEUSDT">--</span></div>
                    <div class="coin-item" onclick="changeCoin('BINANCE:TNSRUSDT', 'TNSRUSDT', this)"><span>TNSR</span><span class="coin-price" id="price_TNSRUSDT">--</span></div>
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

            function changeCoin(symbol, ticker, element) {
                document.querySelectorAll('.coin-item').forEach(el => el.classList.remove('active'));
                element.classList.add('active');
                initChart(symbol);
                
                if(window.innerWidth <= 768) {
                    document.getElementById('sidebar').classList.remove('open');
                }
            }

            function toggleSidebar() {
                document.getElementById('sidebar').classList.toggle('open');
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

            function updatePrices() {
                fetch('https://api.binance.com/api/v3/ticker/price')
                    .then(res => res.json())
                    .then(data => {
                        let priceMap = {};
                        data.forEach(item => {
                            priceMap[item.symbol] = parseFloat(item.price).toLocaleString('en-US', {minimumFractionDigits: 2});
                        });
                        
                        let priceElements = document.querySelectorAll('.coin-price');
                        priceElements.forEach(el => {
                            let symbolKey = el.id.replace('price_', '');
                            if (priceMap[symbolKey]) {
                                el.textContent = priceMap[symbolKey];
                            }
                        });
                    }).catch(err => console.log('Fiyat çekme hatası:', err));
            }

            initChart('BINANCE:BTCUSDT');
            updatePrices();
            setInterval(updatePrices, 3000);
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
