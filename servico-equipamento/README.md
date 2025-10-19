# Serviço de Equipamentos (SCB)

Microsserviço responsável por bicicletas, totens e trancas no Sistema de Controle de Bicicletário (SCB).

## Arquitetura
- `models/`: esquemas Pydantic (ex.: `models/status_model.py`)
- `services/`: regras de negócio (ex.: `services/equipamento_service.py`)
- `routers/`: endpoints FastAPI (ex.: `routers/status.py`)
- `main.py`: instancia o app e registra os routers

Endpoint inicial (alô mundo): `GET /status/`

## Rodando localmente (Poetry)
1. Instale dependências
	- Windows PowerShell
	```powershell
	cd servico-equipamento; poetry install
	```
2. Suba o servidor
	```powershell
	poetry run uvicorn main:app --reload
	```
3. Acesse a documentação
	- http://localhost:8000/docs

## Testes
```powershell
poetry run pytest -q
```

## Docker
Build e run do container:
```powershell
docker build -t servico-equipamento .
docker run -p 8000:8000 servico-equipamento
```

## Healthcheck
`GET /health` retorna `{ "status": "ok" }`.

