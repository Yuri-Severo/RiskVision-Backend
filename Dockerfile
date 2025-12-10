# syntax=docker/dockerfile:1.7
FROM python:3.12-slim

# Variáveis de ambiente para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONIOENCODING=utf-8 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Criar diretório de trabalho
WORKDIR /app

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código fonte
COPY src/ ./src/
COPY scripts/ ./scripts/

# Criar usuário não-root
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Healthcheck interno
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:3333/health || exit 1

# Expor porta
EXPOSE 3333

# Comando para iniciar a aplicação
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3333", "--app-dir", "src", "--access-log"]