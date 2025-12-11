"""
Funções auxiliares para o dashboard
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List


def format_currency(value: float) -> str:
    """Formata valor como moeda USD"""
    return f"${value:.2f}"


def format_percentage(value: float) -> str:
    """Formata valor como percentual"""
    return f"{value:.2f}%"


def format_datetime(dt_string: str) -> str:
    """Formata string de datetime para exibição"""
    try:
        dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        return dt.strftime("%d/%m/%Y %H:%M")
    except:
        return dt_string


def calculate_return(initial: float, final: float) -> float:
    """Calcula retorno percentual"""
    if initial == 0:
        return 0.0
    return ((final - initial) / initial) * 100


def calculate_volatility(prices: List[float]) -> float:
    """Calcula volatilidade (desvio padrão dos retornos)"""
    if len(prices) < 2:
        return 0.0
    
    df = pd.DataFrame({'price': prices})
    df['return'] = df['price'].pct_change()
    return df['return'].std() * 100


def calculate_moving_average(prices: List[float], window: int) -> List[float]:
    """Calcula média móvel"""
    if len(prices) < window:
        return prices
    
    df = pd.DataFrame({'price': prices})
    df['ma'] = df['price'].rolling(window=window).mean()
    return df['ma'].fillna(df['price']).tolist()


def parse_prediction_response(response: Dict[str, Any]) -> pd.DataFrame:
    """Converte resposta de previsão em DataFrame"""
    # Backend retorna 'forecast' (lista de preços) não 'predictions'
    forecast = response.get('forecast', [])
    
    if not forecast:
        return pd.DataFrame()
    
    # Criar DataFrame com índice como timestamp relativo
    df = pd.DataFrame({
        'price': forecast,
        'step': list(range(1, len(forecast) + 1))
    })
    
    # Adicionar timestamp baseado no as_of
    as_of = response.get('as_of')
    if as_of:
        base_time = pd.to_datetime(as_of)
        # Assumindo que cada step é 1 minuto
        df['timestamp'] = [base_time + pd.Timedelta(minutes=i) for i in range(len(forecast))]
    
    return df


def parse_history_response(response) -> pd.DataFrame:
    """Converte resposta de histórico em DataFrame"""
    # Verifica se a resposta é uma lista ou um dicionário
    if isinstance(response, list):
        data = response
    elif isinstance(response, dict):
        data = response.get('data', [])
    else:
        data = []
    
    df = pd.DataFrame(data)
    if not df.empty and 'date' in df.columns:
        # Converte para datetime, tratando diferentes formatos possíveis
        df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
    
    return df


def get_status_color(status: str) -> str:
    """Retorna cor baseada no status"""
    from utils.config import (
        THEME_SUCCESS_COLOR,
        THEME_ERROR_COLOR,
        THEME_WARNING_COLOR
    )
    
    status_colors = {
        'healthy': THEME_SUCCESS_COLOR,
        'warning': THEME_WARNING_COLOR,
        'error': THEME_ERROR_COLOR,
        'unhealthy': THEME_ERROR_COLOR,
    }
    
    return status_colors.get(status.lower(), THEME_WARNING_COLOR)


def generate_time_range(start: datetime, end: datetime, interval_minutes: int) -> List[datetime]:
    """Gera lista de timestamps em intervalo específico"""
    timestamps = []
    current = start
    
    while current <= end:
        timestamps.append(current)
        current += timedelta(minutes=interval_minutes)
    
    return timestamps
