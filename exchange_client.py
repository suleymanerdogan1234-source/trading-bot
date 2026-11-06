import ccxt
import config

class ExchangeClient:
    def __init__(self):
        exchange_class = getattr(ccxt, config.EXCHANGE_NAME)
        self.exchange = exchange_class({
            'apiKey': config.API_KEY,
            'secret': config.API_SECRET,
            'enableRateLimit': True,
        })
        
        if config.SANDBOX_MODE:
            try:
                self.exchange.set_sandbox_mode(True)
                print("🔒 Paper Trading (Test/Sandbox) modu aktif.")
            except Exception as e:
                print(f"⚠️ Bu borsa sandbox modunu desteklemiyor olabilir: {e}")

    def test_connection(self):
        try:
            markets = self.exchange.load_markets()
            print(f"✅ Borsaya başarıyla bağlanıldı! Aktif parite sayısı: {len(markets)}")
            return True
        except Exception as e:
            print(f"❌ Bağlantı başarısız oldu: {e}")
            return False

    def get_historical_data(self, symbol="BTC/USDT", timeframe="1h", limit=50):
        """
        Strateji hesaplaması için geçmiş mum verilerini (OHLCV) çeker.
        """
        try:
            if not self.exchange.markets:
                self.exchange.load_markets()
                
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            return ohlcv
        except Exception as e:
            print(f"❌ Veri çekme hatası ({symbol}): {e}")
            return None

# Geriye dönük uyumluluk için takma ad
ExchangeConnector = ExchangeClient