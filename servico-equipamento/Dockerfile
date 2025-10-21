FROM python:3.11-slim

ENV POETRY_VERSION=1.7.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PIP_NO_CACHE_DIR=1 \
    PATH="/root/.local/bin:$PATH"

RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION

WORKDIR /app/servico-equipamento

# Copia manifestos de dependência primeiro (para cache de build eficiente)
COPY pyproject.toml ./

RUN poetry install --no-interaction --no-root

# Copia o código do serviço
COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]
