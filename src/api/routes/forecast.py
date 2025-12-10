"""
API routes for real-time AAPL stock price forecasting.
All endpoints operate exclusively on AAPL ticker.
"""
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from core.config import TICKER, DEFAULT_FORECAST_HORIZON
from services.forecast.river_service import get_river_manager
from integrations.market_data.yfinance_client import YFinanceError


router = APIRouter(prefix="/forecast", tags=["Forecast"])


class ForecastResponse(BaseModel):
    """Response model for forecast endpoint"""
    ticker: str = Field(description="Stock ticker (always AAPL)")
    horizon: int = Field(description="Forecast horizon")
    last_price: Optional[float] = Field(description="Last observed price")
    forecast: list[float] = Field(description="Forecasted prices")
    as_of: str = Field(description="Timestamp of forecast generation")
    

class TrainResponse(BaseModel):
    """Response model for training endpoint"""
    status: str = Field(description="Training status")
    message: str = Field(description="Status message")
    ticker: str = Field(description="Stock ticker (always AAPL)")
    samples: Optional[int] = Field(default=None, description="Number of samples trained")
    last_price: Optional[float] = Field(default=None, description="Last observed price")
    

class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    model_config = {"protected_namespaces": ()}
    
    ticker: str = Field(description="Stock ticker (always AAPL)")
    model_initialized: bool = Field(description="Whether model is initialized")
    samples_trained: int = Field(description="Number of samples trained")
    last_price: Optional[float] = Field(description="Last observed price")
    last_timestamp: Optional[str] = Field(description="Timestamp of last update")
    ready_for_forecast: bool = Field(description="Whether model is ready for forecasting")


@router.get("/", response_model=ForecastResponse)
def get_forecast(
    horizon: int = Query(
        default=DEFAULT_FORECAST_HORIZON,
        ge=1,
        le=100,
        description="Number of time steps to forecast (1-100)"
    ),
    aapl_only: Optional[bool] = Query(
        default=True,
        description="Parameter to acknowledge AAPL-only operation (ignored)"
    )
):
    """
    Get price forecast for AAPL stock.
    
    This endpoint always operates on AAPL ticker, regardless of any parameters.
    The model is automatically warm-started on first use.
    
    Returns:
        Forecast data including predicted prices for the specified horizon
        
    Raises:
        503: Service unavailable if model cannot be initialized
        502: Bad gateway if yfinance service fails
    """
    manager = get_river_manager()
    
    # Auto warm-start if model not trained yet
    if manager.n_samples_trained == 0:
        try:
            result = manager.warm_start()
            if result["status"] == "error":
                # Try to determine appropriate error code
                error_msg = result.get("message", "Unknown error")
                if "YFinance" in error_msg or "fetch" in error_msg.lower():
                    raise HTTPException(
                        status_code=502,
                        detail=f"Failed to initialize model from data provider: {error_msg}"
                    )
                else:
                    raise HTTPException(
                        status_code=503,
                        detail=f"Failed to initialize forecast model: {error_msg}"
                    )
        except YFinanceError as e:
            raise HTTPException(
                status_code=502,
                detail=f"Market data provider error: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=503,
                detail=f"Service initialization error: {str(e)}"
            )
    
    # Generate forecast
    try:
        forecast_values = manager.forecast(horizon=horizon)
        
        return ForecastResponse(
            ticker=TICKER,
            horizon=horizon,
            last_price=manager.last_price,
            forecast=forecast_values,
            as_of=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate forecast: {str(e)}"
        )


@router.post("/train", response_model=TrainResponse)
def force_train():
    """
    Force a warm-start of the forecasting model.
    
    This endpoint reloads historical data and retrains the model from scratch.
    Use this to refresh the model with the latest data.
    
    Returns:
        Training status and statistics
        
    Raises:
        502: Bad gateway if yfinance service fails
        503: Service unavailable if training fails
    """
    manager = get_river_manager()
    
    try:
        result = manager.warm_start()
        
        if result["status"] == "error":
            # Determine appropriate error code
            error_msg = result.get("message", "Unknown error")
            if "YFinance" in error_msg or "fetch" in error_msg.lower():
                raise HTTPException(
                    status_code=502,
                    detail=f"Failed to fetch training data: {error_msg}"
                )
            else:
                raise HTTPException(
                    status_code=503,
                    detail=f"Training failed: {error_msg}"
                )
        
        return TrainResponse(
            status=result["status"],
            message=result["message"],
            ticker=result["ticker"],
            samples=result.get("samples"),
            last_price=result.get("last_price")
        )
        
    except HTTPException:
        raise
    except YFinanceError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Market data provider error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Training error: {str(e)}"
        )


@router.get("/health", response_model=HealthResponse)
def get_health():
    """
    Get health status of the forecasting model.
    
    Returns information about the model state, including whether it's
    initialized, trained, and ready for forecasting.
    
    Returns:
        Model health status
    """
    manager = get_river_manager()
    status = manager.get_status()
    
    return HealthResponse(
        ticker=status["ticker"],
        model_initialized=status["model_initialized"],
        samples_trained=status["samples_trained"],
        last_price=status["last_price"],
        last_timestamp=status["last_timestamp"],
        ready_for_forecast=status["ready_for_forecast"]
    )
