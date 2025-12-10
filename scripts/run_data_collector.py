#!/usr/bin/env python3
"""
Script standalone para executar o coletor de dados de ações.
Este script pode ser executado independentemente da API FastAPI.

Uso:
    python scripts/run_data_collector.py

O script executará indefinidamente, coletando dados nos intervalos configurados,
até que seja interrompido (Ctrl+C ou SIGTERM).
"""

import sys
import os
import logging
import signal
import time
from pathlib import Path

# Adicionar o diretório src ao path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from config.settings import settings
from scheduler.jobs import collect_stock_data_job

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("data_collector.log"),
    ],
)
logger = logging.getLogger(__name__)

# Variável global para controlar shutdown
shutdown_requested = False


def signal_handler(signum, frame):
    """Handler para sinais de interrupção (SIGTERM, SIGINT)"""
    global shutdown_requested
    signal_name = signal.Signals(signum).name
    logger.info(f"Recebido sinal {signal_name}. Iniciando shutdown gracioso...")
    shutdown_requested = True


def validate_configuration():
    """Valida as configurações antes de iniciar"""
    logger.info("Validando configurações...")

    validations = settings.validate_settings()

    if not validations["database_configured"]:
        logger.error(
            "❌ Banco de dados não configurado! Verifique DATABASE_URL ou POSTGRES_*"
        )
        return False

    if not validations["tickers_configured"]:
        logger.error("❌ Nenhum ticker configurado! Defina STOCK_TICKERS")
        return False

    if not validations["collection_interval_valid"]:
        logger.error(
            "❌ Intervalo de coleta inválido! STOCK_COLLECTION_INTERVAL_MINUTES deve ser > 0"
        )
        return False

    logger.info("✓ Configurações válidas")
    return True


def main():
    """Função principal do coletor de dados"""
    logger.info("=" * 60)
    logger.info("INICIANDO COLETOR DE DADOS DE AÇÕES - RISKVISION")
    logger.info("=" * 60)

    # Ler configuração de salvar no banco (padrão: false = apenas exibir)
    save_to_db = os.getenv("SAVE_TO_DATABASE", "false").lower() in ("true", "1", "yes")
    mode_msg = "SALVAR NO BANCO" if save_to_db else "APENAS EXIBIR NO CONSOLE"
    logger.info(f"Modo de operação: {mode_msg}")

    # Registrar handlers de sinal
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Validar configuração
    if not validate_configuration():
        logger.error("Falha na validação de configurações. Abortando.")
        sys.exit(1)

    # Mostrar configurações
    tickers = settings.get_tickers_list()
    interval = settings.STOCK_COLLECTION_INTERVAL_MINUTES
    period = settings.STOCK_COLLECTION_PERIOD
    data_interval = settings.STOCK_DATA_INTERVAL

    logger.info(f"Tickers configurados: {', '.join(tickers)}")
    logger.info(f"Intervalo de coleta: {interval} minuto(s)")
    logger.info(f"Período de dados: {period}")
    logger.info(f"Intervalo de dados: {data_interval}")
    logger.info(f"Máximo de tentativas: {settings.MAX_RETRY_ATTEMPTS}")
    logger.info("=" * 60)

    # Criar scheduler bloqueante
    scheduler = BlockingScheduler(job_defaults={"coalesce": True, "max_instances": 1})

    # Adicionar job
    scheduler.add_job(
        func=lambda: collect_stock_data_job(save_to_db=save_to_db),
        trigger=IntervalTrigger(minutes=interval),
        id="collect_stock_data",
        name=f"Coletar dados de ações do yFinance ({mode_msg})",
        replace_existing=True,
    )

    logger.info(f"✓ Scheduler configurado (modo: {mode_msg})")

    # Executar coleta imediatamente na primeira vez
    logger.info("Executando primeira coleta imediatamente...")
    try:
        collect_stock_data_job(save_to_db=save_to_db)
    except Exception as e:
        logger.error(f"Erro na primeira coleta: {e}", exc_info=True)

    # Iniciar scheduler
    try:
        logger.info("Iniciando scheduler... (Pressione Ctrl+C para parar)")
        logger.info(f"Próxima coleta em {interval} minuto(s)")
        scheduler.start()

    except (KeyboardInterrupt, SystemExit):
        logger.info("Interrupção recebida. Finalizando...")

    finally:
        # Shutdown gracioso
        logger.info("Parando scheduler...")
        scheduler.shutdown(wait=True)
        logger.info("✓ Coletor de dados finalizado com sucesso")
        logger.info("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Erro crítico não tratado: {e}", exc_info=True)
        sys.exit(1)
