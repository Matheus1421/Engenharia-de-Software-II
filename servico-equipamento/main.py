from fastapi import FastAPI
from routers.status import router as status_router
from routers.admin import router as admin_router
from routers.bicicleta import router as bicicleta_router
from routers.totem import router as totem_router
from routers.tranca import router as tranca_router
from database.database import get_db
from database.init_data import init_db

app = FastAPI(
    title="Serviço de Equipamentos",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Inicializa o banco de dados na primeira execução
@app.on_event("startup")
def startup_event():
    """Inicializa o banco de dados com dados padrão se estiver vazio"""
    db = get_db()
    # Verifica se o banco está vazio
    bicicletas_table = db.get_table('bicicletas')
    if len(bicicletas_table.all()) == 0:
        init_db(db)
        print("✓ Banco de dados inicializado com dados padrão")

# Registra o endpoint de status
app.include_router(status_router)
# Registra o endpoint de admin
app.include_router(admin_router)
# Registra os endpoints de bicicletas
app.include_router(bicicleta_router)
# Registra os endpoints de totems
app.include_router(totem_router)
# Registra os endpoints de trancas
app.include_router(tranca_router)

# Health-check simples (opcional)
@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)