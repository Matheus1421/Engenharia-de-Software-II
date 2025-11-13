from fastapi import FastAPI
from fastapi.responses import JSONResponse

from routers.ciclista import router as ciclista_router
from routers.funcionario import router as funcionario_router
from routers.cartao import router as cartao_router
from routers.aluguel import router as aluguel_router
from routers.admin import router as admin_router

from database.database import get_db
from database.init_data import init_db


app = FastAPI(
    title="Serviço de Aluguel",
    version="0.1.0",
    description="Aluguel do Sistema de Controle de Bicicletário.",
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.on_event("startup")
def startup_event():
    db = get_db()
    ciclistas_table = db.table('ciclistas')

    if len(ciclistas_table.all()) == 0:
        init_db(db)
        print("✓ Banco de dados inicializado com dados padrão")
        print("  - Acesse http://localhost:8001/docs para ver a documentação")
        print("  - Use GET /funcionario para ver funcionários de exemplo")
    else:
        print("✓ Banco de dados já contém dados")

# Registro dos routers
app.include_router(ciclista_router)
app.include_router(funcionario_router)
app.include_router(cartao_router)
app.include_router(aluguel_router)
app.include_router(admin_router)

@app.get("/", tags=["Health"])
def root():
    """Endpoint para verificar se o serviço está funcionando"""
    return {
        "message": "Microsserviço de Aluguel",
        "status": "online",
        "version": "0.1.0",
        "docs": "http://localhost:8001/docs"
    }

@app.get("/health", tags=["Health"])
@app.get("/status", tags=["Health"])
def health():
    """Health check para monitoramento"""
    return {"status": "ok"}

# Execução do servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )
