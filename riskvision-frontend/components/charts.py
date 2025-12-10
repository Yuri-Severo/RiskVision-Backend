"""
Componentes de gráficos para visualização de dados
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional
from utils.config import CHART_HEIGHT, CHART_TEMPLATE, THEME_PRIMARY_COLOR


def create_forecast_chart(
    historical: pd.DataFrame,
    predictions: pd.DataFrame,
    ticker: str = "AAPL"
) -> go.Figure:
    """
    Cria gráfico de previsão com histórico e intervalo de confiança
    
    Args:
        historical: DataFrame com colunas ['date', 'close']
        predictions: DataFrame com colunas ['timestamp', 'price', 'confidence_lower', 'confidence_upper']
        ticker: Símbolo da ação
        
    Returns:
        Figura Plotly
    """
    fig = go.Figure()
    
    # Linha histórica
    if not historical.empty:
        fig.add_trace(go.Scatter(
            x=historical['date'],
            y=historical['close'],
            mode='lines',
            name='Histórico',
            line=dict(color='#888888', width=2),
            hovertemplate='<b>Histórico</b><br>Data: %{x}<br>Preço: $%{y:.2f}<extra></extra>'
        ))
    
    # Linha de previsão
    if not predictions.empty:
        fig.add_trace(go.Scatter(
            x=predictions['timestamp'],
            y=predictions['price'],
            mode='lines+markers',
            name='Previsão',
            line=dict(color=THEME_PRIMARY_COLOR, width=3),
            marker=dict(size=6),
            hovertemplate='<b>Previsão</b><br>Timestamp: %{x}<br>Preço: $%{y:.2f}<extra></extra>'
        ))
        
        # Área de confiança
        if 'confidence_lower' in predictions.columns and 'confidence_upper' in predictions.columns:
            fig.add_trace(go.Scatter(
                x=predictions['timestamp'],
                y=predictions['confidence_upper'],
                mode='lines',
                name='Limite Superior',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            fig.add_trace(go.Scatter(
                x=predictions['timestamp'],
                y=predictions['confidence_lower'],
                mode='lines',
                name='Intervalo de Confiança',
                line=dict(width=0),
                fillcolor='rgba(0, 217, 255, 0.2)',
                fill='tonexty',
                hovertemplate='<b>Confiança</b><br>Min: $%{y:.2f}<extra></extra>'
            ))
    
    fig.update_layout(
        title=f'Previsão de Preço - {ticker}',
        xaxis_title='Data/Hora',
        yaxis_title='Preço (USD)',
        template=CHART_TEMPLATE,
        height=CHART_HEIGHT,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig


def create_candlestick_chart(df: pd.DataFrame, ticker: str = "AAPL") -> go.Figure:
    """
    Cria gráfico candlestick com volume
    
    Args:
        df: DataFrame com colunas ['date', 'open', 'high', 'low', 'close', 'volume']
        ticker: Símbolo da ação
        
    Returns:
        Figura Plotly com candlestick e volume
    """
    from plotly.subplots import make_subplots
    
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.7, 0.3],
        subplot_titles=(f'{ticker} - Preço', 'Volume')
    )
    
    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Preço',
            increasing_line_color='#00C851',
            decreasing_line_color='#FF4444'
        ),
        row=1, col=1
    )
    
    # Volume
    colors = ['#00C851' if close >= open else '#FF4444' 
              for close, open in zip(df['close'], df['open'])]
    
    fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['volume'],
            name='Volume',
            marker_color=colors,
            showlegend=False
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        template=CHART_TEMPLATE,
        height=CHART_HEIGHT + 200,
        xaxis_rangeslider_visible=False,
        hovermode='x unified'
    )
    
    fig.update_yaxes(title_text="Preço (USD)", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_xaxes(title_text="Data", row=2, col=1)
    
    return fig


def create_line_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str) -> go.Figure:
    """
    Cria gráfico de linha simples
    
    Args:
        df: DataFrame com dados
        x_col: Nome da coluna X
        y_col: Nome da coluna Y
        title: Título do gráfico
        
    Returns:
        Figura Plotly
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode='lines',
        name=y_col,
        line=dict(color=THEME_PRIMARY_COLOR, width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 217, 255, 0.1)'
    ))
    
    fig.update_layout(
        title=title,
        template=CHART_TEMPLATE,
        height=CHART_HEIGHT,
        hovermode='x unified'
    )
    
    return fig


def create_metric_gauge(value: float, max_value: float, title: str) -> go.Figure:
    """
    Cria gauge (medidor) para métricas
    
    Args:
        value: Valor atual
        max_value: Valor máximo
        title: Título do gauge
        
    Returns:
        Figura Plotly
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': THEME_PRIMARY_COLOR},
            'steps': [
                {'range': [0, max_value * 0.33], 'color': "rgba(0, 200, 81, 0.2)"},
                {'range': [max_value * 0.33, max_value * 0.66], 'color': "rgba(255, 187, 51, 0.2)"},
                {'range': [max_value * 0.66, max_value], 'color': "rgba(255, 68, 68, 0.2)"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.9
            }
        }
    ))
    
    fig.update_layout(
        template=CHART_TEMPLATE,
        height=300
    )
    
    return fig


def create_comparison_chart(
    actual: pd.DataFrame,
    predicted: pd.DataFrame,
    date_col: str = 'date'
) -> go.Figure:
    """
    Cria gráfico de comparação entre valores reais e previstos
    
    Args:
        actual: DataFrame com valores reais
        predicted: DataFrame com valores previstos
        date_col: Nome da coluna de data
        
    Returns:
        Figura Plotly
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=actual[date_col],
        y=actual['close'],
        mode='lines+markers',
        name='Real',
        line=dict(color='#888888', width=2),
        marker=dict(size=4)
    ))
    
    fig.add_trace(go.Scatter(
        x=predicted[date_col],
        y=predicted['price'],
        mode='lines+markers',
        name='Previsto',
        line=dict(color=THEME_PRIMARY_COLOR, width=2, dash='dash'),
        marker=dict(size=4)
    ))
    
    fig.update_layout(
        title='Comparação: Real vs Previsto',
        xaxis_title='Data',
        yaxis_title='Preço (USD)',
        template=CHART_TEMPLATE,
        height=CHART_HEIGHT,
        hovermode='x unified'
    )
    
    return fig
