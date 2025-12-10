# Guia de Coleta de Dados de Ações - RiskVision

## 📊 Visão Geral

O sistema RiskVision inclui um coletor automático de dados de ações que utiliza a API do yFinance para buscar dados em tempo real e armazená-los no banco de dados PostgreSQL.

## 🚀 Modos de Execução

### 1. **Modo API com Scheduler Integrado**

Execute a API FastAPI com o scheduler de coleta integrado:

```bash
# Localmente
ENABLE_STOCK_SCHEDULER=true uvicorn main:app --host 0.0.0.0 --port 3333 --app-dir src

# Com Docker
docker-compose -f docker-compose.dev.yml up backend
```

> **Nota:** O scheduler só inicia se `ENABLE_STOCK_SCHEDULER=true`

### 2. **Modo Coletor Standalone**

Execute apenas o coletor de dados (sem API):

```bash
# Localmente
python scripts/run_data_collector.py

# Com Docker
docker-compose -f docker-compose.dev.yml --profile with-collector up data-collector
```

### 3. **Modo Completo (API + Coletor Separados)**

Execute ambos simultaneamente em containers separados:

```bash
docker-compose -f docker-compose.dev.yml --profile with-collector up
```

Isso inicia:

- `db` - Banco de dados PostgreSQL
- `backend` - API FastAPI (porta 3333)
- `data-collector` - Coletor de dados standalone
- `frontend` - Interface web (porta 3000)
- `portainer` - Gerenciamento Docker (porta 9000)

## ⚙️ Configuração

### Variáveis de Ambiente

Adicione ao seu arquivo `.env`:

```env
# Configurações de banco de dados (já existentes)
DATABASE_URL=postgresql://user:pass@host:port/db
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=senha
POSTGRES_DB=riskvision

# Configurações do coletor de dados de ações
STOCK_TICKERS=AAPL,GOOGL,MSFT          # Lista de ações separadas por vírgula
STOCK_COLLECTION_INTERVAL_MINUTES=5     # Intervalo entre coletas (minutos)
STOCK_COLLECTION_PERIOD=1d              # Período de dados (1d, 5d, 1mo, etc)
STOCK_DATA_INTERVAL=1m                  # Intervalo dos dados (1m, 5m, 1h, etc)

# Habilitar scheduler na API (opcional)
ENABLE_STOCK_SCHEDULER=false            # true para ativar scheduler na API

# Configurações de retry
MAX_RETRY_ATTEMPTS=3                    # Máximo de tentativas em caso de erro
RETRY_DELAY_SECONDS=5                   # Delay entre tentativas
```

### Tickers Suportados

Qualquer ticker suportado pelo Yahoo Finance:

- **Ações US:** AAPL, GOOGL, MSFT, TSLA, AMZN, etc.
- **Ações BR:** PETR4.SA, VALE3.SA, ITUB4.SA, etc.
- **Índices:** ^GSPC (S&P 500), ^DJI (Dow Jones), ^BVSP (Ibovespa)
- **Criptomoedas:** BTC-USD, ETH-USD, etc.

### Intervalos de Coleta Recomendados

| Uso            | Intervalo         | Period | Data Interval |
| -------------- | ----------------- | ------ | ------------- |
| **Tempo Real** | 1-5 min           | 1d     | 1m            |
| **Intraday**   | 15-30 min         | 1d     | 5m            |
| **Diário**     | 1440 min (1x/dia) | 5d     | 1d            |
| **Semanal**    | 10080 min         | 1mo    | 1wk           |

## 📡 Endpoints da API

### Verificar Status do Scheduler

```bash
GET /scheduler/status
```

Resposta:

```json
{
  "running": true,
  "enabled": true,
  "interval_minutes": 5,
  "tickers": ["AAPL", "GOOGL"],
  "jobs": [
    {
      "id": "collect_stock_data",
      "name": "Coletar dados de ações do yFinance",
      "next_run": "2024-12-09 15:30:00",
      "trigger": "interval[0:05:00]"
    }
  ]
}
```

### Buscar Dados da Apple

```bash
GET /stocks/apple?period=1d&interval=1m
```

### Buscar Histórico do Banco

```bash
GET /history/?period=day
```

Parâmetros: `day`, `week`, `semester`, `year`

## 🐳 Comandos Docker

### Iniciar apenas API

```bash
docker-compose -f docker-compose.dev.yml up backend
```

### Iniciar apenas Coletor

```bash
docker-compose -f docker-compose.dev.yml --profile with-collector up data-collector
```

### Iniciar tudo (API + Coletor)

```bash
docker-compose -f docker-compose.dev.yml --profile with-collector up
```

### Parar serviços

```bash
docker-compose -f docker-compose.dev.yml down
```

### Ver logs do coletor

```bash
docker logs -f data-collector
```

## 🔍 Monitoramento

### Logs

O coletor standalone gera logs em:

- **Console:** `stdout`
- **Arquivo:** `data_collector.log`

Formato:

```
2024-12-09 15:30:00 - INFO - === Iniciando job de coleta de dados de ações ===
2024-12-09 15:30:01 - INFO - Buscando dados para AAPL (period=1d, interval=1m)
2024-12-09 15:30:03 - INFO - Coletados 390 registros para AAPL
2024-12-09 15:30:04 - INFO - ✓ AAPL: 320 salvos, 70 duplicados
2024-12-09 15:30:04 - INFO - === Job finalizado: 1/1 tickers bem-sucedidos ===
```

### Healthcheck

A API possui healthcheck em `/health`:

```bash
curl http://localhost:3333/health
```

## 🛠️ Troubleshooting

### Problema: "Nenhum dado encontrado"

**Solução:**

- Verifique se o ticker está correto
- Mercado pode estar fechado (use `period=5d` e `interval=1d` para dados históricos)
- Verifique conexão com internet

### Problema: Muitos duplicados

**Solução:**

- Aumentar `STOCK_DATA_INTERVAL` (ex: de `1m` para `5m`)
- Aumentar `STOCK_COLLECTION_INTERVAL_MINUTES`
- Dados duplicados são automaticamente ignorados

### Problema: Erro de conexão ao banco

**Solução:**

- Verifique se o serviço `db` está rodando: `docker ps`
- Verifique `DATABASE_URL` no `.env`
- Aguarde o healthcheck do banco: `docker-compose logs db`

### Problema: Rate limiting do yFinance

**Solução:**

- Aumentar intervalo entre coletas
- Reduzir número de tickers
- Usar `period` e `interval` maiores

## 📊 Estrutura do Banco de Dados

Tabela `history`:

| Coluna         | Tipo     | Descrição            |
| -------------- | -------- | -------------------- |
| `id`           | Integer  | ID único (PK)        |
| `ticker_name`  | String   | Símbolo da ação      |
| `date`         | DateTime | Data/hora do dado    |
| `open`         | Float    | Preço de abertura    |
| `high`         | Float    | Preço máximo         |
| `low`          | Float    | Preço mínimo         |
| `close`        | Float    | Preço de fechamento  |
| `volume`       | Integer  | Volume negociado     |
| `dividends`    | Float    | Dividendos           |
| `stock_splits` | Float    | Desdobramento        |
| `created_at`   | DateTime | Timestamp de criação |

**Índices:**

- `idx_ticker_date` em (`ticker_name`, `date`) para queries rápidas
- Constraint UNIQUE em (`ticker_name`, `date`) para evitar duplicados

## 🔒 Segurança

- Logs não expõem dados sensíveis
- Banco de dados protegido por senha
- Containers isolados em rede bridge

## 📝 Exemplo Completo

```bash
# 1. Configure o .env
cat > .env << EOF
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mypass
POSTGRES_DB=riskvision
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://postgres:mypass@db:5432/riskvision

STOCK_TICKERS=AAPL,MSFT,GOOGL
STOCK_COLLECTION_INTERVAL_MINUTES=5
STOCK_COLLECTION_PERIOD=1d
STOCK_DATA_INTERVAL=1m
ENABLE_STOCK_SCHEDULER=false
EOF

# 2. Inicie o ambiente completo
docker-compose -f docker-compose.dev.yml --profile with-collector up -d

# 3. Verifique os logs
docker logs -f data-collector

# 4. Teste a API
curl http://localhost:3333/scheduler/status
curl http://localhost:3333/stocks/apple
curl http://localhost:3333/history/?period=day

# 5. Pare os serviços
docker-compose -f docker-compose.dev.yml down
```

## 🎯 Próximos Passos

- [ ] Adicionar mais tickers conforme necessário
- [ ] Ajustar intervalos de coleta baseado no uso
- [ ] Monitorar volume de dados no banco
- [ ] Configurar alertas para falhas na coleta
- [ ] Implementar cleanup de dados antigos (opcional)
