"""
Basic tests for the River forecasting service.
"""
import sys
import os
# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from unittest.mock import Mock, patch
import pandas as pd
import numpy as np
from datetime import datetime
from services.forecast.river_service import RiverManager
from integrations.market_data.yfinance_client import ThrottledYFinanceClient, YFinanceError


class TestRiverManager:
    """Test cases for RiverManager"""
    
    def test_initialization(self):
        """Test that RiverManager initializes correctly"""
        manager = RiverManager()
        assert manager.ticker == "AAPL"
        assert manager.model is not None
        assert manager.last_price is None
        assert manager.n_samples_trained == 0
    
    def test_warm_start_with_data(self):
        """Test warm_start with mocked data"""
        manager = RiverManager()
        
        # Create mock data
        dates = pd.date_range(start='2024-01-01', periods=100, freq='1min')
        mock_df = pd.DataFrame({
            'Close': np.random.uniform(150, 160, 100),
            'Open': np.random.uniform(150, 160, 100),
            'High': np.random.uniform(150, 160, 100),
            'Low': np.random.uniform(150, 160, 100),
            'Volume': np.random.randint(1000000, 2000000, 100)
        }, index=dates)
        
        with patch('services.forecast.river_service.get_yfinance_client') as mock_client:
            mock_client.return_value.get_history.return_value = mock_df
            
            result = manager.warm_start()
            
            assert result["status"] == "success"
            assert result["ticker"] == "AAPL"
            assert result["samples"] == 100
            assert manager.n_samples_trained == 100
            assert manager.last_price is not None
    
    def test_warm_start_with_empty_data(self):
        """Test warm_start with empty dataframe"""
        manager = RiverManager()
        
        with patch('services.forecast.river_service.get_yfinance_client') as mock_client:
            mock_client.return_value.get_history.return_value = pd.DataFrame()
            
            result = manager.warm_start()
            
            assert result["status"] == "error"
            assert "No data available" in result["message"]
    
    def test_forecast_returns_list(self):
        """Test that forecast returns a list of floats"""
        manager = RiverManager()
        
        # Train model with some data
        for i in range(50):
            manager.update_from_price(150.0 + i * 0.1, datetime.now())
        
        # Generate forecast
        forecasts = manager.forecast(horizon=5)
        
        assert isinstance(forecasts, list)
        # May be empty if model hasn't learned enough, but should be list
        if len(forecasts) > 0:
            assert all(isinstance(f, float) for f in forecasts)
            assert len(forecasts) <= 5
    
    def test_update_from_price(self):
        """Test updating model with new price"""
        manager = RiverManager()
        
        initial_samples = manager.n_samples_trained
        price = 155.5
        
        manager.update_from_price(price)
        
        assert manager.n_samples_trained == initial_samples + 1
        assert manager.last_price == price
        assert manager.last_ts is not None
    
    def test_get_status(self):
        """Test getting model status"""
        manager = RiverManager()
        
        status = manager.get_status()
        
        assert status["ticker"] == "AAPL"
        assert "model_initialized" in status
        assert "samples_trained" in status
        assert "ready_for_forecast" in status


class TestYFinanceClient:
    """Test cases for YFinanceClient"""
    
    def test_initialization(self):
        """Test that client initializes correctly"""
        client = ThrottledYFinanceClient()
        assert client.ticker == "AAPL"
        assert client.last_call_time is None
    
    def test_validate_period_interval_valid(self):
        """Test validation with valid period/interval"""
        client = ThrottledYFinanceClient()
        # Should not raise exception
        client._validate_period_interval("7d", "1m")
    
    def test_validate_period_interval_invalid(self):
        """Test validation with invalid period/interval"""
        client = ThrottledYFinanceClient()
        with pytest.raises(YFinanceError):
            client._validate_period_interval("30d", "1m")
    
    def test_get_history_with_mock(self):
        """Test get_history with mocked yfinance"""
        client = ThrottledYFinanceClient()
        
        # Create mock data
        dates = pd.date_range(start='2024-01-01', periods=10, freq='1min')
        mock_df = pd.DataFrame({
            'Close': np.random.uniform(150, 160, 10),
        }, index=dates)
        
        with patch('integrations.market_data.yfinance_client.yf.Ticker') as mock_ticker:
            mock_ticker.return_value.history.return_value = mock_df
            
            df = client.get_history(period="1d", interval="1m")
            
            assert not df.empty
            assert 'Close' in df.columns
    
    def test_get_latest_price_with_data(self):
        """Test getting latest price"""
        client = ThrottledYFinanceClient()
        
        dates = pd.date_range(start='2024-01-01', periods=10, freq='1min')
        mock_df = pd.DataFrame({
            'Close': [150.0, 151.0, 152.0, 153.0, 154.0, 155.0, 156.0, 157.0, 158.0, 159.0],
        }, index=dates)
        
        with patch('integrations.market_data.yfinance_client.yf.Ticker') as mock_ticker:
            mock_ticker.return_value.history.return_value = mock_df
            
            price = client.get_latest_price(period="1d", interval="1m")
            
            assert price == 159.0
    
    def test_get_latest_price_with_empty_data(self):
        """Test getting latest price with empty data"""
        client = ThrottledYFinanceClient()
        
        with patch('integrations.market_data.yfinance_client.yf.Ticker') as mock_ticker:
            mock_ticker.return_value.history.return_value = pd.DataFrame()
            
            price = client.get_latest_price(period="1d", interval="1m")
            
            assert price is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
