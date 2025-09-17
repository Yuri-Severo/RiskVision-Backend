from fastapi import FastAPI
from database import Base, engine
from routers import userRouter, roleRouter, historyRouter

# Criar tabelas (em dev, usar Alembic em prod)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Minha API", version="2.0.0")

# Routers
app.include_router(userRouter.router)
app.include_router(roleRouter.router)
app.include_router(historyRouter.router)

@app.get("/")
def read_root():
    return {"message": "API funcionando 🚀"}
