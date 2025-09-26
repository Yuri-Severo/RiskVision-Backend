# RiskVision-Backend

## Descrição

**RiskVision** é um sistema de análise de mercado financeiro que utiliza **Inteligência Artificial (IA)** para processar notícias financeiras e gerar insights para investidores e analistas. O sistema classifica o sentimento (positivo, negativo ou neutro) e avalia o nível de risco (alto, médio ou baixo) das notícias, fornecendo atualizações em tempo real por meio de uma **API** e de um **dashboard interativo**.

### Objetivos do projeto:

1. **Coletar e processar notícias** em tempo real.
2. **Classificar sentimentos** (positivo/negativo/neutro) e avaliar riscos.
3. **Entregar insights** para o investidor/analista.
4. **Reduzir o tempo de análise** e aumentar a precisão das decisões.
5. **Visualizar o impacto** das notícias no mercado financeiro.

O sistema visa resolver o problema de **sobrecarga de informações** no mercado financeiro, permitindo que investidores e analistas avaliem rapidamente o impacto das notícias financeiras.

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

---