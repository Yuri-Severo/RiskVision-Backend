# 📊 RiskVision Dashboard

Dashboard interativo em Streamlit para visualização de previsões de preços de ações geradas pela API RiskVision.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Páginas do Dashboard](#páginas-do-dashboard)
- [Docker](#docker)
- [Desenvolvimento](#desenvolvimento)
- [Troubleshooting](#troubleshooting)

## 🎯 Visão Geral

O RiskVision Dashboard é uma interface web moderna e interativa que consome a API RiskVision para:

- Visualizar previsões de preços de ações em tempo real
- Analisar dados históricos com gráficos interativos
- Monitorar status do modelo de Machine Learning
- Gerenciar configurações e controlar o sistema

## ✨ Funcionalidades

### 📊 Página Principal (Overview)
- **Previsões em tempo real** com intervalo de confiança
- **Métricas principais** em cards informativos
- **Gráfico interativo** combinando histórico e previsões
- **Tabela detalhada** de todas as previsões
- **Auto-refresh configurável** (30s, 1min, 5min)
- **Download de dados** em formato CSV

### 📈 Análise Histórica
- **Gráficos candlestick** com volume
- **Múltiplos tipos de visualização** (candlestick, linha, área)
- **Médias móveis** (7, 14, 30, 50 períodos)
- **Estatísticas do período** (retorno, volatilidade, etc.)
- **Análise de distribuição** com histogramas e box plots
- **Retornos diários** e métricas de risco

### ⚙️ Configurações e Controle
- **Status da conexão** em tempo real
- **Informações do modelo** e métricas
- **Retreinamento manual** do modelo
- **Gerenciamento de cache**
- **Logs do sistema**
- **Debug mode** para desenvolvedores

## 📦 Requisitos

### Pré-requisitos
- Python 3.10 ou superior
- API RiskVision rodando (porta 8000 por padrão)
- Docker e Docker Compose (opcional)

### Dependências Python
```
streamlit>=1.28.0
requests>=2.31.0
pandas>=2.0.0
plotly>=5.17.0
python-dotenv>=1.0.0
streamlit-autorefresh>=0.0.1
```

## 🚀 Instalação

### Opção 1: Instalação Local

1. **Clone o repositório**
```bash
cd /caminho/do/RiskVision-Backend
```

2. **Acesse o diretório do frontend**
```bash
cd riskvision-frontend
```

3. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

4. **Instale as dependências**
```bash
pip install -r requirements.txt
```

5. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

6. **Execute o dashboard**
```bash
streamlit run app.py
```

7. **Acesse no navegador**
```
http://localhost:8501
```

### Opção 2: Docker Compose (Recomendado)

1. **Certifique-se de que o docker-compose.yml está atualizado**
   - O arquivo já inclui o serviço `frontend`

2. **Suba todos os serviços**
```bash
cd /caminho/do/RiskVision-Backend
docker-compose up -d
```

3. **Verifique os containers**
```bash
docker-compose ps
```

4. **Acesse o dashboard**
```
http://localhost:8501
```

5. **Acesse a API (para testes)**
```
http://localhost:8000/docs
```

## ⚙️ Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` baseado no `.env.example`:

```env
# URL da API Backend
API_URL=http://localhost:8000

# Timeout para requisições (segundos)
API_TIMEOUT=30

# Porta do Streamlit (opcional)
STREAMLIT_PORT=8501
```

### Configuração Avançada

O arquivo `.streamlit/config.toml` permite customizar:

```toml
[theme]
primaryColor="#00D9FF"          # Cor primária (azul ciano)
backgroundColor="#0E1117"       # Cor de fundo
secondaryBackgroundColor="#262730"
textColor="#FAFAFA"
font="sans serif"

[server]
headless = true
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

## 🎮 Uso

### 1. Login

Ao acessar o dashboard pela primeira vez, você verá a tela de login:

```
Usuário: seu_usuario
Senha: sua_senha
```

**Nota:** As credenciais devem ser as mesmas cadastradas na API RiskVision.

### 2. Gerar Previsões

Na página principal:

1. Ajuste o **horizonte de previsão** (1-100 minutos)
2. Clique em **"🚀 Gerar Previsão"**
3. Visualize os resultados no gráfico e tabela
4. Baixe os dados em CSV se necessário

### 3. Analisar Histórico

Na página **"📈 Historical"**:

1. Selecione o **período** (50, 100, 200, etc. registros)
2. Escolha o **tipo de gráfico** (Candlestick, Linha, Área)
3. Configure a **média móvel** (7, 14, 30, 50 períodos)
4. Explore as abas de análise detalhada

### 4. Gerenciar Sistema

Na página **"⚙️ Settings"**:

1. Monitore o **status da conexão**
2. Veja **informações do modelo**
3. Execute **retreinamento** se necessário
4. Limpe o **cache** para forçar atualização
5. Consulte **logs recentes**

### 5. Auto-Refresh

Configure atualização automática:

1. Na sidebar, selecione o intervalo
   - 30 segundos
   - 1 minuto
   - 5 minutos
   - Desabilitado
2. Os dados serão atualizados automaticamente

## 📁 Estrutura do Projeto

```
riskvision-frontend/
├── app.py                      # Aplicação principal (página Overview)
├── requirements.txt            # Dependências Python
├── Dockerfile                  # Imagem Docker
├── .env.example                # Exemplo de variáveis de ambiente
├── .gitignore                  # Arquivos ignorados pelo Git
│
├── .streamlit/
│   └── config.toml             # Configurações do Streamlit
│
├── pages/                      # Páginas multi-page do Streamlit
│   ├── 1_📈_Historical.py     # Análise histórica
│   └── 2_⚙️_Settings.py       # Configurações e controle
│
├── components/                 # Componentes reutilizáveis
│   ├── __init__.py
│   ├── api_client.py          # Cliente HTTP para API
│   ├── auth.py                # Autenticação e login
│   └── charts.py              # Funções de plotagem
│
└── utils/                      # Utilitários
    ├── __init__.py
    ├── config.py               # Configurações globais
    └── helpers.py              # Funções auxiliares
```

## 📊 Páginas do Dashboard

### 📊 Overview (Página Principal)

**Acesso:** `http://localhost:8501`

**Componentes:**
- Status do modelo (saudável/com problemas)
- Formulário de previsão com slider de horizonte
- Gráfico combinado (histórico + previsões + confiança)
- Métricas: preço inicial, final, médio, versão do modelo
- Tabela de previsões detalhadas
- Botão de download CSV

**Fluxo:**
1. Usuário seleciona horizonte (minutos)
2. Clica em "Gerar Previsão"
3. Sistema faz POST para `/forecast`
4. Exibe resultados graficamente e tabularmente

### 📈 Historical (Análise Histórica)

**Acesso:** Sidebar → "📈 Historical"

**Componentes:**
- Filtros de período e tipo de gráfico
- Estatísticas do período (5 cards)
- Gráfico principal (candlestick/linha/área)
- Média móvel configurável
- Tabs de análise:
  - **Dados Tabulares:** tabela com últimos registros
  - **Distribuição:** histograma e box plot
  - **Retornos:** gráfico de retornos diários + estatísticas

**Métricas Calculadas:**
- Retorno do período (%)
- Volatilidade (desvio padrão)
- Volume médio
- Retornos máximo/mínimo

### ⚙️ Settings (Configurações)

**Acesso:** Sidebar → "⚙️ Settings"

**Componentes:**
- **Status da Conexão:** verifica se API está online
- **Informações do Modelo:** status, treinamento, última previsão
- **Ações:**
  - Retreinar modelo
  - Limpar cache
  - Atualizar dados
- **Sessão:** usuário, tempo de login, duração
- **Logs:** últimas 20 entradas do sistema
- **Configurações Avançadas:** tema, auto-refresh, etc.
- **Debug Mode:** session state e health check

## 🐳 Docker

### Build Manual

```bash
cd riskvision-frontend
docker build -t riskvision-dashboard .
```

### Executar Container

```bash
docker run -d \
  --name riskvision-dashboard \
  -p 8501:8501 \
  -e API_URL=http://host.docker.internal:8000 \
  riskvision-dashboard
```

### Docker Compose (Integrado)

O dashboard já está integrado ao `docker-compose.yml` do projeto principal:

```yaml
services:
  frontend:
    container_name: riskvision-dashboard
    build: ./riskvision-frontend
    ports:
      - "8501:8501"
    environment:
      API_URL: http://backend:3333
    depends_on:
      - backend
```

**Comandos úteis:**

```bash
# Subir todos os serviços
docker-compose up -d

# Ver logs do dashboard
docker-compose logs -f frontend

# Parar apenas o dashboard
docker-compose stop frontend

# Rebuild do dashboard
docker-compose build frontend
docker-compose up -d frontend

# Remover tudo
docker-compose down
```

## 💻 Desenvolvimento

### Executar em Modo Desenvolvimento

```bash
cd riskvision-frontend
streamlit run app.py --server.runOnSave true
```

**Modo watch:** O Streamlit recarrega automaticamente quando detecta mudanças nos arquivos.

### Adicionar Nova Página

1. Crie arquivo em `pages/` com formato: `N_emoji_Nome.py`
   ```python
   # pages/3_📌_NewPage.py
   import streamlit as st
   from components.auth import require_authentication
   
   require_authentication()
   
   st.title("Nova Página")
   # ... seu código
   ```

2. A página aparecerá automaticamente na sidebar

### Adicionar Novo Gráfico

1. Edite `components/charts.py`
2. Crie função que retorna `go.Figure`
   ```python
   def create_my_chart(df: pd.DataFrame) -> go.Figure:
       fig = go.Figure()
       # ... configuração
       return fig
   ```

3. Importe e use na página:
   ```python
   from components.charts import create_my_chart
   
   fig = create_my_chart(data)
   st.plotly_chart(fig, use_container_width=True)
   ```

### Customizar Tema

Edite `.streamlit/config.toml`:

```toml
[theme]
primaryColor="#YOUR_COLOR"
backgroundColor="#YOUR_BG"
```

## 🔧 Troubleshooting

### Erro de Conexão com API

**Sintoma:** "Erro de conexão" ou "API offline"

**Soluções:**
1. Verifique se a API está rodando: `curl http://localhost:8000/docs`
2. Confirme a URL no `.env`: `API_URL=http://localhost:8000`
3. No Docker, use o nome do serviço: `API_URL=http://backend:3333`

### Erro 401 Unauthorized

**Sintoma:** "Sessão expirada. Faça login novamente."

**Soluções:**
1. Faça logout e login novamente
2. Verifique credenciais na API
3. Limpe o cache do navegador
4. Restart do dashboard: `Ctrl+C` e `streamlit run app.py`

### Gráficos não aparecem

**Sintoma:** Área em branco onde deveria ter gráfico

**Soluções:**
1. Verifique se há dados: "Nenhum dado disponível"
2. Limpe cache: Settings → "Limpar Cache"
3. Verifique console do navegador (F12)
4. Reinstale plotly: `pip install --upgrade plotly`

### Dashboard lento

**Sintoma:** Páginas demorando para carregar

**Soluções:**
1. Reduza o limite de dados históricos
2. Desabilite auto-refresh
3. Limpe cache regularmente
4. Aumente RAM do container Docker

### Import Error

**Sintoma:** `ModuleNotFoundError: No module named 'X'`

**Soluções:**
1. Reinstale dependências: `pip install -r requirements.txt`
2. Verifique ambiente virtual ativado
3. No Docker: rebuild da imagem

## 📝 API Endpoints Utilizados

O dashboard consome os seguintes endpoints:

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| POST | `/auth/login` | Autenticação de usuário | ❌ |
| POST | `/forecast` | Gera previsão de preços | ✅ |
| GET | `/forecast/health` | Status do modelo | ✅ |
| GET | `/history` | Histórico de preços | ✅ |
| POST | `/forecast/train` | Retreina modelo | ✅ |

**Headers necessários:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

## 🎨 Customização

### Cores do Tema

```python
# utils/config.py
THEME_PRIMARY_COLOR = "#00D9FF"   # Azul ciano
THEME_SUCCESS_COLOR = "#00C851"   # Verde
THEME_ERROR_COLOR = "#FF4444"     # Vermelho
THEME_WARNING_COLOR = "#FFBB33"   # Amarelo
```

### Intervalos de Auto-Refresh

```python
# utils/config.py
REFRESH_INTERVALS = {
    "30 segundos": 30,
    "1 minuto": 60,
    "5 minutos": 300,
    "10 minutos": 600,  # Adicione aqui
    "Desabilitado": 0
}
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

## 👥 Autores

- **Time RiskVision** - Desenvolvimento inicial

## 📧 Suporte

Para suporte, abra uma issue no GitHub ou entre em contato com a equipe de desenvolvimento.

---

**RiskVision Dashboard v1.0** | Powered by Streamlit + FastAPI
