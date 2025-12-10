"""
River-based forecasting service for AAPL stock.
Uses SNARIMAX model for online learning and prediction.
"""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional, List
from river import time_series
from core.config import TICKER, YF_PERIOD, YF_INTERVAL
from integrations.market_data.yfinance_client import get_yfinance_client, YFinanceError


class RiverManager:
    """
    Manages a single River SNARIMAX model for AAPL stock forecasting.
    Maintains state in memory (no database persistence).
    """
    
    def __init__(self):
        self.ticker = TICKER
        self.model = None
        self.last_price: Optional[float] = None
        self.last_ts: Optional[datetime] = None
        self.n_samples_trained = 0
        self._initialize_model()
        
    def _initialize_model(self):
        """Initialize the SNARIMAX model"""
        # Using SNARIMAX with reasonable defaults for financial time series
        # For 1-minute interval data, m=60 represents hourly seasonality
        self.model = time_series.SNARIMAX(
            p=1,  # AR order
            d=1,  # Differencing order
            q=1,  # MA order
            m=60, # Seasonality period (60 minutes = 1 hour for 1-minute data)
            sp=1, # Seasonal AR order
            sq=1, # Seasonal MA order
        )
        
    def warm_start(self) -> dict:
        """
        Warm start the model by fetching historical data and training.
        
        Returns:
            Dictionary with training status and statistics
        """
        try:
            yf_client = get_yfinance_client()
            df = yf_client.get_history(period=YF_PERIOD, interval=YF_INTERVAL)
            
            if df.empty:
                return {
                    "status": "error",
                    "message": "No data available for warm start",
                    "ticker": self.ticker
                }
            
            # Reset model for fresh training
            self._initialize_model()
            self.n_samples_trained = 0
            
            # Train model with historical data
            for idx, row in df.iterrows():
                price = float(row['Close'])
                timestamp = idx.to_pydatetime() if hasattr(idx, 'to_pydatetime') else idx
                
                # Learn from each observation
                self.model.learn_one(price)
                self.last_price = price
                self.last_ts = timestamp
                self.n_samples_trained += 1
            
            return {
                "status": "success",
                "message": f"Model warm-started with {self.n_samples_trained} samples",
                "ticker": self.ticker,
                "samples": self.n_samples_trained,
                "last_price": self.last_price,
                "last_timestamp": self.last_ts.isoformat() if self.last_ts else None
            }
            
        except YFinanceError as e:
            return {
                "status": "error",
                "message": f"YFinance error: {str(e)}",
                "ticker": self.ticker
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}",
                "ticker": self.ticker
            }
    
    def update_from_price(self, price: float, ts: Optional[datetime] = None):
        """
        Update the model with a new price observation.
        
        Args:
            price: New price value
            ts: Timestamp of the observation (defaults to now)
        """
        if ts is None:
            ts = datetime.now()
        
        # Learn from new observation
        self.model.learn_one(price)
        self.last_price = price
        self.last_ts = ts
        self.n_samples_trained += 1
    
    def forecast(self, horizon: int = 1) -> List[float]:
        """
        Generate price forecasts for the specified horizon.
        
        Args:
            horizon: Number of time steps to forecast
            
        Returns:
            List of predicted prices
        """
        if self.model is None or self.n_samples_trained == 0:
            return []
        
        try:
            # Use River's built-in multi-step forecasting
            forecasts = self.model.forecast(horizon=horizon)
            
            # Convert to list of floats
            if forecasts:
                return [float(f) for f in forecasts]
            return []
            
        except Exception:
            # If forecasting fails, return empty list
            return []
    
    def get_status(self) -> dict:
        """
        Get current status of the model.
        
        Returns:
            Dictionary with model status information
        """
        return {
            "ticker": self.ticker,
            "model_initialized": self.model is not None,
            "samples_trained": self.n_samples_trained,
            "last_price": self.last_price,
            "last_timestamp": self.last_ts.isoformat() if self.last_ts else None,
            "ready_for_forecast": self.n_samples_trained > 0
        }


# Global manager instance
_manager: Optional[RiverManager] = None


def get_river_manager() -> RiverManager:
    """Get or create the global River manager instance"""
    global _manager
    if _manager is None:
        _manager = RiverManager()
    return _manager
