def calculate_sma(prices, period=20):
    """
    Basit Hareketli Ortalama (SMA) hesaplar.
    """
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period

def check_sma_strategy(ohlcv_data, short_period=10, long_period=20):
    """
    Kısa ve uzun vadeli hareketli ortalamaların kesişimine göre sinyal üretir.
    """
    if not ohlcv_data or len(ohlcv_data) < long_period:
        return "BEKLE (Yetersiz Veri)"

    # OHLCV verisinden sadece kapanış (close) fiyatlarını alıyoruz (index 4)
    closes = [candle[4] for candle in ohlcv_data]

    short_sma = calculate_sma(closes, short_period)
    long_sma = calculate_sma(closes, long_period)

    print(f"📊 Kısa SMA ({short_period}): {short_sma:.2f} | Uzun SMA ({long_period}): {long_sma:.2f}")

    if short_sma > long_sma:
        return "ALIM SİNYALİ (BUY) 🟢"
    elif short_sma < long_sma:
        return "SATIM SİNYALİ (SELL) 🔴"
    else:
        return "NÖTR"