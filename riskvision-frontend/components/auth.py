"""
Componente de autenticação
"""
import streamlit as st
from components.api_client import get_api_client


def show_login_page():
    """Exibe página de login"""
    st.markdown(
        """
        <style>
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 2rem;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.05);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("# 🔐 Login")
        st.markdown("### RiskVision Dashboard")
        st.markdown("---")
        
        with st.form("login_form"):
            username = st.text_input(
                "E-mail",
                placeholder="Digite seu e-mail",
                key="login_username",
                help="Use o e-mail cadastrado na API"
            )
            
            password = st.text_input(
                "Senha",
                type="password",
                placeholder="Digite sua senha",
                key="login_password"
            )
            
            submit = st.form_submit_button("Entrar", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("Por favor, preencha todos os campos")
                else:
                    with st.spinner("Autenticando..."):
                        api = get_api_client()
                        if api.login(username, password):
                            st.success("Login realizado com sucesso!")
                            st.rerun()


def require_authentication():
    """
    Decorator/função para proteger páginas que requerem autenticação
    
    Returns:
        True se usuário está autenticado, False caso contrário
    """
    api = get_api_client()
    
    if not api.is_authenticated():
        show_login_page()
        st.stop()
        return False
    
    return True


def show_logout_button():
    """Exibe botão de logout na sidebar"""
    api = get_api_client()
    
    if api.is_authenticated():
        username = st.session_state.get('username', 'Usuário')
        
        with st.sidebar:
            st.markdown("---")
            st.markdown(f"**👤 {username}**")
            
            if st.button("🚪 Sair", use_container_width=True):
                api.logout()
                st.rerun()
