# 📁 Estrutura do Projeto - Serviço de Equipamentos

## 📋 Índice
1. [Visão Geral](#visão-geral)
2. [Estrutura de Pastas](#estrutura-de-pastas)
3. [Arquivos Raiz](#arquivos-raiz)
4. [Código Fonte](#código-fonte)
5. [Testes](#testes)
6. [Documentação](#documentação)
7. [Relatórios e Artefatos](#relatórios-e-artefatos)

---

## 🎯 Visão Geral

Este é um **microserviço REST API** desenvolvido em **FastAPI** para gerenciamento de equipamentos de um sistema de compartilhamento de bicicletas. O serviço gerencia:
- 🚲 **Bicicletas** (8 endpoints)
- 🔒 **Trancas** (11 endpoints)
- 🏪 **Totens** (5 endpoints)
- 👨‍💼 **Administração** (1 endpoint)
- ❤️ **Status** (1 endpoint)

**Total**: 26 endpoints RESTful

---

## 📂 Estrutura de Pastas

```
servico-equipamento/
├── 📁 database/          # Camada de persistência de dados
├── 📁 models/            # Modelos de dados (Pydantic)
├── 📁 repositories/      # Camada de acesso a dados (Repository Pattern)
├── 📁 routers/           # Endpoints da API (Controllers)
├── 📁 services/          # Lógica de negócio (futura expansão)
├── 📁 tests/             # Testes unitários automatizados
├── 📁 htmlcov/           # Relatórios de cobertura de testes (HTML)
├── 📁 .pytest_cache/     # Cache do pytest
└── 📁 __pycache__/       # Cache do Python (bytecode compilado)
```

---

## 📁 Detalhamento das Pastas

### 1. 📁 `database/` - Persistência de Dados

Implementa um banco de dados **JSON** usando **TinyDB**.

| Arquivo | Finalidade | Linhas |
|---------|-----------|---------|
| `database.py` | Singleton do banco de dados, gerencia conexão e operações básicas | ~36 |
| `init_data.py` | Dados iniciais de exemplo (bicicletas, trancas, totens) | ~21 |
| `equipamentos.json` | Arquivo JSON com os dados persistidos | Variável |
| `DATABASE_README.md` | Documentação da implementação do banco | ~150 |

**Por que JSON?**
- ✅ Simplicidade (sem necessidade de servidor de BD)
- ✅ Portabilidade (arquivo único)
- ✅ Adequado para protótipos e demonstrações
- ✅ Fácil inspeção e debug

---

### 2. 📁 `models/` - Modelos de Dados

Define as **estruturas de dados** usando **Pydantic** para validação automática.

| Arquivo | Finalidade | Responsabilidade |
|---------|-----------|------------------|
| `bicicleta_model.py` | Modelos de Bicicleta | `Bicicleta`, `NovaBicicleta`, `StatusBicicleta` (enum) |
| `tranca_model.py` | Modelos de Tranca | `Tranca`, `NovaTranca`, `StatusTranca` (enum) |
| `totem_model.py` | Modelos de Totem | `Totem`, `NovoTotem` |
| `erro_model.py` | Modelos de Erro | `Erro` (padronização de respostas de erro) |
| `status_model.py` | Enums de Status | Centraliza todos os enums de status |

**Padrão Utilizado**:
- `Nova*` = Modelo para criação (sem ID)
- Classe principal = Modelo completo (com ID)
- Enums = Valores válidos para status

**Benefícios do Pydantic**:
- ✅ Validação automática de tipos
- ✅ Serialização/deserialização JSON automática
- ✅ Documentação automática no Swagger
- ✅ Type hints para IDEs

---

### 3. 📁 `repositories/` - Acesso a Dados

Implementa o **Repository Pattern** para abstrair o acesso ao banco de dados.

| Arquivo | Finalidade | Principais Métodos |
|---------|-----------|-------------------|
| `bicicleta_repository.py` | CRUD de bicicletas | `get_all()`, `get_by_id()`, `create()`, `update()`, `delete()` |
| `tranca_repository.py` | CRUD de trancas | `get_all()`, `get_by_id()`, `create()`, `update()`, `delete()`, `associar_bicicleta()` |
| `totem_repository.py` | CRUD de totens | `get_all()`, `get_by_id()`, `create()`, `update()`, `delete()`, `get_trancas_ids()` |

**Por que Repository Pattern?**
- ✅ Separação de responsabilidades (API ↔ Dados)
- ✅ Facilita testes (mock repositories)
- ✅ Permite trocar banco de dados sem alterar API
- ✅ Centraliza queries e lógica de acesso

---

### 4. 📁 `routers/` - Endpoints da API

Contém os **controllers** que definem os endpoints REST.

| Arquivo | Endpoints | Responsabilidade | Cobertura |
|---------|-----------|-----------------|-----------|
| `bicicleta.py` | 8 endpoints | CRUD + operações de bicicletas | 100% ✅ |
| `tranca.py` | 11 endpoints | CRUD + operações de trancas | 100% ✅ |
| `totem.py` | 5 endpoints | CRUD + listagens de totens | 100% ✅ |
| `status.py` | 1 endpoint | Health check da API | 100% ✅ |
| `admin.py` | 1 endpoint | Restaurar banco de dados | 67% ⚠️ |

**Padrão RESTful**:
- `GET /recurso` → Listar todos
- `GET /recurso/{id}` → Obter específico
- `POST /recurso` → Criar novo
- `PUT /recurso/{id}` → Atualizar completo
- `DELETE /recurso/{id}` → Remover

**Operações Especiais**:
- `POST /bicicleta/{id}/status/{acao}` → Alterar status
- `POST /bicicleta/integrarNaRede` → Integrar bicicleta
- `POST /bicicleta/retirarDaRede` → Retirar bicicleta
- `POST /tranca/{id}/trancar` → Trancar com/sem bicicleta
- `POST /tranca/{id}/destrancar` → Destrancar
- `POST /tranca/integrarNaRede` → Integrar tranca
- `POST /tranca/retirarDaRede` → Retirar tranca

---

### 5. 📁 `services/` - Lógica de Negócio

| Arquivo | Finalidade | Status |
|---------|-----------|--------|
| `equipamento_service.py` | Serviço de equipamentos (placeholder) | Não utilizado atualmente |

**Nota**: A lógica de negócio está atualmente nos routers. Esta pasta está preparada para **refatoração futura** seguindo o padrão Service Layer.

---

### 6. 📁 `tests/` - Testes Unitários

Contém toda a **suíte de testes automatizados** usando **pytest**.

| Arquivo | Finalidade | Testes | Cobertura |
|---------|-----------|--------|-----------|
| `conftest.py` | Configurações e fixtures do pytest | - | - |
| `test_bicicleta_endpoints.py` | Testes dos endpoints de bicicletas | 33 | 100% ✅ |
| `test_totem_endpoints.py` | Testes dos endpoints de totens | 36 | 100% ✅ |
| `test_tranca_endpoints.py` | Testes dos endpoints de trancas | 53 | 100% ✅ |
| `test_status_endpoint.py` | Teste do endpoint de status | 1 | 100% ✅ |

**Total**: 123 testes, 100% de sucesso, 80.66% de cobertura geral

**Técnicas Utilizadas**:
- ✅ **Mocking completo** (unittest.mock)
- ✅ **Fixtures reutilizáveis** (pytest fixtures)
- ✅ **TestClient** do FastAPI
- ✅ **Isolamento total** (sem dependências externas)
- ✅ **Testes de cenários positivos e negativos**

**Tipos de Testes**:
1. **Sucesso** (happy path)
2. **Erro 404** (recursos não encontrados)
3. **Erro 422** (validação de dados)
4. **Exceções** (tratamento de erros)

---

### 7. 📁 `htmlcov/` - Relatórios de Cobertura

Relatórios **HTML interativos** gerados pelo `pytest-cov`.

| Arquivo | Finalidade |
|---------|-----------|
| `index.html` | Página principal com resumo de cobertura |
| `*_py.html` | Relatório individual de cada arquivo Python |
| `coverage_html_cb_*.js` | Scripts JavaScript do relatório |
| `style_cb_*.css` | Estilos CSS do relatório |
| `status.json` | Metadados da cobertura |

**Como usar**: Abra `htmlcov/index.html` no navegador para ver:
- 📊 Porcentagem de cobertura por arquivo
- 🔴 Linhas não cobertas (em vermelho)
- 🟢 Linhas cobertas (em verde)
- 🟡 Linhas parcialmente cobertas (em amarelo)

---

### 8. 📁 `.pytest_cache/` - Cache do Pytest

Arquivos de cache do pytest para otimizar execuções subsequentes.

| Arquivo/Pasta | Finalidade |
|---------------|-----------|
| `.gitignore` | Ignora cache no git |
| `CACHEDIR.TAG` | Identifica diretório de cache |
| `README.md` | Explicação do cache |
| `v/cache/` | Dados de cache (nodeids, lastfailed, stepwise) |

**Pode ser deletado**: O pytest recria automaticamente.

---

### 9. 📁 `__pycache__/` - Cache do Python

Bytecode compilado dos arquivos Python (`.pyc`).

**Finalidade**: Acelera execução do código Python.  
**Pode ser deletado**: Python recria automaticamente.  
**Ignorado no git**: `.gitignore` já está configurado.

---

## 📄 Arquivos Raiz

### 🔧 Configuração

| Arquivo | Finalidade | Importância |
|---------|-----------|-------------|
| `main.py` | **Ponto de entrada** da aplicação FastAPI | 🔴 CRÍTICO |
| `pyproject.toml` | Configuração do Poetry (dependências, scripts) | 🔴 CRÍTICO |
| `poetry.lock` | Lock de versões exatas das dependências | 🔴 CRÍTICO |
| `Dockerfile` | Containerização da aplicação | 🟡 PRODUÇÃO |
| `.coveragerc` | Configuração do coverage (exclusões, etc) | 🟢 OPCIONAL |

#### 📝 `main.py` - Aplicação Principal
```python
# Inicializa FastAPI
# Registra todos os routers
# Configura CORS
# Define metadata da API
```

**Responsabilidades**:
- ✅ Criar instância do FastAPI
- ✅ Incluir routers (bicicleta, tranca, totem, admin, status)
- ✅ Configurar CORS para permitir requisições de origens diferentes
- ✅ Definir título, descrição e versão da API

#### 📦 `pyproject.toml` - Gerenciamento de Dependências
```toml
[tool.poetry.dependencies]
python = "^3.11"
fastapi = "0.104.1"
uvicorn = "0.24.0"
pydantic = "2.4.2"
tinydb = "4.8.0"
httpx = "0.25.1"

[tool.poetry.group.dev.dependencies]
pytest = "7.4.2"
pytest-cov = "4.1.0"
```

**Por que Poetry?**
- ✅ Gerenciamento moderno de dependências
- ✅ Ambientes virtuais automáticos
- ✅ Lock de versões (reprodutibilidade)
- ✅ Scripts customizados

#### 🐳 `Dockerfile` - Containerização
```dockerfile
# Imagem base Python
# Instala Poetry
# Copia dependências e código
# Expõe porta 8000
# Comando de inicialização
```

**Para que serve?**
- ✅ Deploy em qualquer ambiente (Heroku, Railway, AWS, etc)
- ✅ Isolamento de dependências
- ✅ Reprodutibilidade garantida

---

### 📊 Relatórios e Artefatos

| Arquivo | Finalidade | Gerado por |
|---------|-----------|-----------|
| `.coverage` | Dados binários de cobertura | pytest-cov |
| `coverage.xml` | Relatório de cobertura em XML (para CI/CD) | pytest-cov |

**Uso**:
- `.coverage` → Lido pelo pytest-cov
- `coverage.xml` → Enviado para SonarCloud, Codecov, etc

---

### 📚 Documentação

#### 🎯 Documentação Técnica Principal

| Arquivo | Conteúdo | Audiência |
|---------|----------|-----------|
| `README.md` | **Visão geral do projeto**, instalação, uso | 👥 TODOS |
| `COMO_EXECUTAR.md` | Instruções passo a passo de instalação e execução | 👨‍💻 Desenvolvedores |
| `ESTRUTURA_PROJETO.md` | Este arquivo - estrutura completa do projeto | 👨‍🏫 Apresentação |

#### 🧪 Documentação de Testes

| Arquivo | Conteúdo | Finalidade |
|---------|----------|-----------|
| `TESTES_README.md` | Guia geral de testes | Introdução aos testes |
| `GUIA_TESTES_COMPLETO.md` | Guia técnico detalhado de testes | Referência técnica |
| `TESTES_EXECUTIVO_FINAL.md` | **Resumo executivo** com estatísticas finais | 📊 Apresentação executiva |
| `RESUMO_TESTES_BICICLETAS.md` | Detalhamento dos 33 testes de bicicletas | Documentação específica |
| `RESUMO_TESTES_TOTENS.md` | Detalhamento dos 36 testes de totens | Documentação específica |
| `RESUMO_TESTES_TRANCAS.md` | Detalhamento dos 53 testes de trancas | Documentação específica |

**Destaque para Apresentação**: `TESTES_EXECUTIVO_FINAL.md`
- ✅ 123 testes implementados
- ✅ 80.66% de cobertura (meta atingida!)
- ✅ 100% taxa de sucesso
- ✅ Comparativos e gráficos

#### 🔌 Documentação de Endpoints

| Arquivo | Conteúdo | Endpoints |
|---------|----------|-----------|
| `ENDPOINTS_BICICLETA.md` | Documentação detalhada dos endpoints de bicicletas | 8 endpoints |
| `ENDPOINTS_TRANCA.md` | Documentação detalhada dos endpoints de trancas | 11 endpoints |
| `TODOS_OS_ENDPOINTS.md` | Visão geral de todos os 26 endpoints | Todos |

**Conteúdo**:
- ✅ Método HTTP, rota, descrição
- ✅ Parâmetros e body
- ✅ Respostas de sucesso e erro
- ✅ Exemplos de uso

#### 🏗️ Documentação de Implementação

| Arquivo | Conteúdo |
|---------|----------|
| `RESUMO_IMPLEMENTACAO_TRANCAS.md` | Resumo da implementação dos endpoints de trancas |
| `IMPLEMENTACAO_BANCO.md` | Detalhes técnicos da implementação do banco JSON |

#### 🔧 Documentação de Suporte

| Arquivo | Conteúdo |
|---------|----------|
| `TROUBLESHOOTING.md` | Soluções para problemas comuns |
| `SONARCLOUD_SETUP.md` | Guia de configuração do SonarCloud |

---

## 🎯 Arquitetura do Projeto

### Camadas da Aplicação

```
┌─────────────────────────────────────────┐
│          CLIENT (HTTP Requests)          │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│         ROUTERS (Controllers)            │  ← routers/
│  - bicicleta.py, tranca.py, totem.py    │
│  - Validação de entrada (Pydantic)      │
│  - Lógica de negócio                    │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│      REPOSITORIES (Data Access)          │  ← repositories/
│  - Abstração do banco de dados          │
│  - CRUD operations                       │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│          DATABASE (Persistence)          │  ← database/
│  - TinyDB (JSON)                        │
│  - equipamentos.json                    │
└─────────────────────────────────────────┘

      MODELS (Data Structures) ← models/
      - Pydantic models em todas as camadas
```

---

## 🚀 Fluxo de uma Requisição

### Exemplo: `GET /bicicleta/1`

```
1. 📥 Cliente faz requisição HTTP
   └→ GET http://localhost:8000/bicicleta/1

2. 🎯 FastAPI roteia para bicicleta.py
   └→ Função obter_bicicleta(idBicicleta: int)

3. ✅ Validação automática (Pydantic)
   └→ idBicicleta deve ser int positivo

4. 🔍 Router chama Repository
   └→ bicicleta_repo.get_by_id(1)

5. 💾 Repository consulta banco
   └→ db.search(Query().id == 1)

6. 📦 Retorna modelo Bicicleta
   └→ Bicicleta(id=1, marca="Trek", ...)

7. 📤 Serialização automática para JSON
   └→ FastAPI converte Pydantic para JSON

8. ✅ Resposta HTTP 200
   └→ {"id": 1, "marca": "Trek", ...}
```

---

## 🧪 Fluxo de Testes

### Exemplo: Teste de GET /bicicleta/1

```python
# tests/test_bicicleta_endpoints.py

def test_obter_bicicleta_sucesso(client, bicicleta_exemplo):
    # 1. ARRANGE: Preparar mocks
    with patch('routers.bicicleta.get_db') as mock_db, \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo:
        
        # Mock retorna bicicleta de exemplo
        mock_repo.return_value.get_by_id.return_value = bicicleta_exemplo
        
        # 2. ACT: Fazer requisição
        response = client.get("/bicicleta/1")
        
        # 3. ASSERT: Verificar resposta
        assert response.status_code == 200
        assert data["marca"] == "Trek"
```

**Benefícios**:
- ✅ Sem dependências externas (mocks)
- ✅ Rápido (sem IO)
- ✅ Confiável (isolado)
- ✅ Repetível (sempre funciona)

---

## 📊 Métricas do Projeto

### Estatísticas de Código

| Métrica | Valor |
|---------|-------|
| **Total de Linhas de Código** | ~2.000 linhas |
| **Total de Endpoints** | 26 endpoints |
| **Total de Modelos** | 12 models |
| **Total de Repositories** | 3 repositories |
| **Total de Routers** | 5 routers |

### Estatísticas de Testes

| Métrica | Valor | Status |
|---------|-------|--------|
| **Total de Testes** | 123 | ✅ |
| **Taxa de Sucesso** | 100% | ✅ |
| **Cobertura Geral** | 80.66% | ✅ Meta atingida |
| **Cobertura de Routers** | 97.52% | ✅ |
| **Tempo de Execução** | 2.25s | ⚡ |

### Cobertura Detalhada

| Módulo | Cobertura | Linhas |
|--------|-----------|--------|
| routers/bicicleta.py | 100% | 121/121 |
| routers/tranca.py | 100% | 179/179 |
| routers/totem.py | 100% | 89/89 |
| routers/status.py | 100% | 6/6 |
| models/* | 90% | - |

---

## 🎓 Tecnologias e Padrões

### Stack Tecnológico

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.11+ | Linguagem principal |
| **FastAPI** | 0.104.1 | Framework web |
| **Uvicorn** | 0.24.0 | ASGI server |
| **Pydantic** | 2.4.2 | Validação de dados |
| **TinyDB** | 4.8.0 | Banco de dados JSON |
| **pytest** | 7.4.2 | Framework de testes |
| **pytest-cov** | 4.1.0 | Cobertura de testes |

### Padrões de Projeto

| Padrão | Implementação | Benefício |
|--------|--------------|-----------|
| **Repository Pattern** | repositories/* | Abstração de dados |
| **Singleton** | database.py | Uma instância do DB |
| **Dependency Injection** | FastAPI Depends | Testabilidade |
| **DTO Pattern** | models/Nova* | Separação de modelos |
| **RESTful API** | routers/* | Padrão HTTP |

### Clean Code Principles

✅ **SOLID**
- Single Responsibility (cada classe uma responsabilidade)
- Open/Closed (extensível sem modificação)
- Liskov Substitution (herança correta)
- Interface Segregation (interfaces específicas)
- Dependency Inversion (depende de abstrações)

✅ **DRY** (Don't Repeat Yourself)
- Fixtures reutilizáveis nos testes
- Repository pattern evita duplicação

✅ **KISS** (Keep It Simple, Stupid)
- Código limpo e legível
- Funções pequenas e focadas

---

## 🎯 Pontos Fortes do Projeto

### 1. Arquitetura Limpa
- ✅ Separação clara de responsabilidades
- ✅ Camadas bem definidas (Router → Repository → Database)
- ✅ Fácil manutenção e extensão

### 2. Qualidade de Código
- ✅ Type hints em todo o código
- ✅ Validação automática com Pydantic
- ✅ Tratamento de erros padronizado

### 3. Testes Abrangentes
- ✅ 123 testes automatizados
- ✅ 80.66% de cobertura
- ✅ 100% cobertura nos routers principais

### 4. Documentação Completa
- ✅ 11 arquivos de documentação
- ✅ Swagger automático (FastAPI)
- ✅ Comentários no código

### 5. Pronto para Produção
- ✅ Dockerfile para containerização
- ✅ Configuração para CI/CD
- ✅ Relatórios de cobertura (XML para SonarCloud)

---

## 🚀 Como Executar

### 1. Instalação
```bash
# Instalar Poetry (se não tiver)
pip install poetry

# Instalar dependências
poetry install

# Ativar ambiente virtual
poetry shell
```

### 2. Executar Aplicação
```bash
# Modo desenvolvimento (com hot reload)
poetry run uvicorn main:app --reload

# Produção
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3. Acessar Documentação
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 4. Executar Testes
```bash
# Todos os testes
poetry run pytest

# Com cobertura
poetry run pytest --cov=. --cov-report=html

# Abrir relatório
# Abra htmlcov/index.html no navegador
```

---

## 📈 Evolução do Projeto

### Fase 1: Infraestrutura ✅
- [x] Setup do FastAPI
- [x] Banco de dados JSON
- [x] Models Pydantic
- [x] Repository Pattern

### Fase 2: Endpoints ✅
- [x] 8 endpoints de Bicicletas
- [x] 5 endpoints de Totens
- [x] 11 endpoints de Trancas
- [x] 1 endpoint de Admin
- [x] 1 endpoint de Status

### Fase 3: Testes ✅
- [x] 33 testes de Bicicletas
- [x] 36 testes de Totens
- [x] 53 testes de Trancas
- [x] 1 teste de Status
- [x] 80%+ cobertura alcançada

### Fase 4: Documentação ✅
- [x] Documentação técnica
- [x] Documentação de endpoints
- [x] Guias de testes
- [x] Resumo executivo

### Fase 5: Deploy 🔄 (Em andamento)
- [ ] Configurar SonarCloud
- [ ] Deploy Heroku/Railway
- [ ] Collection Postman
- [ ] CI/CD pipeline

---

## 🎓 Para a Apresentação

### Slides Sugeridos

#### Slide 1: Visão Geral
- Nome do projeto
- Tecnologias principais
- 26 endpoints REST

#### Slide 2: Arquitetura
- Diagrama de camadas
- Padrões utilizados (Repository, Singleton)
- FastAPI + TinyDB

#### Slide 3: Funcionalidades
- Gerenciamento de Bicicletas (8 endpoints)
- Gerenciamento de Trancas (11 endpoints)
- Gerenciamento de Totens (5 endpoints)

#### Slide 4: Qualidade
- 123 testes automatizados
- 80.66% de cobertura
- 100% nos routers principais

#### Slide 5: Demo
- Swagger UI ao vivo
- Executar alguns endpoints
- Mostrar relatório de cobertura

---

## 📞 Contatos e Links

### Documentação Adicional
- **FastAPI**: https://fastapi.tiangolo.com/
- **Pydantic**: https://docs.pydantic.dev/
- **TinyDB**: https://tinydb.readthedocs.io/
- **pytest**: https://docs.pytest.org/

### Arquivos Importantes para Apresentação
1. `TESTES_EXECUTIVO_FINAL.md` → Estatísticas de testes
2. `ENDPOINTS_BICICLETA.md` → Documentação de endpoints
3. `ENDPOINTS_TRANCA.md` → Documentação de endpoints
4. `htmlcov/index.html` → Relatório visual de cobertura
5. http://localhost:8000/docs → Swagger UI

---

## ✨ Conclusão

Este projeto demonstra:
- ✅ **Boas práticas de desenvolvimento**
- ✅ **Arquitetura limpa e escalável**
- ✅ **Testes abrangentes e confiáveis**
- ✅ **Documentação completa e profissional**
- ✅ **Pronto para produção**

**Cobertura de testes de 80.66% alcançada!** 🎉

---

*Última atualização: 08/11/2025*  
*Versão: 1.0*
