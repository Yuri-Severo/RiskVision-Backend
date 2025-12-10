"""
Background poller for automatic AAPL price updates.
Periodically fetches latest price and updates the forecasting model.
"""
import asyncio
import logging
from datetime import datetime
from typing import Optional
from core.config import POLL_ENABLED, POLL_EVERY_SECONDS, TICKER
from services.forecast.river_service import get_river_manager
from integrations.market_data.yfinance_client import get_yfinance_client


# Configure logging
logger = logging.getLogger(__name__)


class PricePoller:
    """
    Background task that periodically fetches the latest AAPL price
    and updates the forecasting model.
    """
    
    def __init__(self):
        self.enabled = POLL_ENABLED
        self.poll_interval = POLL_EVERY_SECONDS
        self.ticker = TICKER
        self.task: Optional[asyncio.Task] = None
        self.running = False
        
    async def _poll_once(self):
        """Fetch latest price and update model"""
        try:
            yf_client = get_yfinance_client()
            manager = get_river_manager()
            
            # Get latest price
            price = yf_client.get_latest_price(period="1d", interval="1m")
            
            if price is not None:
                # Update model
                manager.update_from_price(price, datetime.now())
                logger.info(
                    f"Updated model with latest {self.ticker} price: ${price:.2f} "
                    f"(total samples: {manager.n_samples_trained})"
                )
            else:
                logger.warning(f"Failed to fetch latest price for {self.ticker}")
                
        except Exception as e:
            logger.error(f"Error in price poller: {str(e)}", exc_info=True)
    
    async def _poll_loop(self):
        """Main polling loop"""
        logger.info(
            f"Starting price poller for {self.ticker} "
            f"(interval: {self.poll_interval}s)"
        )
        
        while self.running:
            await self._poll_once()
            await asyncio.sleep(self.poll_interval)
        
        logger.info("Price poller stopped")
    
    async def start(self):
        """Start the polling task"""
        if not self.enabled:
            logger.info("Price polling disabled (POLL_ENABLED=false)")
            return
        
        if self.running:
            logger.warning("Price poller already running")
            return
        
        self.running = True
        self.task = asyncio.create_task(self._poll_loop())
        logger.info("Price poller started")
    
    async def stop(self):
        """Stop the polling task"""
        if not self.running:
            return
        
        self.running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        
        logger.info("Price poller stopped")


# Global poller instance
_poller: Optional[PricePoller] = None


def get_poller() -> PricePoller:
    """Get or create the global poller instance"""
    global _poller
    if _poller is None:
        _poller = PricePoller()
    return _poller
