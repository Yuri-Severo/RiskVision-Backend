#!/bin/bash

# Script de inicialização rápida do RiskVision Dashboard
# 
# Uso: ./start.sh [opção]
# Opções:
#   local    - Executa localmente com Python
#   docker   - Executa com Docker
#   compose  - Executa com Docker Compose (stack completa)

set -e

OPTION=${1:-local}

echo "🚀 Iniciando RiskVision Dashboard..."
echo ""

case $OPTION in
  local)
    echo "📦 Modo: Execução Local"
    echo ""
    
    # Verifica se o ambiente virtual existe
    if [ ! -d "venv" ]; then
      echo "🔧 Criando ambiente virtual..."
      python -m venv venv
    fi
    
    # Ativa ambiente virtual
    echo "🔌 Ativando ambiente virtual..."
    source venv/bin/activate
    
    # Instala dependências
    echo "📚 Instalando dependências..."
    pip install -q -r requirements.txt
    
    # Copia .env se não existir
    if [ ! -f ".env" ]; then
      echo "⚙️  Criando arquivo .env..."
      cp .env.example .env
      echo "⚠️  Não esqueça de configurar as variáveis em .env"
    fi
    
    echo ""
    echo "✅ Setup completo!"
    echo ""
    echo "📊 Iniciando dashboard em http://localhost:8501"
    echo "🔐 Use as credenciais da API para fazer login"
    echo ""
    echo "Pressione Ctrl+C para parar"
    echo ""
    
    # Inicia Streamlit
    streamlit run app.py
    ;;
    
  docker)
    echo "🐳 Modo: Docker"
    echo ""
    
    # Build da imagem
    echo "🔨 Construindo imagem Docker..."
    docker build -t riskvision-dashboard .
    
    # Para container anterior se existir
    if [ "$(docker ps -aq -f name=riskvision-dashboard)" ]; then
      echo "🛑 Parando container anterior..."
      docker stop riskvision-dashboard
      docker rm riskvision-dashboard
    fi
    
    # Executa container
    echo "🚀 Iniciando container..."
    docker run -d \
      --name riskvision-dashboard \
      -p 8501:8501 \
      -e API_URL=http://host.docker.internal:8000 \
      riskvision-dashboard
    
    echo ""
    echo "✅ Dashboard iniciado!"
    echo "📊 Acesse: http://localhost:8501"
    echo ""
    echo "Comandos úteis:"
    echo "  docker logs -f riskvision-dashboard    # Ver logs"
    echo "  docker stop riskvision-dashboard       # Parar"
    echo "  docker start riskvision-dashboard      # Iniciar"
    echo ""
    ;;
    
  compose)
    echo "🐳 Modo: Docker Compose (Stack Completa)"
    echo ""
    
    cd ..
    
    echo "🔨 Construindo serviços..."
    docker-compose build frontend
    
    echo "🚀 Iniciando stack..."
    docker-compose up -d
    
    echo ""
    echo "✅ Stack completa iniciada!"
    echo ""
    echo "📊 Dashboard: http://localhost:8501"
    echo "🔌 API: http://localhost:8000"
    echo "📋 API Docs: http://localhost:8000/docs"
    echo "🐳 Portainer: http://localhost:9000"
    echo ""
    echo "Comandos úteis:"
    echo "  docker-compose logs -f frontend    # Logs do dashboard"
    echo "  docker-compose ps                  # Status dos serviços"
    echo "  docker-compose stop                # Parar tudo"
    echo "  docker-compose down                # Parar e remover"
    echo ""
    ;;
    
  *)
    echo "❌ Opção inválida: $OPTION"
    echo ""
    echo "Uso: ./start.sh [opção]"
    echo ""
    echo "Opções disponíveis:"
    echo "  local    - Executa localmente com Python"
    echo "  docker   - Executa com Docker"
    echo "  compose  - Executa com Docker Compose (stack completa)"
    echo ""
    exit 1
    ;;
esac
