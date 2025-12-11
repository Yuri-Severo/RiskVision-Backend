"""
Cliente HTTP para comunicação com a API RiskVision
"""
import requests
import streamlit as st
from typing import Optional, Dict, Any, List
from datetime import datetime
from utils.config import API_URL, API_TIMEOUT


class RiskVisionAPI:
    """Cliente para interagir com a API RiskVision"""
    
    def __init__(self, base_url: str = API_URL):
        self.base_url = base_url.rstrip('/')
        self.timeout = API_TIMEOUT
    
    def _get_headers(self) -> Dict[str, str]:
        """Retorna headers com token de autenticação"""
        headers = {
            'Content-Type': 'application/json'
        }
        
        token = st.session_state.get('access_token')
        if token:
            headers['Authorization'] = f'Bearer {token}'
        
        return headers
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Trata resposta da API"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                # Token expirado ou inválido
                st.session_state.clear()
                st.error("Sessão expirada. Por favor, faça login novamente.")
                st.rerun()
            raise Exception(f"Erro HTTP {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro de conexão: {str(e)}")
    
    def login(self, username: str, password: str) -> bool:
        """
        Realiza autenticação na API
        
        Args:
            username: Nome de usuário (email)
            password: Senha
            
        Returns:
            True se autenticação bem-sucedida
        """
        try:
            response = requests.post(
                f'{self.base_url}/auth/login',
                json={'email': username, 'password': password},
                timeout=self.timeout
            )
            
            data = self._handle_response(response)
            
            # Armazena token no session_state
            st.session_state['access_token'] = data['access_token']
            st.session_state['username'] = username
            st.session_state['logged_in'] = True
            st.session_state['login_time'] = datetime.now()
            
            return True
            
        except Exception as e:
            st.error(f"Erro ao fazer login: {str(e)}")
            return False
    
    def logout(self):
        """Remove dados de autenticação"""
        for key in ['access_token', 'username', 'logged_in', 'login_time']:
            if key in st.session_state:
                del st.session_state[key]
    
    def is_authenticated(self) -> bool:
        """Verifica se usuário está autenticado"""
        return st.session_state.get('logged_in', False)
    
    def get_forecast(self, horizon: int = 60) -> Dict[str, Any]:
        """
        Obtém previsão de preços
        
        Args:
            horizon: Minutos para previsão (padrão: 60)
            
        Returns:
            Dicionário com previsões e informações do modelo
        """
        try:
            response = requests.get(
                f'{self.base_url}/forecast/',
                params={'horizon': horizon},
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            return self._handle_response(response)
            
        except Exception as e:
            st.error(f"Erro ao obter previsão: {str(e)}")
            return {}
    
    def get_health(self) -> Dict[str, Any]:
        """
        Verifica status do modelo
        
        Returns:
            Dicionário com informações de saúde do modelo
        """
        try:
            response = requests.get(
                f'{self.base_url}/forecast/health',
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            return self._handle_response(response)
            
        except Exception as e:
            st.error(f"Erro ao verificar status: {str(e)}")
            return {'status': 'error', 'model_trained': False}
    
    def get_history(self, limit: int = 100):
        """
        Obtém histórico de preços
        
        Args:
            limit: Número máximo de registros
            
        Returns:
            Lista de dados históricos ou dicionário com chave 'data'
        """
        try:
            response = requests.get(
                f'{self.base_url}/history',
                params={'limit': limit},
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            result = self._handle_response(response)
            # Retorna diretamente o resultado da API (pode ser lista ou dict)
            return result
            
        except Exception as e:
            st.error(f"Erro ao obter histórico: {str(e)}")
            return []
    
    def retrain_model(self) -> bool:
        """
        Força retreinamento do modelo
        
        Returns:
            True se retreinamento iniciado com sucesso
        """
        try:
            response = requests.post(
                f'{self.base_url}/forecast/train',
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            data = self._handle_response(response)
            st.success(data.get('message', 'Modelo retreinado com sucesso'))
            return True
            
        except Exception as e:
            st.error(f"Erro ao retreinar modelo: {str(e)}")
            return False
    
    def ping(self) -> bool:
        """
        Verifica conectividade com a API
        
        Returns:
            True se API está acessível
        """
        try:
            response = requests.get(
                f'{self.base_url}/docs',
                timeout=5
            )
            return response.status_code == 200
        except:
            return False


# Instância global do cliente API
@st.cache_resource
def get_api_client() -> RiskVisionAPI:
    """Retorna instância singleton do cliente API"""
    return RiskVisionAPI()
