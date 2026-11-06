from exchange_client import ExchangeClient
from strategy import check_sma_strategy

def main():
    print("🤖 Ticaret Botu Strateji Analizi Başlatılıyor...")
    
    # Borsa İstemcisini çağırıyoruz
    client = ExchangeClient()
    
    # Bağlantıyı test ediyoruz
    if client.test_connection():
        symbol = "BTC/USDT"
        print(f"\n🔍 {symbol} için geçmiş piyasa verileri çekiliyor...")
        
        # Son 30 mumluk veriyi alalım
        ohlcv = client.get_historical_data(symbol=symbol, timeframe="1h", limit=30)
        
        if ohlcv:
            # Stratejimizi çalıştıralım
            signal = check_sma_strategy(ohlcv)
            print(f"\n🎯 Analiz Sonucu: {signal}")

if __name__ == "__main__":
    main()


