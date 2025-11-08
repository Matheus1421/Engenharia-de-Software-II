# Banco de Dados JSON - Serviço de Equipamentos

Este documento descreve a estrutura do banco de dados JSON implementado para o microsserviço de equipamentos.

## Tecnologia Utilizada

O banco de dados utiliza **TinyDB**, uma biblioteca Python leve e simples para armazenar dados em formato JSON. É perfeita para simulações e protótipos, oferecendo uma interface semelhante a um banco de dados NoSQL.

### Por que TinyDB?

- ✅ **Sem configuração**: Não requer instalação ou configuração de servidor
- ✅ **JSON nativo**: Armazena dados em formato JSON legível
- ✅ **API simples**: Interface Python intuitiva para operações CRUD
- ✅ **Zero dependências externas**: Apenas uma biblioteca Python
- ✅ **Perfeito para desenvolvimento**: Ideal para prototipagem e testes

## Estrutura do Banco de Dados

O banco de dados é armazenado no arquivo `database/equipamentos.json` e contém 4 tabelas:

### 1. Bicicletas (`bicicletas`)

Armazena informações sobre bicicletas disponíveis no sistema.

**Campos:**
- `id` (int): Identificador único
- `marca` (string): Marca da bicicleta
- `modelo` (string): Modelo da bicicleta
- `ano` (string): Ano de fabricação
- `numero` (int): Número identificador da bicicleta
- `status` (enum): Status atual - valores possíveis:
  - `DISPONIVEL`: Disponível para aluguel
  - `EM_USO`: Atualmente alugada
  - `NOVA`: Recém cadastrada, ainda não integrada
  - `APOSENTADA`: Removida de circulação
  - `REPARO_SOLICITADO`: Aguardando reparo
  - `EM_REPARO`: Sendo reparada

**Exemplo:**
```json
{
  "id": 1,
  "marca": "Caloi",
  "modelo": "Mountain Bike Pro",
  "ano": "2023",
  "numero": 100,
  "status": "DISPONIVEL"
}
```

### 2. Trancas (`trancas`)

Armazena informações sobre trancas dos totems.

**Campos:**
- `id` (int): Identificador único
- `numero` (int): Número da tranca
- `localizacao` (string): Coordenadas GPS
- `anoDeFabricacao` (string): Ano de fabricação
- `modelo` (string): Modelo da tranca
- `status` (enum): Status atual - valores possíveis:
  - `LIVRE`: Sem bicicleta, disponível
  - `OCUPADA`: Com bicicleta presa
  - `NOVA`: Recém cadastrada
  - `APOSENTADA`: Desativada
  - `EM_REPARO`: Em manutenção
- `bicicleta` (int|null): ID da bicicleta associada (null se livre)

**Exemplo:**
```json
{
  "id": 1,
  "numero": 1,
  "localizacao": "-22.9068, -43.1729",
  "anoDeFabricacao": "2023",
  "modelo": "Tranca Smart v1",
  "status": "LIVRE",
  "bicicleta": null
}
```

### 3. Totems (`totems`)

Armazena informações sobre pontos de aluguel (totems).

**Campos:**
- `id` (int): Identificador único
- `localizacao` (string): Coordenadas GPS
- `descricao` (string): Descrição do local

**Exemplo:**
```json
{
  "id": 1,
  "localizacao": "-22.9068, -43.1729",
  "descricao": "Totem da Praça Central - Centro"
}
```

### 4. Relacionamento Tranca-Totem (`tranca_totem`)

Tabela associativa que relaciona trancas aos totems.

**Campos:**
- `idTranca` (int): ID da tranca
- `idTotem` (int): ID do totem

**Exemplo:**
```json
{
  "idTranca": 1,
  "idTotem": 1
}
```

## Repositórios

Cada entidade possui um repositório dedicado que encapsula as operações de banco de dados:

### BicicletaRepository
- `create(bicicleta: NovaBicicleta) -> Bicicleta`
- `get_by_id(bicicleta_id: int) -> Optional[Bicicleta]`
- `get_all() -> List[Bicicleta]`
- `update(bicicleta_id: int, bicicleta: NovaBicicleta) -> Optional[Bicicleta]`
- `delete(bicicleta_id: int) -> bool`
- `update_status(bicicleta_id: int, status: StatusBicicleta) -> Optional[Bicicleta]`

### TrancaRepository
- `create(tranca: NovaTranca) -> Tranca`
- `get_by_id(tranca_id: int) -> Optional[Tranca]`
- `get_all() -> List[Tranca]`
- `update(tranca_id: int, tranca: NovaTranca) -> Optional[Tranca]`
- `delete(tranca_id: int) -> bool`
- `update_status(tranca_id: int, status: StatusTranca) -> Optional[Tranca]`
- `associar_bicicleta(tranca_id: int, bicicleta_id: Optional[int]) -> Optional[Tranca]`
- `get_bicicleta_id(tranca_id: int) -> Optional[int]`
- `associar_totem(tranca_id: int, totem_id: int) -> bool`
- `desassociar_totem(tranca_id: int) -> bool`
- `get_totem_id(tranca_id: int) -> Optional[int]`

### TotemRepository
- `create(totem: NovoTotem) -> Totem`
- `get_by_id(totem_id: int) -> Optional[Totem]`
- `get_all() -> List[Totem]`
- `update(totem_id: int, totem: NovoTotem) -> Optional[Totem]`
- `delete(totem_id: int) -> bool`
- `get_trancas_ids(totem_id: int) -> List[int]`

## Dados Iniciais

O banco de dados é inicializado automaticamente na primeira execução com dados de exemplo:
- 3 bicicletas
- 3 trancas
- 2 totems
- Relacionamentos entre trancas e totems

## Endpoint de Restauração

O endpoint `/restaurarBanco` (GET) permite restaurar o banco de dados para o estado inicial:

```bash
curl http://localhost:8000/restaurarBanco
```

**Resposta:**
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

## Uso nos Serviços

Para utilizar o banco de dados em seus serviços:

```python
from database.database import get_db
from repositories.bicicleta_repository import BicicletaRepository

# Obtém a instância do banco
db = get_db()

# Cria um repositório
bicicleta_repo = BicicletaRepository(db)

# Usa as operações
bicicleta = bicicleta_repo.get_by_id(1)
todas_bicicletas = bicicleta_repo.get_all()
```

## Instalação de Dependências

Para instalar as dependências necessárias:

```bash
cd servico-equipamento
poetry install
```

Ou adicionar o TinyDB manualmente:

```bash
poetry add tinydb
```

## Localização dos Arquivos

```
servico-equipamento/
├── database/
│   ├── database.py          # Gerenciador do banco de dados
│   ├── init_data.py         # Dados iniciais
│   ├── equipamentos.json    # Arquivo do banco (gerado automaticamente)
│   └── DATABASE_README.md   # Esta documentação
├── repositories/
│   ├── bicicleta_repository.py
│   ├── tranca_repository.py
│   └── totem_repository.py
└── models/
    ├── bicicleta_model.py
    ├── tranca_model.py
    ├── totem_model.py
    └── erro_model.py
```

## Notas Importantes

- O arquivo `equipamentos.json` é criado automaticamente na primeira execução
- Não é necessário criar o arquivo manualmente
- O banco é thread-safe para operações básicas
- Para produção, considere migrar para PostgreSQL, MySQL ou MongoDB
- O TinyDB é recomendado apenas para desenvolvimento e testes
