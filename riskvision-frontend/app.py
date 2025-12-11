"""
RiskVision Dashboard - Aplicação Principal
Dashboard interativo para visualização de previsões de preços de ações
"""
import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

from components.auth import require_authentication, show_logout_button
from components.api_client import get_api_client
from components.charts import create_forecast_chart
from utils.config import (
    DASHBOARD_TITLE,
    DASHBOARD_ICON,
    DEFAULT_HORIZON,
    MIN_HORIZON,
    MAX_HORIZON,
    THEME_SUCCESS_COLOR,
    THEME_ERROR_COLOR,
    THEME_WARNING_COLOR
)
from utils.helpers import (
    format_currency,
    format_percentage,
    format_datetime,
    parse_prediction_response,
    parse_history_response,
    get_status_color
)

# Configuração da página
st.set_page_config(
    page_title=DASHBOARD_TITLE,
    page_icon=DASHBOARD_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00D9FF;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #00D9FF;
    }
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
    }
    .status-healthy {
        background-color: rgba(0, 200, 81, 0.2);
        color: #00C851;
    }
    .status-error {
        background-color: rgba(255, 68, 68, 0.2);
        color: #FF4444;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Requer autenticação
require_authentication()

# Sidebar
with st.sidebar:
    st.markdown("# 📊 RiskVision")
    st.markdown("### Dashboard de Previsões")
    st.markdown("---")
    
    # Auto-refresh
    st.markdown("### ⚙️ Configurações")
    refresh_interval = st.selectbox(
        "Auto-refresh",
        options=[0, 30, 60, 300],
        format_func=lambda x: {
            0: "Desabilitado",
            30: "30 segundos",
            60: "1 minuto",
            300: "5 minutos"
        }[x],
        key="refresh_interval"
    )
    
    if refresh_interval > 0:
        st_autorefresh(interval=refresh_interval * 1000, key="data_refresh")
    
    show_logout_button()

# Header principal
st.markdown('<p class="main-header">📊 RiskVision Dashboard</p>', unsafe_allow_html=True)

# Inicializa cliente API
api = get_api_client()

# Verifica status do modelo
with st.spinner("Carregando status do sistema..."):
    health = api.get_health()

# Status do modelo
col_status1, col_status2, col_status3 = st.columns([2, 1, 1])

with col_status1:
    status = health.get('status', 'error')
    status_color = get_status_color(status)
    status_text = "Saudável" if status == "healthy" else "Com Problemas"
    
    st.markdown(
        f'<span class="status-badge status-{status}">'
        f'● {status_text}'
        f'</span>',
        unsafe_allow_html=True
    )

with col_status2:
    model_trained = health.get('model_trained', False)
    st.metric(
        "Modelo Treinado",
        "✅ Sim" if model_trained else "❌ Não"
    )

with col_status3:
    total_predictions = health.get('total_predictions', 0)
    st.metric("Total de Previsões", total_predictions)

st.markdown("---")

# Seção de previsão
st.markdown("## 🎯 Gerar Nova Previsão")

col1, col2 = st.columns([3, 1])

with col1:
    horizon = st.slider(
        "Horizonte de Previsão (minutos)",
        min_value=MIN_HORIZON,
        max_value=MAX_HORIZON,
        value=DEFAULT_HORIZON,
        help="Selecione quantos minutos à frente deseja prever"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    predict_button = st.button("🚀 Gerar Previsão", use_container_width=True, type="primary")

# Armazena última previsão no session state
if 'last_forecast' not in st.session_state:
    st.session_state.last_forecast = None

if predict_button:
    with st.spinner(f"Gerando previsão para {horizon} minutos..."):
        forecast_data = api.get_forecast(horizon=horizon)
        
        if forecast_data:
            st.session_state.last_forecast = forecast_data
            st.success(f"✅ Previsão gerada com sucesso!")

# Exibe última previsão
if st.session_state.last_forecast:
    forecast_data = st.session_state.last_forecast
    ticker = forecast_data.get('ticker', 'AAPL')
    predictions_df = parse_prediction_response(forecast_data)
    last_price = forecast_data.get('last_price')
    horizon = forecast_data.get('horizon')
    as_of = forecast_data.get('as_of')
    
    st.markdown("---")
    st.markdown("## 📈 Resultado da Previsão")
    
    # Métricas da previsão
    if not predictions_df.empty:
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        first_price = predictions_df.iloc[0]['price']
        last_price = predictions_df.iloc[-1]['price']
        avg_price = predictions_df['price'].mean()
        price_change = ((last_price - first_price) / first_price) * 100
        
        with col_m1:
            st.metric(
                "Preço Inicial",
                format_currency(first_price)
            )
        
        with col_m2:
            st.metric(
                "Preço Final Previsto",
                format_currency(last_price),
                delta=format_percentage(price_change)
            )
        
        with col_m3:
            st.metric(
                "Preço Médio",
                format_currency(avg_price)
            )
        
        with col_m4:
            st.metric(
                "Horizonte",
                f"{horizon} steps" if horizon else "N/A"
            )
        
        # Informações adicionais
        if last_price and as_of:
            st.info(f"💡 **Último preço real observado:** ${last_price:.2f} | **Gerado em:** {pd.to_datetime(as_of).strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Gráfico de previsão
    st.markdown("### 📊 Visualização")
    
    # Busca dados históricos recentes
    with st.spinner("Carregando dados históricos..."):
        history_data = api.get_history(limit=50)
        history_df = parse_history_response(history_data)
    
    if not predictions_df.empty:
        fig = create_forecast_chart(history_df, predictions_df, ticker)
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabela de previsões
    st.markdown("### 📋 Detalhes das Previsões")
    
    if not predictions_df.empty:
        # Formata dataframe para exibição
        display_df = predictions_df[['timestamp', 'price', 'step']].copy()
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%d/%m/%Y %H:%M:%S')
        display_df['price'] = display_df['price'].apply(lambda x: f"${x:.2f}")
        
        # Renomeia colunas (apenas as 3 que existem)
        display_df.columns = ['Timestamp', 'Preço', 'Step']
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Botão para download
        csv = predictions_df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"previsao_{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # Informações do modelo
    with st.expander("ℹ️ Informações da Previsão"):
        col_i1, col_i2, col_i3 = st.columns(3)
        
        with col_i1:
            st.markdown(f"**Ticker:** {ticker}")
        
        with col_i2:
            if as_of:
                formatted_time = pd.to_datetime(as_of).strftime('%d/%m/%Y %H:%M:%S')
                st.markdown(f"**Gerado em:** {formatted_time}")
            else:
                st.markdown(f"**Gerado em:** N/A")
        
        with col_i3:
            st.markdown(f"**Último Preço Real:** ${last_price:.2f}" if last_price else "**Último Preço Real:** N/A")

else:
    st.info("👆 Clique em 'Gerar Previsão' para começar")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #888;'>"
    "RiskVision Dashboard v1.0 | Powered by FastAPI + Streamlit"
    "</p>",
    unsafe_allow_html=True
)
