# Serviço Externo

Microsserviço para gerenciar serviços externos do sistema de bicicletário, incluindo notificações por e-mail, processamento de cobranças e validação de cartão de crédito.

## Sobre

Este projeto é uma API REST feita com FastAPI para controlar os serviços externos do bicicletário. Os principais serviços são:

1. **Notificações por e-mail**: Envio de e-mails para usuários do sistema
2. **Processamento e consulta de cobranças**: Gerenciamento de cobranças e pagamentos
3. **Validação de cartão de crédito**: Validação de dados de cartões de crédito

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

# Configurar variáveis de ambiente (opcional)
# Copie config.env.example para .env e configure suas credenciais SMTP
cp config.env.example .env
# Edite o arquivo .env com suas credenciais

# Rodar o servidor
poetry run uvicorn main:app --reload
```

Abre no navegador: http://localhost:8000/docs

### Opção 2: Com Docker

Se tiver Docker instalado:

```bash
docker build -t servico-externo .
docker run -p 8000:8000 servico-externo
```

## Configuração de E-mail (SMTP)

O serviço de e-mail usa SMTP para envio real de e-mails. Você pode configurar as credenciais de duas formas:

### 1. Arquivo .env (Recomendado)

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=seu-email@gmail.com
SMTP_PASSWORD=sua-senha-ou-app-password
SMTP_FROM_EMAIL=seu-email@gmail.com
SMTP_USE_TLS=true
```

**Para Gmail:**
- Use uma "App Password" ao invés da senha normal
- Ative a verificação em duas etapas
- Gere uma App Password em: https://myaccount.google.com/apppasswords

**Para outros provedores:**
- **Outlook/Hotmail**: `smtp-mail.outlook.com`, porta 587
- **Yahoo**: `smtp.mail.yahoo.com`, porta 587
- **Servidor próprio**: Configure conforme seu servidor SMTP

### 2. Variáveis de Ambiente do Sistema

Configure as variáveis diretamente no sistema operacional antes de rodar o servidor.

### Modo de Simulação

Se as credenciais SMTP não estiverem configuradas, o sistema entrará em **modo de simulação**, onde os e-mails são apenas registrados no banco de dados mas não são enviados realmente. Isso é útil para desenvolvimento e testes.

## Endpoints

Depois que rodar, acessa http://localhost:8000/docs pra ver todos os endpoints no Swagger.

Principais rotas:

**Notificações por E-mail** (`/email`)
- POST /enviar - enviar e-mail
- GET /{id} - consultar e-mail enviado
- GET - listar todos os e-mails

**Cobranças** (`/cobranca`)
- POST - criar cobrança
- GET /{id} - consultar cobrança
- GET - listar todas as cobranças
- POST /{id}/processar - processar pagamento
- GET /{id}/status - consultar status da cobrança

**Validação de Cartão** (`/cartao`)
- POST /validar - validar cartão de crédito
- GET /{id} - consultar validação realizada
- GET - listar todas as validações

**Admin**
- GET /status - ver se tá funcionando
- GET /restaurarBanco - reseta o banco pro estado inicial

## Testes

Pra rodar os testes:

```bash
poetry run pytest
```

Se quiser ver a cobertura:

```bash
poetry run pytest --cov
```

## Estrutura

```
servico-externo/
├── main.py              # arquivo principal
├── database/            # gerenciamento do banco TinyDB
├── models/              # modelos Pydantic
├── repositories/        # camada de acesso a dados
├── routers/             # endpoints da API
├── services/            # serviços externos (SMTP, etc)
└── tests/               # testes unitários
```

Arquitetura bem simples: routers chamam services/repositories que acessam o banco. Models fazem a validação com Pydantic.

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

