# 🚲 Implementação do Banco de Dados JSON - Serviço de Equipamentos

Este documento descreve a implementação completa do banco de dados JSON para o microsserviço de equipamentos do Sistema de Controle de Bicicletário (SCB).

## 📋 Resumo da Implementação

Foi implementado um sistema completo de banco de dados JSON utilizando a biblioteca **TinyDB** para simular o armazenamento de dados do microsserviço de equipamentos, incluindo:

- ✅ Modelos Pydantic para todas as entidades (Bicicleta, Tranca, Totem)
- ✅ Camada de banco de dados com gerenciamento singleton
- ✅ Repositórios com operações CRUD completas
- ✅ Dados iniciais para popular o banco
- ✅ Endpoint `/restaurarBanco` para resetar os dados
- ✅ Integração com FastAPI
- ✅ Documentação completa

## 📁 Estrutura de Arquivos Criados

```
servico-equipamento/
├── database/
│   ├── database.py              # Gerenciador do banco de dados (singleton)
│   ├── init_data.py             # Dados iniciais do banco
│   ├── equipamentos.json        # Arquivo JSON (gerado automaticamente)
│   └── DATABASE_README.md       # Documentação detalhada do banco
│
├── repositories/
│   ├── bicicleta_repository.py  # CRUD de bicicletas
│   ├── tranca_repository.py     # CRUD de trancas
│   └── totem_repository.py      # CRUD de totems
│
├── models/
│   ├── bicicleta_model.py       # Modelo Pydantic de Bicicleta
│   ├── tranca_model.py          # Modelo Pydantic de Tranca
│   ├── totem_model.py           # Modelo Pydantic de Totem
│   ├── erro_model.py            # Modelo Pydantic de Erro
│   └── status_model.py          # (já existia)
│
├── routers/
│   ├── admin.py                 # Router com endpoint /restaurarBanco
│   └── status.py                # (já existia)
│
├── exemplo_banco.py             # Script de demonstração
└── pyproject.toml               # Atualizado com TinyDB
```

## 🗄️ Estrutura do Banco de Dados

### Tabelas

1. **bicicletas** - Armazena informações das bicicletas
2. **trancas** - Armazena informações das trancas
3. **totems** - Armazena informações dos totems (pontos de aluguel)
4. **tranca_totem** - Tabela associativa que relaciona trancas aos totems

### Modelos de Dados

#### Bicicleta
```python
{
  "id": int,
  "marca": str,
  "modelo": str,
  "ano": str,
  "numero": int,
  "status": enum['DISPONIVEL', 'EM_USO', 'NOVA', 'APOSENTADA', 
                  'REPARO_SOLICITADO', 'EM_REPARO']
}
```

#### Tranca
```python
{
  "id": int,
  "numero": int,
  "localizacao": str,
  "anoDeFabricacao": str,
  "modelo": str,
  "status": enum['LIVRE', 'OCUPADA', 'NOVA', 'APOSENTADA', 'EM_REPARO'],
  "bicicleta": int | null
}
```

#### Totem
```python
{
  "id": int,
  "localizacao": str,
  "descricao": str
}
```

## 🚀 Como Usar

### 1. Instalar Dependências

```bash
cd servico-equipamento
poetry install
```

### 2. Executar o Script de Demonstração

```bash
poetry run python exemplo_banco.py
```

Este script demonstra todas as funcionalidades do banco de dados:
- Inicialização com dados de exemplo
- Listagem de todas as entidades
- Busca por ID
- Criação de novos registros
- Atualização de status
- Associação entre trancas e bicicletas
- Remoção de registros

### 3. Iniciar o Servidor

```bash
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Acessar a Documentação da API

Após iniciar o servidor, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 5. Testar o Endpoint de Restauração

```bash
# Via curl
curl http://localhost:8000/restaurarBanco

# Via navegador
# Abra: http://localhost:8000/restaurarBanco
```

**Resposta esperada:**
```json
{
  "mensagem": "Banco de dados restaurado com sucesso",
  "dados_inseridos": {
    "bicicletas": 3,
    "trancas": 3,
    "totems": 2,
    "relacionamentos": 3
  }
}
```

## 💡 Exemplos de Uso nos Serviços

### Exemplo 1: Usar Repositório de Bicicletas

```python
from database.database import get_db
from repositories.bicicleta_repository import BicicletaRepository
from models.bicicleta_model import NovaBicicleta, StatusBicicleta

# Obtém a instância do banco
db = get_db()
bicicleta_repo = BicicletaRepository(db)

# Listar todas as bicicletas
bicicletas = bicicleta_repo.get_all()

# Buscar uma bicicleta específica
bicicleta = bicicleta_repo.get_by_id(1)

# Criar nova bicicleta
nova_bici = NovaBicicleta(
    marca="Caloi",
    modelo="Elite",
    ano="2024",
    numero=150,
    status=StatusBicicleta.NOVA
)
bici_criada = bicicleta_repo.create(nova_bici)

# Atualizar status
bici_atualizada = bicicleta_repo.update_status(
    bici_criada.id, 
    StatusBicicleta.DISPONIVEL
)
```

### Exemplo 2: Associar Tranca e Bicicleta

```python
from repositories.tranca_repository import TrancaRepository

tranca_repo = TrancaRepository(db)

# Associar bicicleta ID 1 à tranca ID 1
tranca_atualizada = tranca_repo.associar_bicicleta(
    tranca_id=1, 
    bicicleta_id=1
)

# Desassociar (passar None)
tranca_livre = tranca_repo.associar_bicicleta(
    tranca_id=1, 
    bicicleta_id=None
)
```

### Exemplo 3: Listar Trancas de um Totem

```python
from repositories.totem_repository import TotemRepository

totem_repo = TotemRepository(db)
tranca_repo = TrancaRepository(db)

# Obter IDs das trancas do totem 1
trancas_ids = totem_repo.get_trancas_ids(totem_id=1)

# Buscar detalhes de cada tranca
for tranca_id in trancas_ids:
    tranca = tranca_repo.get_by_id(tranca_id)
    print(f"Tranca #{tranca.numero} - Status: {tranca.status}")
```

## 📊 Dados Iniciais

O banco é inicializado automaticamente com os seguintes dados:

### Bicicletas (3)
1. Caloi Mountain Bike Pro 2023 - DISPONIVEL
2. Shimano City Bike 2023 - DISPONIVEL
3. Trek Speed Master 2024 - NOVA

### Trancas (3)
1. Tranca Smart v1 #1 - LIVRE - Totem 1
2. Tranca Smart v1 #2 - LIVRE - Totem 1
3. Tranca Smart v2 #3 - NOVA - Totem 2

### Totems (2)
1. Totem da Praça Central - Centro
2. Totem do Parque Municipal

## 🔧 Funcionalidades dos Repositórios

### BicicletaRepository
- `create()` - Criar nova bicicleta
- `get_by_id()` - Buscar por ID
- `get_all()` - Listar todas
- `update()` - Atualizar dados completos
- `delete()` - Remover bicicleta
- `update_status()` - Atualizar apenas o status

### TrancaRepository
- `create()` - Criar nova tranca
- `get_by_id()` - Buscar por ID
- `get_all()` - Listar todas
- `update()` - Atualizar dados completos
- `delete()` - Remover tranca
- `update_status()` - Atualizar apenas o status
- `associar_bicicleta()` - Associar/desassociar bicicleta
- `get_bicicleta_id()` - Obter ID da bicicleta associada
- `associar_totem()` - Associar tranca a um totem
- `desassociar_totem()` - Remover associação com totem
- `get_totem_id()` - Obter ID do totem associado

### TotemRepository
- `create()` - Criar novo totem
- `get_by_id()` - Buscar por ID
- `get_all()` - Listar todos
- `update()` - Atualizar dados completos
- `delete()` - Remover totem
- `get_trancas_ids()` - Obter IDs das trancas do totem

## 📝 Notas Importantes

### Por que TinyDB?

1. **Simplicidade**: Não requer instalação ou configuração de servidor de banco de dados
2. **JSON Nativo**: Armazena dados em formato JSON legível e editável
3. **Zero Configuração**: Funciona out-of-the-box sem setup complexo
4. **Ideal para Desenvolvimento**: Perfeito para prototipagem e testes
5. **API Pythônica**: Interface intuitiva e fácil de usar

### Limitações

- **Não é adequado para produção** com alta carga
- **Sem suporte a transações** complexas
- **Performance limitada** com grandes volumes de dados
- **Concorrência limitada** (não recomendado para múltiplos processos)

### Migração Futura

Para produção, considere migrar para:
- **PostgreSQL** (recomendado)
- **MySQL/MariaDB**
- **MongoDB**

A arquitetura com repositórios facilita essa migração, pois basta:
1. Criar novos repositórios com a nova tecnologia
2. Manter as mesmas interfaces
3. Trocar a injeção de dependências

## 🧪 Testando

### Verificar se o Banco Funciona

```bash
# Executar script de demonstração
poetry run python exemplo_banco.py

# Verificar se o arquivo JSON foi criado
ls database/equipamentos.json
```

### Inspecionar o Banco de Dados

O arquivo `database/equipamentos.json` pode ser aberto e editado em qualquer editor de texto. Ele contém todos os dados em formato JSON legível.

## 📚 Documentação Adicional

Para mais detalhes sobre a estrutura do banco de dados, consulte:
- `database/DATABASE_README.md` - Documentação detalhada do banco de dados

## ✅ Checklist de Implementação

- [x] Adicionar TinyDB ao pyproject.toml
- [x] Criar modelos Pydantic para Bicicleta, Tranca, Totem e Erro
- [x] Implementar gerenciador de banco de dados (database.py)
- [x] Criar dados iniciais (init_data.py)
- [x] Implementar repositórios CRUD para todas as entidades
- [x] Criar endpoint /restaurarBanco
- [x] Integrar com FastAPI (main.py)
- [x] Criar script de demonstração (exemplo_banco.py)
- [x] Adicionar banco ao .gitignore
- [x] Documentar toda a implementação
- [x] Testar todas as funcionalidades

## 🎯 Próximos Passos

Para completar a implementação da API conforme o Swagger:

1. **Criar routers para as entidades**:
   - `/bicicleta` - Endpoints CRUD de bicicletas
   - `/tranca` - Endpoints CRUD de trancas
   - `/totem` - Endpoints CRUD de totems

2. **Implementar endpoints específicos**:
   - `/bicicleta/integrarNaRede`
   - `/bicicleta/retirarDaRede`
   - `/tranca/trancar`
   - `/tranca/destrancar`
   - etc.

3. **Adicionar validações**:
   - Validar transições de status
   - Validar regras de negócio
   - Tratamento de erros

4. **Testes**:
   - Testes unitários dos repositórios
   - Testes de integração da API
   - Testes de validação

## 🤝 Contribuindo

Para adicionar novos endpoints ou funcionalidades:

1. Crie o modelo Pydantic em `models/`
2. Implemente o repositório em `repositories/`
3. Crie o router em `routers/`
4. Registre o router no `main.py`

---

**Implementado com base em:**
- Especificação Swagger fornecida
- PDFs de requisitos do sistema
- Boas práticas de arquitetura em camadas
