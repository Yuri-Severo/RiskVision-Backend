"""
Configurações do Dashboard RiskVision
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

# Dashboard Configuration
DASHBOARD_TITLE = "RiskVision Dashboard"
DASHBOARD_ICON = "📊"
DEFAULT_TICKER = "AAPL"

# Theme Configuration
THEME_PRIMARY_COLOR = "#00D9FF"
THEME_SUCCESS_COLOR = "#00C851"
THEME_ERROR_COLOR = "#FF4444"
THEME_WARNING_COLOR = "#FFBB33"

# Auto-refresh intervals (in seconds)
REFRESH_INTERVALS = {
    "30 segundos": 30,
    "1 minuto": 60,
    "5 minutos": 300,
    "Desabilitado": 0
}

# Chart Configuration
CHART_HEIGHT = 500
CHART_TEMPLATE = "plotly_dark"

# Prediction Configuration
MIN_HORIZON = 1
MAX_HORIZON = 100
DEFAULT_HORIZON = 60
