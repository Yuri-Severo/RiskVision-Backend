"""
Página de Análise Histórica
Visualização detalhada dos dados históricos de preços
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

from components.auth import require_authentication, show_logout_button
from components.api_client import get_api_client
from components.charts import create_candlestick_chart, create_line_chart
from utils.config import CHART_HEIGHT, CHART_TEMPLATE, THEME_PRIMARY_COLOR
from utils.helpers import (
    format_currency,
    format_percentage,
    calculate_return,
    calculate_volatility,
    calculate_moving_average,
    parse_history_response
)

# Configuração da página
st.set_page_config(
    page_title="Análise Histórica | RiskVision",
    page_icon="📈",
    layout="wide"
)

# CSS customizado
st.markdown(
    """
    <style>
    .stat-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #888;
        margin-bottom: 0.5rem;
    }
    .stat-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #00D9FF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Requer autenticação
require_authentication()

# Sidebar
with st.sidebar:
    st.markdown("# 📈 Análise Histórica")
    show_logout_button()

# Header
st.markdown("# 📈 Análise Histórica de Preços")
st.markdown("Explore dados históricos e estatísticas detalhadas")
st.markdown("---")

# Inicializa cliente API
api = get_api_client()

# Controles de filtro
col_filter1, col_filter2, col_filter3 = st.columns(3)

with col_filter1:
    limit = st.selectbox(
        "Período",
        options=[50, 100, 200, 500, 1000],
        index=1,
        format_func=lambda x: f"Últimos {x} registros"
    )

with col_filter2:
    chart_type = st.selectbox(
        "Tipo de Visualização",
        options=["Candlestick", "Linha", "Área"],
        index=0
    )

with col_filter3:
    ma_window = st.selectbox(
        "Média Móvel",
        options=[7, 14, 30, 50],
        format_func=lambda x: f"{x} períodos"
    )

# Botão de atualização
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
with col_btn1:
    refresh_button = st.button("🔄 Atualizar Dados", use_container_width=True)

# Carrega dados históricos
@st.cache_data(ttl=60)
def load_historical_data(limit_value):
    """Carrega e cacheia dados históricos"""
    history_data = api.get_history(limit=limit_value)
    return parse_history_response(history_data)

if refresh_button:
    st.cache_data.clear()

with st.spinner("Carregando dados históricos..."):
    df = load_historical_data(limit)

if df.empty:
    st.warning("⚠️ Nenhum dado histórico disponível")
    st.stop()

# Ordena por data
df = df.sort_values('date')

# Estatísticas principais
st.markdown("## 📊 Estatísticas do Período")

col_stat1, col_stat2, col_stat3, col_stat4, col_stat5 = st.columns(5)

first_close = df.iloc[0]['close']
last_close = df.iloc[-1]['close']
period_return = calculate_return(first_close, last_close)
volatility = calculate_volatility(df['close'].tolist())
avg_volume = df['volume'].mean()

with col_stat1:
    st.markdown(
        f'<div class="stat-card">'
        f'<div class="stat-label">Preço Inicial</div>'
        f'<div class="stat-value">{format_currency(first_close)}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

with col_stat2:
    st.markdown(
        f'<div class="stat-card">'
        f'<div class="stat-label">Preço Atual</div>'
        f'<div class="stat-value">{format_currency(last_close)}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

with col_stat3:
    return_color = "#00C851" if period_return >= 0 else "#FF4444"
    st.markdown(
        f'<div class="stat-card">'
        f'<div class="stat-label">Retorno</div>'
        f'<div class="stat-value" style="color: {return_color}">{format_percentage(period_return)}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

with col_stat4:
    st.markdown(
        f'<div class="stat-card">'
        f'<div class="stat-label">Volatilidade</div>'
        f'<div class="stat-value">{format_percentage(volatility)}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

with col_stat5:
    st.markdown(
        f'<div class="stat-card">'
        f'<div class="stat-label">Volume Médio</div>'
        f'<div class="stat-value">{avg_volume:,.0f}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

st.markdown("---")

# Gráfico principal
st.markdown("## 📈 Visualização de Preços")

if chart_type == "Candlestick":
    fig = create_candlestick_chart(df)
    st.plotly_chart(fig, use_container_width=True)
else:
    # Adiciona média móvel
    df['ma'] = calculate_moving_average(df['close'].tolist(), ma_window)
    
    fig = go.Figure()
    
    if chart_type == "Área":
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['close'],
            mode='lines',
            name='Preço',
            line=dict(color=THEME_PRIMARY_COLOR, width=2),
            fill='tozeroy',
            fillcolor='rgba(0, 217, 255, 0.1)'
        ))
    else:  # Linha
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['close'],
            mode='lines',
            name='Preço',
            line=dict(color=THEME_PRIMARY_COLOR, width=2)
        ))
    
    # Adiciona média móvel
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['ma'],
        mode='lines',
        name=f'MA {ma_window}',
        line=dict(color='#FFBB33', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title='Histórico de Preços',
        xaxis_title='Data',
        yaxis_title='Preço (USD)',
        template=CHART_TEMPLATE,
        height=CHART_HEIGHT,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Análise detalhada
st.markdown("---")
st.markdown("## 🔍 Análise Detalhada")

tab1, tab2, tab3 = st.tabs(["📋 Dados Tabulares", "📊 Distribuição", "📈 Retornos"])

with tab1:
    st.markdown("### Últimos Registros")
    
    # Formata dataframe para exibição
    display_df = df.tail(20).copy()
    
    # Garante que 'date' é datetime antes de formatar
    if not pd.api.types.is_datetime64_any_dtype(display_df['date']):
        display_df['date'] = pd.to_datetime(display_df['date'], errors='coerce')
    
    display_df['date'] = display_df['date'].dt.strftime('%d/%m/%Y')
    display_df['open'] = display_df['open'].apply(lambda x: f"${x:.2f}")
    display_df['high'] = display_df['high'].apply(lambda x: f"${x:.2f}")
    display_df['low'] = display_df['low'].apply(lambda x: f"${x:.2f}")
    display_df['close'] = display_df['close'].apply(lambda x: f"${x:.2f}")
    display_df['volume'] = display_df['volume'].apply(lambda x: f"{x:,.0f}")
    
    # Renomeia colunas
    display_df = display_df[['date', 'open', 'high', 'low', 'close', 'volume']]
    display_df.columns = ['Data', 'Abertura', 'Máxima', 'Mínima', 'Fechamento', 'Volume']
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Download
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV Completo",
        data=csv,
        file_name=f"historico_precos_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with tab2:
    st.markdown("### Distribuição de Preços")
    
    import plotly.express as px
    
    fig_hist = px.histogram(
        df,
        x='close',
        nbins=30,
        title='Distribuição de Preços de Fechamento',
        labels={'close': 'Preço (USD)', 'count': 'Frequência'}
    )
    fig_hist.update_layout(
        template=CHART_TEMPLATE,
        showlegend=False
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Box plot
    fig_box = px.box(
        df,
        y='close',
        title='Box Plot - Preços de Fechamento',
        labels={'close': 'Preço (USD)'}
    )
    fig_box.update_layout(template=CHART_TEMPLATE)
    st.plotly_chart(fig_box, use_container_width=True)

with tab3:
    st.markdown("### Retornos Diários")
    
    # Calcula retornos
    df['daily_return'] = df['close'].pct_change() * 100
    
    fig_returns = create_line_chart(
        df.dropna(),
        'date',
        'daily_return',
        'Retornos Diários (%)'
    )
    st.plotly_chart(fig_returns, use_container_width=True)
    
    # Estatísticas de retornos
    col_ret1, col_ret2, col_ret3, col_ret4 = st.columns(4)
    
    with col_ret1:
        st.metric("Retorno Médio", f"{df['daily_return'].mean():.2f}%")
    
    with col_ret2:
        st.metric("Desvio Padrão", f"{df['daily_return'].std():.2f}%")
    
    with col_ret3:
        st.metric("Retorno Máximo", f"{df['daily_return'].max():.2f}%")
    
    with col_ret4:
        st.metric("Retorno Mínimo", f"{df['daily_return'].min():.2f}%")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #888;'>"
    "Análise Histórica | RiskVision Dashboard"
    "</p>",
    unsafe_allow_html=True
)
