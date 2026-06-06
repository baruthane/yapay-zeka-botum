"""
Configuration module for the trading bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Binance API
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
BINANCE_TESTNET = os.getenv("BINANCE_TESTNET", "True").lower() == "true"

# Trading Configuration
TRADING_PAIRS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]
TIMEFRAMES = ["1h", "4h"]

# Position Management
MAX_POSITION_SIZE = 0.5
RISK_PER_TRADE = 0.02
MAX_DAILY_LOSS = 0.05
MAX_POSITIONS = 5

# Scoring
LONG_SCORE_THRESHOLD = 80
SHORT_SCORE_THRESHOLD = 20

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "logs/bot.log"
