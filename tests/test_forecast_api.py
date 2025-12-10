"""
Integration tests for the forecast API endpoints.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import pandas as pd
import numpy as np
from main import app


client = TestClient(app)


class TestForecastAPI:
    """Integration tests for forecast endpoints"""
    
    def test_health_endpoint(self):
        """Test main health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
    
    def test_forecast_health_endpoint(self):
        """Test forecast health endpoint"""
        response = client.get("/forecast/health")
        assert response.status_code == 200
        data = response.json()
        assert data["ticker"] == "AAPL"
        assert "model_initialized" in data
        assert "samples_trained" in data
        assert "ready_for_forecast" in data
    
    def test_forecast_endpoint_with_mock_data(self):
        """Test forecast endpoint with mocked yfinance data"""
        # Create mock data
        dates = pd.date_range(start='2024-01-01', periods=100, freq='1min')
        mock_df = pd.DataFrame({
            'Close': np.random.uniform(150, 160, 100),
            'Open': np.random.uniform(150, 160, 100),
            'High': np.random.uniform(150, 160, 100),
            'Low': np.random.uniform(150, 160, 100),
            'Volume': np.random.randint(1000000, 2000000, 100)
        }, index=dates)
        
        with patch('integrations.market_data.yfinance_client.yf.Ticker') as mock_ticker:
            mock_ticker.return_value.history.return_value = mock_df
            
            response = client.get("/forecast/?horizon=5")
            assert response.status_code == 200
            
            data = response.json()
            assert data["ticker"] == "AAPL"
            assert data["horizon"] == 5
            assert "forecast" in data
            assert "last_price" in data
            assert "as_of" in data
    
    def test_forecast_train_endpoint_with_mock_data(self):
        """Test forecast train endpoint with mocked yfinance data"""
        # Create mock data
        dates = pd.date_range(start='2024-01-01', periods=100, freq='1min')
        mock_df = pd.DataFrame({
            'Close': np.random.uniform(150, 160, 100),
            'Open': np.random.uniform(150, 160, 100),
            'High': np.random.uniform(150, 160, 100),
            'Low': np.random.uniform(150, 160, 100),
            'Volume': np.random.randint(1000000, 2000000, 100)
        }, index=dates)
        
        with patch('integrations.market_data.yfinance_client.yf.Ticker') as mock_ticker:
            mock_ticker.return_value.history.return_value = mock_df
            
            response = client.post("/forecast/train")
            assert response.status_code == 200
            
            data = response.json()
            assert data["status"] == "success"
            assert data["ticker"] == "AAPL"
            assert data["samples"] == 100
    
    def test_forecast_with_invalid_horizon(self):
        """Test forecast endpoint with invalid horizon"""
        response = client.get("/forecast/?horizon=0")
        assert response.status_code == 422  # Validation error
        
        response = client.get("/forecast/?horizon=101")
        assert response.status_code == 422  # Validation error


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
