# RiskVision-Backend

## Descrição

**RiskVision** é um sistema de análise de mercado financeiro que utiliza **Inteligência Artificial (IA)** para processar notícias financeiras e gerar insights para investidores e analistas. O sistema classifica o sentimento (positivo, negativo ou neutro) e avalia o nível de risco (alto, médio ou baixo) das notícias, fornecendo atualizações em tempo real por meio de uma **API** e de um **dashboard interativo**.

## 📊 RiskVision Dashboard

Este projeto agora inclui um **dashboard interativo em Streamlit** para visualização de previsões de preços!

### Acesso Rápido
- **Dashboard:** http://localhost:8501
- **API:** http://localhost:8000
- **Documentação do Dashboard:** [riskvision-frontend/README.md](riskvision-frontend/README.md)

### Executar com Docker Compose
```bash
docker-compose up -d
```

Veja a [documentação completa do dashboard](riskvision-frontend/) para mais informações.

---

### Objetivos do projeto:

1. **Coletar e processar notícias** em tempo real.
2. **Classificar sentimentos** (positivo/negativo/neutro) e avaliar riscos.
3. **Entregar insights** para o investidor/analista.
4. **Reduzir o tempo de análise** e aumentar a precisão das decisões.
5. **Visualizar o impacto** das notícias no mercado financeiro.

O sistema visa resolver o problema de **sobrecarga de informações** no mercado financeiro, permitindo que investidores e analistas avaliem rapidamente o impacto das notícias financeiras.

---

## Previsão Online com River (AAPL apenas)

### 🚀 Nova Feature: Previsão de Preços em Tempo Real

Este sistema agora inclui um serviço de **previsão de preços em tempo real** usando **Online Machine Learning** com a biblioteca **River** e dados da **Apple (AAPL)** obtidos via **yfinance**.

#### ⚠️ Limitações Importantes

- **Ticker fixo**: O sistema opera **exclusivamente com a ação da Apple (AAPL)**. Não há suporte para outros tickers nesta versão.
- **Estado em memória**: O modelo é mantido em memória e não persiste em banco de dados. Recomenda-se executar com `--workers 1` para consistência.
- **Não constitui recomendação de investimento**: Este sistema é apenas para fins educacionais e de demonstração. Não deve ser usado como base para decisões de investimento.

#### 📊 Funcionalidades

1. **Modelo Incremental (SNARIMAX)**: Utiliza River para aprendizado online, atualizando-se continuamente com novos dados.
2. **Dados em Tempo Real**: Integração com yfinance para obter cotações atualizadas.
3. **Warm-start Automático**: O modelo é inicializado automaticamente com dados históricos na primeira requisição.
4. **Atualização em Background**: Poller opcional que busca novos preços periodicamente e atualiza o modelo.
5. **API RESTful**: Endpoints para obter previsões, forçar retreinamento e verificar status do modelo.

#### 🔧 Variáveis de Ambiente

Adicione as seguintes variáveis ao seu arquivo `.env`:

```ini
# Configuração de dados do yfinance
YF_PERIOD=7d              # Período histórico (max 7d para interval=1m)
YF_INTERVAL=1m            # Intervalo dos dados (1m, 5m, 1h, 1d, etc.)

# Configuração do poller de background
POLL_ENABLED=true         # Habilita atualização automática
POLL_EVERY_SECONDS=60     # Intervalo entre atualizações (segundos)

# Configuração de throttling
THROTTLE_SECONDS=1.0      # Delay entre chamadas à API do yfinance

# Configuração do modelo
DEFAULT_FORECAST_HORIZON=1  # Horizonte padrão de previsão
```

#### 📡 Endpoints da API

##### 1. Obter Previsão
```bash
GET /forecast?horizon=5
```

Retorna previsões de preço para AAPL.

**Parâmetros:**
- `horizon` (opcional): Número de períodos à frente para prever (padrão: 1, máximo: 100)
- `aapl_only` (opcional): Parâmetro de reconhecimento (ignorado, sempre AAPL)

**Exemplo de resposta:**
```json
{
  "ticker": "AAPL",
  "horizon": 5,
  "last_price": 178.50,
  "forecast": [178.55, 178.60, 178.65, 178.70, 178.75],
  "as_of": "2024-12-10T10:30:00.123456"
}
```

**Exemplo de uso:**
```bash
curl 'http://localhost:8000/forecast?horizon=5'
```

##### 2. Forçar Treinamento
```bash
POST /forecast/train
```

Força o modelo a recarregar dados históricos e retreinar do zero.

**Exemplo de resposta:**
```json
{
  "status": "success",
  "message": "Model warm-started with 420 samples",
  "ticker": "AAPL",
  "samples": 420,
  "last_price": 178.50
}
```

**Exemplo de uso:**
```bash
curl -X POST 'http://localhost:8000/forecast/train'
```

##### 3. Verificar Status do Modelo
```bash
GET /forecast/health
```

Retorna o status atual do modelo de previsão.

**Exemplo de resposta:**
```json
{
  "ticker": "AAPL",
  "model_initialized": true,
  "samples_trained": 420,
  "last_price": 178.50,
  "last_timestamp": "2024-12-10T10:30:00.123456",
  "ready_for_forecast": true
}
```

**Exemplo de uso:**
```bash
curl 'http://localhost:8000/forecast/health'
```

#### 🚦 Como Executar com Previsão

**Importante**: Execute com apenas **1 worker** para manter o estado do modelo consistente:

```bash
# Instalação de dependências
pip install -r requirements.txt

# Executar em modo desenvolvimento
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 1 --reload

# Executar em produção
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 1
```

#### 🧪 Executar Testes

```bash
# Executar todos os testes
pytest tests/ -v

# Executar apenas testes do serviço de previsão
pytest tests/test_river_service.py -v
```

#### 📝 Notas Técnicas

- **Intervalo de 1 minuto**: O yfinance limita dados de 1 minuto a um período máximo de 7 dias.
- **Retry automático**: O cliente yfinance implementa retry exponencial (3 tentativas) em caso de falhas.
- **Throttling**: Há um delay configurável entre chamadas sucessivas à API do yfinance para evitar rate limiting.
- **Modelo SNARIMAX**: Modelo de séries temporais com componentes autorregressivos, diferenciação e média móvel, incluindo sazonalidade.

#### ⚠️ Aviso Legal

**Este sistema é fornecido apenas para fins educacionais e de demonstração. As previsões geradas não constituem recomendação de investimento. Investimentos em ações envolvem riscos, incluindo a perda do capital investido. Sempre consulte um profissional financeiro qualificado antes de tomar decisões de investimento.**

---

## Repositórios

O projeto **RiskVision** é dividido em três repositórios:

* [**Frontend-RiskVision**](https://github.com/Edgar-Klewert/Frontend-RiskVision) - Frontend do sistema, construído com **Next.js**.
* [**RiskVision-Backend**](https://github.com/Yuri-Severo/RiskVision-Backend) - Backend do sistema, construído com **FastAPI**, processando os dados e servindo a **API**.
* [**Relatorio-Dados-RiskVision**](https://github.com/Edgar-Klewert/Relatorio-Dados-RiskVision) - Repositório para análise de dados e relatórios do projeto.

---

## Dependências (Backend)

O serviço **RiskVision-Backend** utiliza as seguintes dependências:

* **FastAPI**: Framework moderno para construir APIs em Python.
* **Uvicorn**: Servidor **ASGI** para rodar a aplicação **FastAPI**.
* **SQLAlchemy**: ORM para interações com o banco de dados PostgreSQL.
* **psycopg2-binary**: Adaptador do PostgreSQL para Python.
* **Passlib**: Biblioteca para hash de senhas.
* **python-jose**: Para criação e validação de **tokens JWT**.
* **Pydantic**: Validação de dados e gerenciamento de configurações.
* **python-dotenv**: Para carregar variáveis de ambiente a partir de arquivos `.env`.

Para instalar todas as dependências, execute:

```bash
pip install -r requirements.txt
```

---

## Instruções de Configuração

### Pré-requisitos:

1. **Docker**: O Docker deve estar instalado para containerizar e rodar os serviços.
2. **Docker Compose**: O Docker Compose é utilizado para gerenciar os containers dos serviços.

### Passo a Passo para Execução

1. **Clone os repositórios**:

   Você precisará clonar os três repositórios para rodar o projeto completo:

   ```bash
   git clone https://github.com/Edgar-Klewert/Frontend-RiskVision
   git clone https://github.com/Yuri-Severo/RiskVision-Backend
   git clone https://github.com/Edgar-Klewert/Relatorio-Dados-RiskVision
   ```

   Certifique-se de que todos os projetos estejam dentro da mesma pasta.

2. **Configuração do arquivo `.env` do Backend**:

   Na raiz do projeto **RiskVision-Backend**, crie um arquivo `.env` usando o arquivo de exemplo `.env.example`:

   ```bash
   cp .env.example .env
   ```

   Edite o arquivo `.env` com os valores adequados. Certifique-se de **não expor informações sensíveis**.

   Exemplo do arquivo `.env`:

   ```
   DATABASE_URL=postgresql://<usuario>:<senha>@<host>:<porta>/<nome_banco>
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_USER=seu_usuario
   POSTGRES_PASSWORD=sua_senha
   POSTGRES_DB=nome_banco
   FRONTEND_URL=http://localhost:3000
   JWT_SECRET=seu_segredo
   ```

3. **Configuração do arquivo `.env` do Frontend**:

   Da mesma forma, no diretório **Frontend-RiskVision**, crie o arquivo `.env` a partir do arquivo `.env.example`:

   ```bash
   cp .env.example .env
   ```

   Edite o arquivo `.env` com os valores adequados:

   Exemplo do arquivo `.env`:

   ```
   NODE_ENV=development
   API_URL=http://localhost:3333
   NEXT_PUBLIC_API_URL=http://localhost:3333
   JWT_SECRET=seu_segredo
   ```

   **Importante**: As variáveis de ambiente do frontend devem ser configuradas de acordo com as necessidades do projeto, principalmente para garantir que o frontend consiga se comunicar corretamente com a API do backend.

4. **Ajustando o contexto no Docker Compose**:

   Para garantir que todos os repositórios se integrem corretamente, ajuste o contexto nos arquivos `docker-compose.yml` e `docker-compose.dev.yml`.

   Exemplo:

   ```yaml
   frontend:
     container_name: riskvision-web
     build:
       context: ../Frontend-RiskVision  # O repositório frontend deve estar na mesma pasta que o backend
       dockerfile: Dockerfile
     restart: always
     ports:
       - "3000:3000"
     depends_on:
       backend:
         condition: service_healthy
   ```

5. **Executando em Desenvolvimento**:

   No diretório **RiskVision-Backend**, execute o seguinte comando para iniciar os containers em modo de desenvolvimento:

   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```

   Isso irá rodar os containers para **backend**, **frontend**, e o banco **PostgreSQL** no modo de desenvolvimento.

   Verifique se todos os containers estão funcionando corretamente:

   * O **backend** estará disponível em `http://localhost:3333`.
   * O **frontend** estará disponível em `http://localhost:3000`.

6. **Executando em Produção**:

   Para rodar o projeto em produção, use o seguinte comando no diretório **RiskVision-Backend**:

   ```bash
   docker-compose up --build
   ```

   Isso irá iniciar os containers para **backend**, **frontend**, e o banco **PostgreSQL** com configurações adequadas para produção.

---

## Arquivo `.env.example`

Este é um exemplo do arquivo `.env` usado para configurar as variáveis de ambiente para o backend:

```ini
DATABASE_URL=postgresql://<usuario>:<senha>@<host>:<porta>/<nome_banco>
POSTGRES_HOST=<host_banco>
POSTGRES_PORT=<porta_banco>
POSTGRES_USER=<usuario_banco>
POSTGRES_PASSWORD=<senha_banco>
POSTGRES_DB=<nome_banco>
FRONTEND_URL=<url_frontend>
JWT_SECRET=<seu_segredo>
```

---

## Comandos Úteis

* **Construindo os containers**:

  ```bash
  docker-compose build
  ```

* **Iniciando os containers em desenvolvimento**:

  ```bash
  docker-compose -f docker-compose.dev.yml up --build
  ```

* **Iniciando os containers em produção**:

  ```bash
  docker-compose up --build
  ```

* **Parando os containers**:

  ```bash
  docker-compose down
  ```

* **Visualizando os logs**:

  ```bash
  docker logs <nome_do_container>
  ```

---

## Contribuindo

Sinta-se à vontade para fazer um fork deste repositório e contribuir com melhorias. Para qualquer alteração, por favor, crie um **pull request**.

