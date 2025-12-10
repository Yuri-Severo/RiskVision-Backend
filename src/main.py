from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import Base, engine
from routers import userRouter, roleRouter, historyRouter, authRouter, registerRouter
from api.routes import forecast
from background.poller import get_poller


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    poller = get_poller()
    await poller.start()
    
    yield
    
    # Shutdown
    await poller.stop()


# Criar tabelas (se o banco estiver disponível)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    import sys
    print(f"⚠️  Warning: Could not create database tables: {e}", file=sys.stderr)
    print("   Forecasting service will still work without database.", file=sys.stderr)

app = FastAPI(title="Riskvision", version="1.0.0", lifespan=lifespan)

# Routers
app.include_router(authRouter.router)
app.include_router(userRouter.router)
app.include_router(roleRouter.router)
app.include_router(registerRouter.router)
app.include_router(historyRouter.router)
app.include_router(forecast.router)


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "API funcionando com JWT 🚀"}