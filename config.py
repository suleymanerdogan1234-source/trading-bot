import os
from dotenv import load_dotenv

load_dotenv()

# Borsa ve API Bilgileri
API_KEY = os.getenv("BINANCE_API_KEY", "")
API_SECRET = os.getenv("BINANCE_API_SECRET", "")
EXCHANGE_NAME = "binance"
exchange_id = "binance"
SANDBOX_MODE = True
