# 🚀 Guia de Início Rápido - RiskVision Dashboard

## Opção 1: Execução Local (Mais Rápido)

### 1. Navegue até o diretório
```bash
cd riskvision-frontend
```

### 2. Execute o script de início
```bash
chmod +x start.sh
./start.sh local
```

**Ou manualmente:**

```bash
# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instale dependências
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edite .env se necessário

# Execute
streamlit run app.py
```

### 3. Acesse o dashboard
```
http://localhost:8501
```

### 4. Faça login
Use as credenciais cadastradas na API RiskVision.

---

## Opção 2: Docker (Isolado)

### 1. Build e execute
```bash
cd riskvision-frontend
./start.sh docker
```

**Ou manualmente:**

```bash
docker build -t riskvision-dashboard .
docker run -d \
  --name riskvision-dashboard \
  -p 8501:8501 \
  -e API_URL=http://host.docker.internal:8000 \
  riskvision-dashboard
```

### 2. Acesse
```
http://localhost:8501
```

---

## Opção 3: Docker Compose (Stack Completa - RECOMENDADO)

### 1. Execute a stack completa
```bash
cd /caminho/do/RiskVision-Backend
docker-compose up -d
```

### 2. Verifique os serviços
```bash
docker-compose ps
```

Você deve ver:
- `riskvision-api` (porta 8000)
- `riskvision-dashboard` (porta 8501)
- `portainer-riskvision` (porta 9000)

### 3. Acesse os serviços

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **Dashboard** | http://localhost:8501 | Interface principal |
| **API** | http://localhost:8000 | Backend API |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **Portainer** | http://localhost:9000 | Gerenciamento Docker |

---

## Primeiros Passos no Dashboard

### 1. Login
- **URL:** http://localhost:8501
- **Credenciais:** Use as mesmas da API
- Se não tiver usuário, crie um via API primeiro

### 2. Gerar Primeira Previsão
1. Na página principal (📊 Overview)
2. Ajuste o **horizonte** (ex: 60 minutos)
3. Clique em **"🚀 Gerar Previsão"**
4. Aguarde o processamento
5. Visualize resultados no gráfico

### 3. Explorar Análise Histórica
1. Clique em **"📈 Historical"** na sidebar
2. Selecione o período desejado
3. Escolha tipo de gráfico (Candlestick recomendado)
4. Explore as abas:
   - **Dados Tabulares:** visualização tabular
   - **Distribuição:** análise estatística
   - **Retornos:** performance diária

### 4. Configurar Sistema
1. Clique em **"⚙️ Settings"** na sidebar
2. Configure **auto-refresh** conforme necessário
3. Monitore **status do modelo**
4. Execute **retreinamento** se desejar

---

## Configuração de Auto-Refresh

Na **sidebar** da página principal:

```
⚙️ Configurações
Auto-refresh: [Selecionar intervalo]
  ○ Desabilitado
  ○ 30 segundos
  ○ 1 minuto
  ○ 5 minutos
```

**Recomendado:**
- **Desenvolvimento:** Desabilitado (atualiza manualmente)
- **Monitoramento:** 1-5 minutos
- **Demo:** 30 segundos

---

## Comandos Úteis

### Docker Compose

```bash
# Ver logs de todos os serviços
docker-compose logs -f

# Ver logs apenas do dashboard
docker-compose logs -f frontend

# Parar todos os serviços
docker-compose stop

# Parar e remover containers
docker-compose down

# Rebuild de um serviço específico
docker-compose build frontend
docker-compose up -d frontend

# Restart de um serviço
docker-compose restart frontend

# Ver status
docker-compose ps
```

### Docker (container isolado)

```bash
# Ver logs
docker logs -f riskvision-dashboard

# Parar
docker stop riskvision-dashboard

# Iniciar
docker start riskvision-dashboard

# Remover
docker rm -f riskvision-dashboard

# Entrar no container
docker exec -it riskvision-dashboard /bin/bash
```

### Local (Python)

```bash
# Ativar ambiente
source venv/bin/activate

# Executar
streamlit run app.py

# Executar com auto-reload
streamlit run app.py --server.runOnSave true

# Limpar cache
streamlit cache clear

# Ver versão
streamlit --version
```

---

## Variáveis de Ambiente

Edite o arquivo `.env`:

```env
# URL da API (ajuste conforme seu setup)
API_URL=http://localhost:8000        # Local
# API_URL=http://backend:3333        # Docker Compose
# API_URL=http://192.168.1.10:8000   # Rede local

# Timeout (segundos)
API_TIMEOUT=30

# Porta do Streamlit (opcional)
STREAMLIT_PORT=8501
```

---

## Solução de Problemas Rápida

### Dashboard não conecta com API

**Erro:** "API offline" ou "Erro de conexão"

**Solução:**
1. Verifique se a API está rodando:
   ```bash
   curl http://localhost:8000/docs
   ```
2. Ajuste `API_URL` no `.env`
3. No Docker Compose, use: `API_URL=http://backend:3333`

### Erro 401 (Não autorizado)

**Erro:** "Sessão expirada"

**Solução:**
1. Faça logout (botão na sidebar)
2. Faça login novamente
3. Limpe cache do navegador
4. Verifique credenciais

### Página em branco

**Solução:**
1. Abra o console do navegador (F12)
2. Recarregue a página (Ctrl+R)
3. Limpe o cache: Settings → "Limpar Cache"
4. Restart do dashboard

### Container não inicia

**Erro:** Container para logo após iniciar

**Solução:**
```bash
# Ver logs de erro
docker logs riskvision-dashboard

# Verificar configuração
docker-compose config

# Rebuild forçado
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

---

## Próximos Passos

1. ✅ Familiarize-se com as 3 páginas principais
2. ✅ Gere algumas previsões de teste
3. ✅ Explore a análise histórica
4. ✅ Configure auto-refresh
5. ✅ Experimente retreinar o modelo
6. 📚 Leia o README completo para recursos avançados

---

## Links Úteis

- **README Completo:** `README.md`
- **Documentação API:** http://localhost:8000/docs
- **Streamlit Docs:** https://docs.streamlit.io
- **Plotly Charts:** https://plotly.com/python/

---

## Suporte

**Problemas?** 
- Verifique o README.md (seção Troubleshooting)
- Veja os logs: `docker-compose logs -f frontend`
- Abra uma issue no GitHub

**Boa navegação! 🚀📊**
