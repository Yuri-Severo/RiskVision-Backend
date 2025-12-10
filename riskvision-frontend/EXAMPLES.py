"""
Exemplos de Uso do RiskVision Dashboard
Snippets de código para referência rápida
"""

# ============================================
# 1. AUTENTICAÇÃO
# ============================================

from components.api_client import get_api_client

# Obter cliente API
api = get_api_client()

# Login
if api.login(username="admin", password="senha123"):
    print("Login bem-sucedido!")
    
# Verificar autenticação
if api.is_authenticated():
    print("Usuário está autenticado")
    
# Logout
api.logout()


# ============================================
# 2. GERAR PREVISÕES
# ============================================

import streamlit as st
from components.api_client import get_api_client
from utils.helpers import parse_prediction_response

api = get_api_client()

# Gerar previsão para 60 minutos
forecast_data = api.get_forecast(horizon=60)

# Parsear resposta
if forecast_data:
    ticker = forecast_data.get('ticker', 'AAPL')
    predictions_df = parse_prediction_response(forecast_data)
    model_info = forecast_data.get('model_info', {})
    
    print(f"Ticker: {ticker}")
    print(f"Previsões: {len(predictions_df)} pontos")
    print(f"Versão do modelo: {model_info.get('version')}")


# ============================================
# 3. OBTER DADOS HISTÓRICOS
# ============================================

from utils.helpers import parse_history_response

# Buscar últimos 100 registros
history_data = api.get_history(limit=100)

# Converter para DataFrame
history_df = parse_history_response(history_data)

print(f"Registros históricos: {len(history_df)}")
print(history_df.head())


# ============================================
# 4. VERIFICAR STATUS DO MODELO
# ============================================

# Health check
health = api.get_health()

print(f"Status: {health.get('status')}")
print(f"Modelo treinado: {health.get('model_trained')}")
print(f"Total de previsões: {health.get('total_predictions')}")


# ============================================
# 5. CRIAR GRÁFICOS
# ============================================

from components.charts import (
    create_forecast_chart,
    create_candlestick_chart,
    create_line_chart
)

# Gráfico de previsão
fig = create_forecast_chart(
    historical=history_df,
    predictions=predictions_df,
    ticker="AAPL"
)
st.plotly_chart(fig, use_container_width=True)

# Gráfico candlestick
fig = create_candlestick_chart(history_df, ticker="AAPL")
st.plotly_chart(fig, use_container_width=True)

# Gráfico de linha simples
fig = create_line_chart(
    df=history_df,
    x_col='date',
    y_col='close',
    title='Preços de Fechamento'
)
st.plotly_chart(fig, use_container_width=True)


# ============================================
# 6. MÉTRICAS E CÁLCULOS
# ============================================

from utils.helpers import (
    format_currency,
    format_percentage,
    calculate_return,
    calculate_volatility,
    calculate_moving_average
)

# Formatar valores
price = 150.25
print(format_currency(price))  # "$150.25"

return_pct = 2.5
print(format_percentage(return_pct))  # "2.50%"

# Calcular retorno
initial = 100.0
final = 105.0
ret = calculate_return(initial, final)
print(f"Retorno: {ret:.2f}%")  # "5.00%"

# Calcular volatilidade
prices = [100, 102, 98, 103, 101]
vol = calculate_volatility(prices)
print(f"Volatilidade: {vol:.2f}%")

# Média móvel
ma = calculate_moving_average(prices, window=3)
print(f"Média móvel: {ma}")


# ============================================
# 7. CACHE DE DADOS
# ============================================

import streamlit as st

# Cache de função com TTL de 60 segundos
@st.cache_data(ttl=60)
def load_data():
    api = get_api_client()
    return api.get_history(limit=100)

# Usar dados cacheados
data = load_data()

# Limpar cache manualmente
st.cache_data.clear()


# ============================================
# 8. SESSION STATE
# ============================================

# Armazenar dados na sessão
st.session_state['last_forecast'] = forecast_data
st.session_state['user_preferences'] = {
    'theme': 'dark',
    'refresh_interval': 60
}

# Recuperar dados
if 'last_forecast' in st.session_state:
    forecast = st.session_state.last_forecast
    
# Verificar existência
has_data = 'last_forecast' in st.session_state


# ============================================
# 9. AUTO-REFRESH
# ============================================

from streamlit_autorefresh import st_autorefresh

# Auto-refresh a cada 60 segundos (60000 ms)
count = st_autorefresh(interval=60000, key="data_refresh")

# Condicional
refresh_interval = st.selectbox(
    "Intervalo",
    options=[0, 30, 60, 300]
)

if refresh_interval > 0:
    st_autorefresh(interval=refresh_interval * 1000, key="refresh")


# ============================================
# 10. TRATAMENTO DE ERROS
# ============================================

import streamlit as st

try:
    # Operação que pode falhar
    forecast = api.get_forecast(horizon=60)
    
    if not forecast:
        st.warning("Nenhum dado retornado pela API")
    else:
        st.success("Previsão gerada com sucesso!")
        
except Exception as e:
    st.error(f"Erro ao gerar previsão: {str(e)}")


# ============================================
# 11. FORMULÁRIOS INTERATIVOS
# ============================================

with st.form("prediction_form"):
    horizon = st.slider("Horizonte (minutos)", 1, 100, 60)
    
    ticker = st.selectbox(
        "Ticker",
        options=["AAPL", "GOOGL", "MSFT"]
    )
    
    submitted = st.form_submit_button("Gerar Previsão")
    
    if submitted:
        st.write(f"Gerando previsão para {ticker} - {horizon}min")


# ============================================
# 12. TABS E EXPANDERS
# ============================================

# Tabs
tab1, tab2, tab3 = st.tabs(["Dados", "Gráfico", "Estatísticas"])

with tab1:
    st.dataframe(history_df)
    
with tab2:
    fig = create_line_chart(history_df, 'date', 'close', 'Preços')
    st.plotly_chart(fig)
    
with tab3:
    st.metric("Média", history_df['close'].mean())

# Expander
with st.expander("Ver detalhes"):
    st.json(model_info)


# ============================================
# 13. DOWNLOAD DE ARQUIVOS
# ============================================

import pandas as pd
from datetime import datetime

# Preparar CSV
csv = predictions_df.to_csv(index=False)

# Botão de download
st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name=f"previsoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv"
)


# ============================================
# 14. SIDEBAR PERSONALIZADA
# ============================================

with st.sidebar:
    st.markdown("# 📊 Dashboard")
    st.markdown("---")
    
    # Configurações
    st.markdown("### ⚙️ Configurações")
    
    refresh = st.selectbox(
        "Auto-refresh",
        options=[0, 30, 60, 300],
        format_func=lambda x: f"{x}s" if x > 0 else "Off"
    )
    
    theme = st.radio(
        "Tema",
        options=["Dark", "Light"]
    )
    
    st.markdown("---")
    
    # Informações do usuário
    st.markdown(f"**👤 {st.session_state.get('username', 'Guest')}**")
    
    if st.button("🚪 Sair", use_container_width=True):
        api.logout()
        st.rerun()


# ============================================
# 15. LAYOUT RESPONSIVO
# ============================================

# 3 colunas
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Preço", "$150.25")
    
with col2:
    st.metric("Retorno", "+2.5%", delta="0.5%")
    
with col3:
    st.metric("Volume", "1.2M")

# Colunas com tamanhos diferentes
col_a, col_b = st.columns([2, 1])  # 2:1 ratio

with col_a:
    st.plotly_chart(fig, use_container_width=True)
    
with col_b:
    st.dataframe(history_df)


# ============================================
# 16. NOTIFICAÇÕES E FEEDBACK
# ============================================

# Success
st.success("✅ Operação concluída com sucesso!")

# Error
st.error("❌ Erro ao processar requisição")

# Warning
st.warning("⚠️ Atenção: dados incompletos")

# Info
st.info("ℹ️ Carregando dados...")

# Spinner
with st.spinner("Processando..."):
    # Operação demorada
    time.sleep(2)

# Progress bar
progress = st.progress(0)
for i in range(100):
    progress.progress(i + 1)
    
# Balloons (celebração)
st.balloons()


# ============================================
# 17. ESTILO CUSTOMIZADO
# ============================================

# CSS customizado
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #00D9FF;
        text-align: center;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# HTML customizado
st.markdown(
    '<p class="main-header">Dashboard Title</p>',
    unsafe_allow_html=True
)


# ============================================
# 18. RETREINAR MODELO
# ============================================

st.markdown("### 🔄 Retreinar Modelo")
st.markdown("Force o retreinamento com dados mais recentes.")

if st.button("🚀 Retreinar", type="primary"):
    with st.spinner("Retreinando modelo..."):
        success = api.retrain_model()
        
        if success:
            st.success("✅ Modelo retreinado!")
            st.balloons()
        else:
            st.error("❌ Erro ao retreinar")


# ============================================
# 19. VALIDAÇÃO DE INPUTS
# ============================================

# Validar antes de processar
username = st.text_input("Usuário")
password = st.text_input("Senha", type="password")

if st.button("Login"):
    if not username or not password:
        st.error("Preencha todos os campos")
    elif len(password) < 6:
        st.error("Senha deve ter no mínimo 6 caracteres")
    else:
        # Processar login
        pass


# ============================================
# 20. PÁGINA COM AUTENTICAÇÃO
# ============================================

from components.auth import require_authentication, show_logout_button

# Página protegida
st.set_page_config(
    page_title="Minha Página",
    page_icon="📊",
    layout="wide"
)

# Requer login
require_authentication()

# Conteúdo da página
st.title("Página Protegida")
st.write("Apenas usuários autenticados veem isto")

# Sidebar com logout
with st.sidebar:
    show_logout_button()


# ============================================
# FIM DOS EXEMPLOS
# ============================================

"""
Para mais exemplos, consulte:
- app.py (página principal)
- pages/1_📈_Historical.py (análise histórica)
- pages/2_⚙️_Settings.py (configurações)
- components/*.py (componentes reutilizáveis)
"""
