# Serviço de Equipamentos

Microsserviço para gerenciar bicicletas, trancas e totens do sistema de bicicletário.

## Sobre

Este projeto é uma API REST feita com FastAPI pra controlar os equipamentos do bicicletário. Basicamente tem 3 equipamentos principais: bicicletas, trancas (onde as bikes ficam presas) e totems (os pontos de estação).

A ideia é gerenciar todo o ciclo de vida desses equipamentos, desde cadastrar até integrar na rede, tirar da rede, consertar, etc.

## O que tem aqui

**Bicicletas:**
- Criar, listar, editar e deletar bikes
- Integrar bike na rede (colocar numa tranca)
- Retirar da rede
- Mudar status (disponível, em uso, em reparo, etc)

**Trancas:**
- CRUD básico de trancas
- Trancar e destrancar
- Integrar/remover da rede
- Associar com totems

**Totems:**
- Gerenciar os pontos de estação
- Ver quais trancas tem em cada totem
- Ver quais bikes estão em cada totem

## Tecnologias

- Python 3.11
- FastAPI
- TinyDB (banco de dados JSON simples)
- Pydantic pra validação
- Pytest pra testes
- Docker

## Como rodar

### Opção 1: Com Poetry

Precisa ter Python 3.11+ e Poetry instalado.

```bash
# Instalar dependências
poetry install

# Rodar o servidor
poetry run uvicorn main:app --reload
```

Abre no navegador: http://localhost:8000/docs

### Opção 2: Com Docker

Se tiver Docker instalado:

```bash
docker build -t servico-equipamento .
docker run -p 8000:8000 servico-equipamento
```

## Endpoints

Depois que rodar, acessa http://localhost:8000/docs pra ver todos os endpoints no Swagger.

Principais rotas:

**Bicicletas** (`/bicicleta`)
- GET / POST - listar e criar
- GET /{id} - buscar uma específica
- PUT /{id} - atualizar
- DELETE /{id} - remover
- POST /integrarNaRede - colocar bike numa tranca
- POST /retirarDaRede - tirar da rede
- POST /{id}/status/{acao} - mudar status

**Trancas** (`/tranca`)
- CRUD normal (GET, POST, PUT, DELETE)
- POST /{id}/trancar - trancar
- POST /{id}/destrancar - destrancar  
- POST /integrarNaRede e /retirarDaRede
- GET /{id}/bicicleta - ver qual bike tá na tranca

**Totems** (`/totem`)
- CRUD básico
- GET /{id}/trancas - lista trancas do totem
- GET /{id}/bicicletas - lista bikes do totem

**Admin**
- GET /status - ver se tá funcionando
- GET /restaurarBanco - reseta o banco pro estado inicial

## Testes

Tem 123 testes implementados. Pra rodar:

```bash
poetry run pytest
```

Se quiser ver a cobertura:

```bash
poetry run pytest --cov
```

Os testes estão na pasta `tests/` e cobrem os principais cenários dos endpoints.

## Estrutura

```
servico-equipamento/
├── main.py              # arquivo principal
├── database/            # gerenciamento do banco TinyDB
├── models/              # modelos Pydantic
├── repositories/        # camada de acesso a dados
├── routers/             # endpoints da API
└── tests/               # testes unitários
```

Arquitetura bem simples: routers chamam repositories que acessam o banco. Models fazem a validação com Pydantic.

## Problemas comuns

**Porta 8000 ocupada**
```bash
# muda a porta
poetry run uvicorn main:app --port 8001
```

**Erro de dependências**
```bash
poetry install --no-root
```
