"""
yfinance client for fetching AAPL stock data with retry logic and throttling.
"""
import time
import yfinance as yf
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from typing import Optional
from core.config import TICKER, THROTTLE_SECONDS


class YFinanceError(Exception):
    """Custom exception for yfinance errors"""
    pass


class ThrottledYFinanceClient:
    """
    yfinance client with built-in throttling and retry logic.
    Operates exclusively on AAPL ticker.
    """
    
    def __init__(self):
        self.last_call_time: Optional[float] = None
        self.ticker = TICKER
        
    def _throttle(self):
        """Apply throttling between API calls"""
        if self.last_call_time is not None:
            elapsed = time.time() - self.last_call_time
            if elapsed < THROTTLE_SECONDS:
                time.sleep(THROTTLE_SECONDS - elapsed)
        self.last_call_time = time.time()
    
    def _validate_period_interval(self, period: str, interval: str):
        """
        Validate that the period/interval combination is valid for yfinance.
        For interval=1m, period must be <= 7 days.
        """
        if interval == "1m":
            valid_periods = ["1d", "2d", "3d", "4d", "5d", "6d", "7d"]
            if period not in valid_periods:
                raise YFinanceError(
                    f"For interval=1m, period must be one of {valid_periods}. Got: {period}"
                )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    def get_history(self, period: str, interval: str) -> pd.DataFrame:
        """
        Fetch historical data for AAPL ticker.
        
        Args:
            period: Time period (e.g., "7d", "1d")
            interval: Data interval (e.g., "1m", "5m", "1h", "1d")
            
        Returns:
            DataFrame with OHLCV data
            
        Raises:
            YFinanceError: If the request fails or validation fails
        """
        # Validate period/interval combination
        self._validate_period_interval(period, interval)
        
        # Apply throttling
        self._throttle()
        
        try:
            ticker_obj = yf.Ticker(self.ticker)
            df = ticker_obj.history(period=period, interval=interval)
            
            if df is None or df.empty:
                raise YFinanceError(f"No data returned for {self.ticker}")
            
            return df
            
        except Exception as e:
            raise YFinanceError(f"Failed to fetch data for {self.ticker}: {str(e)}") from e
    
    def get_latest_price(self, period: str = "1d", interval: str = "1m") -> Optional[float]:
        """
        Get the most recent close price for AAPL.
        
        Args:
            period: Time period (default: "1d")
            interval: Data interval (default: "1m")
            
        Returns:
            Latest close price or None if unavailable
        """
        try:
            df = self.get_history(period=period, interval=interval)
            if not df.empty:
                return float(df['Close'].iloc[-1])
            return None
        except Exception:
            return None


# Global client instance
_client: Optional[ThrottledYFinanceClient] = None


def get_yfinance_client() -> ThrottledYFinanceClient:
    """Get or create the global yfinance client instance"""
    global _client
    if _client is None:
        _client = ThrottledYFinanceClient()
    return _client
