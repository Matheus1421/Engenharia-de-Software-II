from fastapi import FastAPI
from routers.status import router as status_router

app = FastAPI(
    title="Serviço de Equipamentos",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Registra o endpoint de status
app.include_router(status_router)

# Health-check simples (opcional)
@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)