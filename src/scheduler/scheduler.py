import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.executors.pool import ThreadPoolExecutor
from config.settings import settings
from scheduler.jobs import collect_stock_data_job

logger = logging.getLogger(__name__)

# Instância global do scheduler
_scheduler: BackgroundScheduler = None


def get_scheduler() -> BackgroundScheduler:
    """Retorna a instância do scheduler (singleton)"""
    global _scheduler

    if _scheduler is None:
        _scheduler = BackgroundScheduler(
            executors={"default": ThreadPoolExecutor(max_workers=2)},
            job_defaults={
                "coalesce": True,  # Agrupa execuções perdidas
                "max_instances": 1,  # Apenas uma instância do job por vez
            },
        )

    return _scheduler


def start_scheduler():
    """Inicia o scheduler e adiciona os jobs"""
    if not settings.ENABLE_STOCK_SCHEDULER:
        logger.info("Scheduler desabilitado (ENABLE_STOCK_SCHEDULER=false)")
        return

    scheduler = get_scheduler()

    # Verificar se já está rodando
    if scheduler.running:
        logger.warning("Scheduler já está rodando")
        return

    # Adicionar job de coleta de dados
    interval_minutes = settings.STOCK_COLLECTION_INTERVAL_MINUTES

    scheduler.add_job(
        func=collect_stock_data_job,
        trigger=IntervalTrigger(minutes=interval_minutes),
        id="collect_stock_data",
        name="Coletar dados de ações do yFinance",
        replace_existing=True,
    )

    # Iniciar scheduler
    scheduler.start()

    logger.info(
        f"✓ Scheduler iniciado com sucesso! "
        f"Coleta a cada {interval_minutes} minuto(s) para: {settings.STOCK_TICKERS}"
    )

    # Executar job imediatamente na primeira vez (opcional)
    # collect_stock_data_job()


def stop_scheduler():
    """Para o scheduler de forma graciosa"""
    scheduler = get_scheduler()

    if scheduler.running:
        logger.info("Parando scheduler...")
        scheduler.shutdown(wait=True)
        logger.info("✓ Scheduler parado com sucesso")
    else:
        logger.warning("Scheduler não está rodando")


def get_scheduler_status() -> dict:
    """Retorna o status do scheduler e seus jobs"""
    scheduler = get_scheduler()

    if not scheduler.running:
        return {"running": False, "jobs": []}

    jobs_info = []
    for job in scheduler.get_jobs():
        jobs_info.append(
            {
                "id": job.id,
                "name": job.name,
                "next_run": str(job.next_run_time) if job.next_run_time else None,
                "trigger": str(job.trigger),
            }
        )

    return {
        "running": True,
        "jobs": jobs_info,
        "enabled": settings.ENABLE_STOCK_SCHEDULER,
        "interval_minutes": settings.STOCK_COLLECTION_INTERVAL_MINUTES,
        "tickers": settings.get_tickers_list(),
    }
