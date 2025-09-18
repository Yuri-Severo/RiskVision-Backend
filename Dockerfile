# syntax=docker/dockerfile:1.7
FROM python:3.12-slim AS base

# Evita buffer no stdout/stderr e .pyc no container
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Dependências de sistema (ex.: psycopg2, healthchecks com curl)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala dependências de Python com cache
# (coloque seu requirements.txt na raiz do repo)
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Copia o código (ajuste conforme sua estrutura)
COPY src ./src

# Usuário não-root por segurança
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Porta exposta pela API
EXPOSE 3333

# Comando padrão (o docker-compose sobrescreve com `command`)
CMD ["python", "src/main.py"]
