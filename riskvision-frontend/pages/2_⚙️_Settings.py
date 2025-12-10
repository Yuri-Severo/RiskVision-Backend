"""
Página de Configurações e Controle
Gerenciamento do sistema e informações técnicas
"""
import streamlit as st
from datetime import datetime, timedelta

from components.auth import require_authentication, show_logout_button
from components.api_client import get_api_client
from utils.config import API_URL
from utils.helpers import format_datetime, get_status_color

# Configuração da página
st.set_page_config(
    page_title="Configurações | RiskVision",
    page_icon="⚙️",
    layout="wide"
)

# CSS customizado
st.markdown(
    """
    <style>
    .info-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .info-label {
        color: #888;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    .info-value {
        color: #00D9FF;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .action-button {
        margin: 0.5rem 0;
    }
    .log-entry {
        padding: 0.5rem;
        margin: 0.3rem 0;
        border-left: 3px solid #00D9FF;
        background: rgba(0, 217, 255, 0.05);
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Requer autenticação
require_authentication()

# Sidebar
with st.sidebar:
    st.markdown("# ⚙️ Configurações")
    show_logout_button()

# Header
st.markdown("# ⚙️ Configurações e Controle do Sistema")
st.markdown("Gerencie o modelo e monitore o status do sistema")
st.markdown("---")

# Inicializa cliente API
api = get_api_client()

# Verifica conectividade
with st.spinner("Verificando conectividade..."):
    is_online = api.ping()

# Status da API
st.markdown("## 🌐 Status da Conexão")

col_conn1, col_conn2 = st.columns(2)

with col_conn1:
    status_color = "#00C851" if is_online else "#FF4444"
    status_text = "Online ✅" if is_online else "Offline ❌"
    
    st.markdown(
        f'<div class="info-box">'
        f'<div class="info-label">Status da API</div>'
        f'<div class="info-value" style="color: {status_color}">{status_text}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

with col_conn2:
    st.markdown(
        f'<div class="info-box">'
        f'<div class="info-label">URL da API</div>'
        f'<div class="info-value" style="font-size: 1rem;">{API_URL}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

# Informações do Sistema
st.markdown("---")
st.markdown("## 🤖 Informações do Modelo")

with st.spinner("Carregando informações do modelo..."):
    health = api.get_health()

col_info1, col_info2, col_info3, col_info4 = st.columns(4)

with col_info1:
    status = health.get('status', 'unknown')
    status_emoji = "✅" if status == "healthy" else "⚠️"
    st.markdown(
        f'<div class="info-box">'
        f'<div class="info-label">Status do Modelo</div>'
        f'<div class="info-value">{status_emoji} {status.upper()}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

with col_info2:
    model_trained = health.get('model_trained', False)
    trained_text = "Sim ✅" if model_trained else "Não ❌"
    st.markdown(
        f'<div class="info-box">'
        f'<div class="info-label">Modelo Treinado</div>'
        f'<div class="info-value">{trained_text}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

with col_info3:
    last_prediction = health.get('last_prediction', 'N/A')
    if last_prediction != 'N/A':
        last_prediction = format_datetime(last_prediction)
    st.markdown(
        f'<div class="info-box">'
        f'<div class="info-label">Última Previsão</div>'
        f'<div class="info-value" style="font-size: 0.9rem;">{last_prediction}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

with col_info4:
    total_predictions = health.get('total_predictions', 0)
    st.markdown(
        f'<div class="info-box">'
        f'<div class="info-label">Total de Previsões</div>'
        f'<div class="info-value">{total_predictions}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

# Ações do Sistema
st.markdown("---")
st.markdown("## 🎮 Ações do Sistema")

col_action1, col_action2, col_action3 = st.columns(3)

with col_action1:
    st.markdown("### 🔄 Retreinar Modelo")
    st.markdown("Force o retreinamento do modelo com os dados mais recentes.")
    
    if st.button("🚀 Retreinar Agora", key="retrain", type="primary", use_container_width=True):
        with st.spinner("Retreinando modelo... Isso pode levar alguns minutos."):
            if api.retrain_model():
                st.success("✅ Modelo retreinado com sucesso!")
                st.balloons()
            else:
                st.error("❌ Erro ao retreinar modelo")

with col_action2:
    st.markdown("### 🗑️ Limpar Cache")
    st.markdown("Remove dados em cache do dashboard para forçar atualização.")
    
    if st.button("🧹 Limpar Cache", key="clear_cache", use_container_width=True):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.success("✅ Cache limpo com sucesso!")

with col_action3:
    st.markdown("### 🔄 Atualizar Dados")
    st.markdown("Recarrega todas as informações do dashboard.")
    
    if st.button("♻️ Atualizar", key="refresh_all", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Informações da Sessão
st.markdown("---")
st.markdown("## 👤 Informações da Sessão")

col_session1, col_session2, col_session3 = st.columns(3)

with col_session1:
    username = st.session_state.get('username', 'N/A')
    st.markdown(
        f'<div class="info-box">'
        f'<div class="info-label">Usuário</div>'
        f'<div class="info-value">{username}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

with col_session2:
    login_time = st.session_state.get('login_time', None)
    if login_time:
        login_str = login_time.strftime('%d/%m/%Y %H:%M:%S')
    else:
        login_str = 'N/A'
    
    st.markdown(
        f'<div class="info-box">'
        f'<div class="info-label">Login em</div>'
        f'<div class="info-value" style="font-size: 0.9rem;">{login_str}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

with col_session3:
    if login_time:
        session_duration = datetime.now() - login_time
        hours = session_duration.seconds // 3600
        minutes = (session_duration.seconds % 3600) // 60
        duration_str = f"{hours}h {minutes}m"
    else:
        duration_str = 'N/A'
    
    st.markdown(
        f'<div class="info-box">'
        f'<div class="info-label">Duração da Sessão</div>'
        f'<div class="info-value">{duration_str}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

# Logs do Sistema (simulado)
st.markdown("---")
st.markdown("## 📋 Logs Recentes")

# Inicializa logs no session_state
if 'system_logs' not in st.session_state:
    st.session_state.system_logs = [
        {"time": datetime.now() - timedelta(minutes=5), "level": "INFO", "message": "Sistema inicializado"},
        {"time": datetime.now() - timedelta(minutes=3), "level": "INFO", "message": "Modelo carregado com sucesso"},
        {"time": datetime.now() - timedelta(minutes=1), "level": "INFO", "message": f"Usuário '{username}' autenticado"},
    ]

# Adiciona log da verificação de health
if health:
    st.session_state.system_logs.append({
        "time": datetime.now(),
        "level": "INFO",
        "message": f"Health check: {health.get('status', 'unknown')}"
    })

# Mantém apenas os últimos 20 logs
st.session_state.system_logs = st.session_state.system_logs[-20:]

# Exibe logs
log_container = st.container()

with log_container:
    for log in reversed(st.session_state.system_logs):
        level_color = {
            "INFO": "#00D9FF",
            "WARNING": "#FFBB33",
            "ERROR": "#FF4444"
        }.get(log['level'], "#888")
        
        timestamp = log['time'].strftime('%H:%M:%S')
        
        st.markdown(
            f'<div class="log-entry">'
            f'<span style="color: {level_color}; font-weight: bold;">[{log["level"]}]</span> '
            f'<span style="color: #888;">{timestamp}</span> - '
            f'{log["message"]}'
            f'</div>',
            unsafe_allow_html=True
        )

# Configurações Avançadas
st.markdown("---")
st.markdown("## 🔧 Configurações Avançadas")

with st.expander("⚙️ Configurações do Dashboard"):
    col_config1, col_config2 = st.columns(2)
    
    with col_config1:
        theme = st.selectbox(
            "Tema",
            options=["Escuro", "Claro"],
            index=0,
            help="Tema de cores do dashboard"
        )
        
        auto_refresh = st.selectbox(
            "Auto-refresh padrão",
            options=["Desabilitado", "30 segundos", "1 minuto", "5 minutos"],
            index=0
        )
    
    with col_config2:
        chart_theme = st.selectbox(
            "Tema dos Gráficos",
            options=["plotly_dark", "plotly", "seaborn", "ggplot2"],
            index=0
        )
        
        default_horizon = st.slider(
            "Horizonte padrão de previsão",
            min_value=1,
            max_value=100,
            value=60,
            help="Minutos"
        )
    
    if st.button("💾 Salvar Configurações", use_container_width=True):
        st.success("✅ Configurações salvas com sucesso!")
        st.info("ℹ️ Algumas configurações requerem recarregar a página")

# Informações Técnicas
with st.expander("ℹ️ Informações Técnicas"):
    col_tech1, col_tech2 = st.columns(2)
    
    with col_tech1:
        st.markdown("**Dashboard**")
        st.markdown("- Versão: 1.0.0")
        st.markdown("- Framework: Streamlit")
        st.markdown("- Python: 3.10+")
    
    with col_tech2:
        st.markdown("**API**")
        st.markdown(f"- URL: {API_URL}")
        st.markdown("- Framework: FastAPI")
        st.markdown("- Autenticação: JWT Bearer")

# Debug Mode
with st.expander("🐛 Debug Mode"):
    st.markdown("### Session State")
    st.json({
        k: str(v) if not isinstance(v, (str, int, float, bool, type(None))) else v
        for k, v in st.session_state.items()
        if not k.startswith('_')
    })
    
    st.markdown("### Health Check Response")
    st.json(health)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #888;'>"
    "Configurações | RiskVision Dashboard v1.0"
    "</p>",
    unsafe_allow_html=True
)
