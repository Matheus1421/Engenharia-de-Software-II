# Dockerfile para o Microsserviço de Aluguel

FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --no-dev

COPY . .

EXPOSE 8001

# Comando para iniciar o servidor
# 0.0.0.0 permite acessar de fora do container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
