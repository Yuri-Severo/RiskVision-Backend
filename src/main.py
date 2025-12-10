from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import Base, engine
from routers import (
    userRouter,
    roleRouter,
    historyRouter,
    authRouter,
    registerRouter,
    stockRouter,
)
from scheduler.scheduler import start_scheduler, stop_scheduler, get_scheduler_status
from config.settings import settings
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    # Startup
    logger.info("Iniciando aplicação RiskVision...")

    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    logger.info("✓ Tabelas do banco de dados verificadas")

    # Iniciar scheduler se habilitado
    if settings.ENABLE_STOCK_SCHEDULER:
        start_scheduler()
    else:
        logger.info("Scheduler de coleta de dados desabilitado")

    yield

    # Shutdown
    logger.info("Finalizando aplicação...")
    stop_scheduler()
    logger.info("✓ Aplicação finalizada com sucesso")


app = FastAPI(title="Riskvision", version="1.0.0", lifespan=lifespan)

# Routers
app.include_router(authRouter.router)
app.include_router(userRouter.router)
app.include_router(roleRouter.router)
app.include_router(registerRouter.router)
app.include_router(historyRouter.router)
app.include_router(stockRouter.router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def read_root():
    return {"message": "API funcionando com JWT 🚀"}


@app.get("/scheduler/status")
def scheduler_status():
    """Retorna o status do scheduler de coleta de dados"""
    return get_scheduler_status()
