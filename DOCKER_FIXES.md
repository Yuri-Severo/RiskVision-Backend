# 🔧 Correções Aplicadas nos Arquivos de Configuração

## Resumo das Alterações

### ✅ 1. docker-compose.yml (Produção)

**Problemas corrigidos:**
- ❌ Healthcheck apontava para porta 3333, mas backend roda na 8000
- ❌ Faltavam variáveis de ambiente de forecasting (YF_PERIOD, etc)

**Alterações:**
```yaml
# ANTES:
healthcheck:
  test: ["CMD-SHELL", "curl -f http://localhost:3333/health || exit 1"]

# DEPOIS:
healthcheck:
  test: ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"]
```

**Variáveis adicionadas ao backend:**
- YF_PERIOD (padrão: 7d)
- YF_INTERVAL (padrão: 1m)
- POLL_ENABLED (padrão: true)
- POLL_EVERY_SECONDS (padrão: 60)
- THROTTLE_SECONDS (padrão: 1.0)
- DEFAULT_FORECAST_HORIZON (padrão: 1)

---

### ✅ 2. docker-compose.dev.yml (Desenvolvimento)

**Problemas corrigidos:**
- ❌ Faltavam variáveis de ambiente de forecasting
- ❌ Não tinha serviço frontend

**Alterações:**
- Adicionadas mesmas variáveis de forecasting
- Adicionado serviço `frontend` completo com:
  - API_URL: http://backend:3333 (porta dev)
  - Healthcheck configurado
  - Dependência do backend

---

### ✅ 3. Dockerfile (Backend)

**Problemas corrigidos:**
- ❌ Comando uvicorn tinha duplicação: `src.main:app` com `--app-dir src`

**Alterações:**
```dockerfile
# ANTES:
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src"]

# DEPOIS:
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src"]
```

---

### ✅ 4. .env (Backend)

**Problemas corrigidos:**
- ❌ Variáveis vazias (DATABASE_URL, POSTGRES_*)

**Alterações:**
```env
# ANTES:
DATABASE_URL=
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_USER=
POSTGRES_PASSWORD=

# DEPOIS:
DATABASE_URL=postgresql://neondb_owner:npg_pQPxN14VFnEd@...
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=docker
POSTGRES_PASSWORD=docker
```

---

### ✅ 5. riskvision-frontend/.env

**Problemas corrigidos:**
- ✅ Estava correto para uso local

**Alterações:**
- Adicionados comentários explicativos
- Criado arquivo `.env.docker` separado

---

### ✅ 6. riskvision-frontend/.env.example

**Melhorias:**
- Documentação clara sobre diferentes modos de uso:
  - Local: `http://localhost:8000`
  - Docker Compose: `http://backend:8000`
  - Rede Externa: `http://IP_DO_HOST:8000`

---

### ✅ 7. riskvision-frontend/.env.docker (NOVO)

**Arquivo criado para uso com Docker Compose:**
```env
API_URL=http://backend:8000
API_TIMEOUT=30
STREAMLIT_PORT=8501
```

---

## 📋 Checklist de Validação

### Backend
- [x] Porta correta no healthcheck (8000)
- [x] Todas variáveis de forecasting presentes
- [x] Comando uvicorn correto (sem duplicação)
- [x] .env preenchido com valores válidos

### Frontend
- [x] API_URL correto para Docker (http://backend:8000)
- [x] API_URL correto para dev (http://backend:3333)
- [x] Healthcheck funcionando
- [x] Arquivos .env documentados

### Docker Compose
- [x] Portas consistentes entre serviços
- [x] Healthchecks corretos
- [x] Dependências configuradas (depends_on)
- [x] Variáveis de ambiente completas
- [x] Frontend presente em ambos (prod e dev)

---

## 🚀 Como Usar Agora

### Modo Produção (docker-compose.yml)
```bash
# Backend na porta 8000, Frontend na 8501
docker-compose up -d

# Acessar:
# - API: http://localhost:8000
# - Dashboard: http://localhost:8501
# - Portainer: http://localhost:9000
```

### Modo Desenvolvimento (docker-compose.dev.yml)
```bash
# Backend na porta 3333 (com DB local), Frontend na 8501
docker-compose -f docker-compose.dev.yml up -d

# Acessar:
# - API: http://localhost:3333
# - Dashboard: http://localhost:8501
# - Portainer: http://localhost:9000
```

### Modo Local (sem Docker)
```bash
# Backend
cd /caminho/do/projeto
uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir src

# Frontend (em outro terminal)
cd riskvision-frontend
streamlit run app.py
```

---

## 🔍 Diferenças Entre Arquivos

### docker-compose.yml vs docker-compose.dev.yml

| Característica | docker-compose.yml | docker-compose.dev.yml |
|---------------|-------------------|----------------------|
| **Backend Port** | 8000 | 3333 |
| **Database** | Externo (Neon) | Local (PostgreSQL) |
| **Seeder** | Não | Sim (mock_data) |
| **Frontend API_URL** | http://backend:8000 | http://backend:3333 |
| **Uso** | Produção | Desenvolvimento |

---

## ⚠️ Pontos de Atenção

### 1. Variáveis Sensíveis
O arquivo `.env` contém credenciais reais do banco Neon. **NÃO COMMITAR** no Git!

```bash
# Verificar se está no .gitignore
grep -r "\.env$" .gitignore
```

### 2. Portas em Uso
Certifique-se de que as portas não estão sendo usadas:

```bash
# Verificar portas em uso
sudo lsof -i :8000  # Backend prod
sudo lsof -i :3333  # Backend dev
sudo lsof -i :8501  # Frontend
sudo lsof -i :9000  # Portainer
sudo lsof -i :5432  # PostgreSQL (apenas dev)
```

### 3. Ordem de Inicialização
O Docker Compose já gerencia a ordem correta:
1. Database (apenas dev)
2. Backend (aguarda DB saudável)
3. Frontend (aguarda Backend saudável)

### 4. Healthchecks
Todos os serviços têm healthcheck configurado. Aguarde até que estejam "healthy":

```bash
docker-compose ps
# ou
docker-compose -f docker-compose.dev.yml ps
```

---

## 🧪 Teste Rápido

```bash
# 1. Limpar ambiente anterior
docker-compose down -v

# 2. Subir stack completa
docker-compose up -d

# 3. Verificar logs
docker-compose logs -f

# 4. Testar endpoints
curl http://localhost:8000/health
curl http://localhost:8501/_stcore/health

# 5. Acessar no navegador
# Dashboard: http://localhost:8501
```

---

## 📚 Arquivos Modificados

1. ✅ `/docker-compose.yml` - Corrigido healthcheck e variáveis
2. ✅ `/docker-compose.dev.yml` - Adicionado frontend e variáveis
3. ✅ `/Dockerfile` - Corrigido comando uvicorn
4. ✅ `/.env` - Preenchido variáveis vazias
5. ✅ `/riskvision-frontend/.env` - Documentado uso local
6. ✅ `/riskvision-frontend/.env.example` - Melhorada documentação
7. ✨ `/riskvision-frontend/.env.docker` - Criado para Docker

---

**Status:** ✅ Todas as correções aplicadas com sucesso!
