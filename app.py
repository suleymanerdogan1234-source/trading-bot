from flask import Flask, render_template_string, jsonify, request
from exchange_client import ExchangeClient
from strategy import check_sma_strategy
import json
import pandas as pd

app = Flask(__name__)

def get_sma_data(ohlcv, period=200):
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['sma'] = df['close'].rolling(window=period).mean()
    sma_data = []
    for _, row in df.iterrows():
        if pd.notna(row['sma']):
            timestamp = int(row['timestamp'] / 1000)
            sma_data.append({"time": timestamp, "value": row['sma']})
    return sma_data

@app.route("/")
def index():
    try:
        timeframe = request.args.get('tf', '1h')
        client = ExchangeClient()
        ohlcv = client.get_historical_data("BTC/USDT", timeframe=timeframe, limit=300)
        signal = check_sma_strategy(ohlcv)
        
        chart_data = []
        for candle in ohlcv:
            timestamp = int(candle[0] / 1000)
            chart_data.append({
                "time": timestamp,
                "open": candle[1],
                "high": candle[2],
                "low": candle[3],
                "close": candle[4]
            })
            
        sma200_data = get_sma_data(ohlcv, period=200)
        current_price = chart_data[-1]["close"] if chart_data else 0
        current_sma200 = sma200_data[-1]["value"] if sma200_data else 0
        
        html_code = """
        <!DOCTYPE html>
        <html lang="tr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dijitaltrade - Kripto Sinyal Botu</title>
            <link rel="manifest" href="/static/manifest.json">
            <meta name="apple-mobile-web-app-capable" content="yes">
            <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
            <meta name="apple-mobile-web-app-title" content="Dijitaltrade">
            <meta name="theme-color" content="#1e293b">
            <script src="https://unpkg.com/lightweight-charts@4.1.1/dist/lightweight-charts.standalone.production.js"></script>
            <style>
                html, body {
                    margin: 0;
                    padding: 0;
                    width: 100%;
                    height: 100%;
                    background: #0f172a;
                    color: #f8fafc;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    overflow: hidden;
                }
                .header {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: calc(100% - 32px);
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 8px 16px;
                    background: #1e293b;
                    border-bottom: 1px solid #334155;
                    z-index: 20;
                    height: 24px;
                }
                .pair-info { font-size: 1.1em; font-weight: bold; }
                .price { color: #38bdf8; font-size: 1.1em; font-weight: bold; }
                
                .timeframes {
                    position: absolute;
                    top: 41px;
                    left: 0;
                    width: calc(100% - 32px);
                    display: flex;
                    gap: 15px;
                    padding: 6px 16px;
                    background: #1e293b;
                    font-size: 0.85em;
                    color: #94a3b8;
                    border-bottom: 1px solid #334155;
                    align-items: center;
                    z-index: 20;
                    height: 20px;
                }
                .tf-btn {
                    background: none;
                    border: none;
                    color: #94a3b8;
                    cursor: pointer;
                    font-size: 1em;
                    padding: 2px 6px;
                    border-radius: 4px;
                }
                .tf-btn.active {
                    color: #f59e0b;
                    font-weight: bold;
                    background: rgba(245, 158, 11, 0.1);
                    border-bottom: 2px solid #f59e0b;
                }

                #chart-container {
                    position: absolute;
                    top: 74px;
                    bottom: 49px;
                    left: 0;
                    width: 100%;
                    background: #0f172a;
                }

                .signal-overlay {
                    position: absolute;
                    top: 15px;
                    right: 15px;
                    background: rgba(30, 41, 59, 0.9);
                    padding: 10px 14px;
                    border-radius: 8px;
                    border: 1px solid #334155;
                    z-index: 10;
                    font-size: 0.8em;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
                }

                .bottom-nav {
                    position: absolute;
                    bottom: 0;
                    left: 0;
                    width: 100%;
                    display: flex;
                    justify-content: space-around;
                    background: #1e293b;
                    padding: 6px 0;
                    border-top: 1px solid #334155;
                    z-index: 20;
                    height: 36px;
                }
                .nav-item {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    color: #94a3b8;
                    text-decoration: none;
                    font-size: 0.75em;
                    gap: 2px;
                }
                .nav-item.active {
                    color: #f59e0b;
                    font-weight: bold;
                }
                .nav-icon { font-size: 1.2em; }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="pair-info"><span>🚀 Dijitaltrade | BTC/USDT (Binance)</span></div>
                <div class="price" id="price-display">{{ current_price | round(2) }} USDT <span style="font-size: 0.8em; color: #f59e0b; margin-left: 10px;">SMA 200: <span id="sma-display">{{ current_sma200 | round(2) }}</span></span></div>
            </div>

            <div class="timeframes">
                <button class="tf-btn {% if current_tf == '1m' %}active{% endif %}" onclick="changeTf('1m')">1dk</button>
                <button class="tf-btn {% if current_tf == '5m' %}active{% endif %}" onclick="changeTf('5m')">5dk</button>
                <button class="tf-btn {% if current_tf == '15m' %}active{% endif %}" onclick="changeTf('15m')">15dk</button>
                <button class="tf-btn {% if current_tf == '30m' %}active{% endif %}" onclick="changeTf('30m')">30dk</button>
                <button class="tf-btn {% if current_tf == '1h' %}active{% endif %}" onclick="changeTf('1h')">1sa</button>
                <button class="tf-btn {% if current_tf == '4h' %}active{% endif %}" onclick="changeTf('4h')">4sa</button>
                <button class="tf-btn {% if current_tf == '1d' %}active{% endif %}" onclick="changeTf('1d')">Günlük</button>
            </div>

            <div id="chart-container">
                <div class="signal-overlay">
                    <div><b>Strateji:</b> <span id="signal-display" style="color: {% if 'AL' in signal %}#22c55e{% else %}#ef4444{% endif %};">{{ signal }}</span></div>
                </div>
            </div>

            <div class="bottom-nav">
                <a href="#" class="nav-item"><span class="nav-icon">📊</span><span>Panel</span></a>
                <a href="#" class="nav-item"><span class="nav-icon">💰</span><span>Kasa</span></a>
                <a href="#" class="nav-item active"><span class="nav-icon">📈</span><span>Grafik</span></a>
                <a href="#" class="nav-item"><span class="nav-icon">🎓</span><span>Eğitim</span></a>
                <a href="#" class="nav-item"><span class="nav-icon">🌐</span><span>Meydan</span></a>
            </div>

            <script>
                function changeTf(tf) {
                    window.location.href = "/?tf=" + tf;
                }

                const container = document.getElementById('chart-container');
                const chart = LightweightCharts.createChart(container, {
                    width: container.clientWidth,
                    height: container.clientHeight,
                    layout: {
                        background: { type: 'solid', color: '#0f172a' },
                        textColor: '#94a3b8',
                    },
                    grid: {
                        vertLines: { color: '#1e293b' },
                        horzLines: { color: '#1e293b' },
                    },
                    timeScale: {
                        timeVisible: true,
                        secondsVisible: false,
                    },
                });

                const candlestickSeries = chart.addCandlestickSeries({
                    upColor: '#22c55e',
                    downColor: '#ef4444',
                    borderVisible: false,
                    wickUpColor: '#22c55e',
                    wickDownColor: '#ef4444',
                });

                const candleData = {{ chart_data | safe }};
                candlestickSeries.setData(candleData);

                const smaSeries = chart.addLineSeries({
                    color: '#a855f7',
                    lineWidth: 2,
                });
                const smaData = {{ sma200_data | safe }};
                smaSeries.setData(smaData);

                chart.timeScale().fitContent();

                window.addEventListener('resize', () => {
                    chart.applyOptions({ 
                        width: container.clientWidth,
                        height: container.clientHeight 
                    });
                });

                setInterval(async () => {
                    try {
                        const response = await fetch('/api/ticker?tf={{ current_tf }}');
                        const data = await response.json();
                        
                        document.getElementById('price-display').innerText = data.price.toFixed(2) + ' USDT';
                        document.getElementById('signal-display').innerText = data.signal;
                        
                        if (data.signal.includes('AL')) {
                            document.getElementById('signal-display').style.color = '#22c55e';
                        } else {
                            document.getElementById('signal-display').style.color = '#ef4444';
                        }

                        if (candleData.length > 0) {
                            const lastCandle = candleData[candleData.length - 1];
                            lastCandle.close = data.price;
                            if (data.price > lastCandle.high) lastCandle.high = data.price;
                            if (data.price < lastCandle.low) lastCandle.low = data.price;
                            candlestickSeries.update(lastCandle);
                        }
                    } catch (error) {
                        console.error('Fiyat güncellenirken hata oluştu:', error);
                    }
                }, 20000);
            </script>
        </body>
        </html>
        """
        return render_template_string(html_code, signal=signal, current_price=current_price, current_sma200=current_sma200, chart_data=json.dumps(chart_data), sma200_data=json.dumps(sma200_data), current_tf=timeframe)
    except Exception as e:
        return f"Hata oluştu: {e}"

@app.route("/api/ticker")
def api_ticker():
    try:
        timeframe = request.args.get('tf', '1h')
        client = ExchangeClient()
        ohlcv = client.get_historical_data("BTC/USDT", timeframe=timeframe, limit=300)
        signal = check_sma_strategy(ohlcv)
        current_price = ohlcv[-1][4] if ohlcv else 0
        return jsonify({"price": current_price, "signal": signal})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)