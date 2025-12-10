"""
Configuration for the AAPL forecasting service.
This service operates exclusively with Apple (AAPL) stock ticker.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Fixed ticker - Only AAPL is supported
TICKER = "AAPL"

# yfinance configuration
YF_PERIOD = os.getenv("YF_PERIOD", "7d")  # Compatible with interval=1m (max 7 days)
YF_INTERVAL = os.getenv("YF_INTERVAL", "1m")  # 1-minute intervals

# Background polling configuration
POLL_ENABLED = os.getenv("POLL_ENABLED", "true").lower() == "true"
POLL_EVERY_SECONDS = int(os.getenv("POLL_EVERY_SECONDS", "60"))

# Throttling configuration (seconds between API calls)
THROTTLE_SECONDS = float(os.getenv("THROTTLE_SECONDS", "1.0"))

# Model parameters
DEFAULT_FORECAST_HORIZON = int(os.getenv("DEFAULT_FORECAST_HORIZON", "1"))
