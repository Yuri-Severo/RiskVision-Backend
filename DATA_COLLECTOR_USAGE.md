# 📊 Guia de Uso do Coletor de Dados

## Como Funcionar o Profile do Docker Compose

### Serviços que sempre iniciam:

- `db` (PostgreSQL)
- `backend` (API FastAPI)

### Serviço opcional (com profile):

- `data-collector` (coletor de dados de ações)

## Comandos

### 1. Iniciar SEM o coletor de dados (apenas API)

```bash
docker compose -f docker-compose.dev.yml up
```

### 2. Iniciar COM o coletor de dados

```bash
docker compose -f docker-compose.dev.yml --profile with-collector up
```

## Comportamento do Coletor

Por padrão, o coletor **NÃO SALVA** os dados no banco de dados. Ele apenas **exibe no console**.

### Para APENAS EXIBIR no console (padrão):

No arquivo `.env`:

```env
SAVE_TO_DATABASE=false
```

### Para SALVAR no banco de dados:

No arquivo `.env`:

```env
SAVE_TO_DATABASE=true
```

## Exemplo de Output (modo console)

```
================================================================================
📊 DADOS COLETADOS PARA AAPL
================================================================================

[1/390] 2024-12-09 09:30:00-05:00
  Open:   $195.50
  High:   $196.20
  Low:    $195.30
  Close:  $195.80
  Volume: 2,543,210

[2/390] 2024-12-09 09:31:00-05:00
  Open:   $195.80
  High:   $196.10
  Low:    $195.75
  Close:  $196.00
  Volume: 1,234,567

...

================================================================================
✓ Total de 390 registros exibidos para AAPL
================================================================================
```

## Configurações do Coletor (.env)

```env
# Tickers para coletar (separados por vírgula)
STOCK_TICKERS=AAPL,MSFT,GOOGL

# Intervalo entre coletas (em minutos)
STOCK_COLLECTION_INTERVAL_MINUTES=5

# Período de dados (1d, 5d, 1mo, etc)
STOCK_COLLECTION_PERIOD=1d

# Intervalo dos dados (1m, 5m, 1h, etc)
STOCK_DATA_INTERVAL=1m

# Máximo de tentativas em caso de erro
MAX_RETRY_ATTEMPTS=3

# Delay entre tentativas (segundos)
RETRY_DELAY_SECONDS=5

# Salvar no banco? (true/false)
SAVE_TO_DATABASE=false
```

## Fluxo Completo

1. **Configurar variáveis** no `.env`
2. **Escolher modo** (salvar ou apenas exibir)
3. **Executar com profile**:
   ```bash
   docker compose -f docker-compose.dev.yml --profile with-collector up
   ```
4. **Ver logs** no console
5. **Parar** com `Ctrl+C` ou `docker compose down`

## Verificar Logs do Coletor

```bash
# Ver logs em tempo real
docker logs -f data-collector

# Ver últimas 100 linhas
docker logs --tail 100 data-collector
```
