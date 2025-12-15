from fastapi import FastAPI
from dotenv import load_dotenv
from routers.status import router as status_router
from routers.admin import router as admin_router
from routers.email import contrato_router as email_contrato_router
from routers.cobranca import contrato_router as cobranca_contrato_router
from routers.cartao import contrato_router as cartao_contrato_router
from database.database import get_db
from database.init_data import init_db

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

app = FastAPI(
    title="Serviço Externo",
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
    emails_table = db.get_table('emails')
    if len(emails_table.all()) == 0:
        init_db(db)
        print("✓ Banco de dados inicializado com dados padrão")

# Registra o endpoint de status
app.include_router(status_router)
# Registra o endpoint de admin
app.include_router(admin_router)
# Endpoints do contrato externo
app.include_router(email_contrato_router)          # /enviarEmail
app.include_router(cobranca_contrato_router)       # /filaCobranca, /processaCobrancasEmFila
app.include_router(cartao_contrato_router)         # /validaCartaoDeCredito


# Health-check simples (opcional)
@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

