import os
from fastapi import FastAPI
from database import Base, engine
from routers import userRouter, roleRouter, historyRouter, authRouter

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Riskvision", version="1.0.0")

# Routers
app.include_router(authRouter.router)
app.include_router(userRouter.router)
app.include_router(roleRouter.router)
app.include_router(historyRouter.router)


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "API funcionando com JWT 🚀"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "3333")),
        reload=False
    )