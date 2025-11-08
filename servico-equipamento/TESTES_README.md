# Testes Unitários - Serviço de Equipamentos

## 📋 Visão Geral

Este documento descreve a estrutura de testes unitários implementada para o microsserviço de equipamentos, seguindo as melhores práticas de desenvolvimento e os requisitos do projeto.

## 🎯 Objetivos dos Testes

- ✅ **Cobertura mínima de 80%**: Todos os endpoints possuem testes abrangentes
- ✅ **Testes unitários**: Escopo de método com uso de mocks
- ✅ **Cenários de sucesso e erro**: Cobertura completa de casos de uso
- ✅ **Isolamento**: Uso de mocks para simular dependências (banco de dados, repositórios)

## 📁 Estrutura de Testes

```
tests/
├── conftest.py                    # Configurações globais do pytest
├── test_status_endpoint.py        # Testes do endpoint de status (1 teste)
├── test_bicicleta_endpoints.py    # Testes dos endpoints de bicicletas (33 testes)
└── test_totem_endpoints.py        # Testes dos endpoints de totens (36 testes)
```

**Total: 70 testes unitários** ✅

## 🧪 Testes de Bicicletas

### Arquivo: `test_bicicleta_endpoints.py`

**Cobertura Atual: 100%** ✅

### Endpoints Testados

#### 1. GET /bicicleta
- ✅ Listagem com sucesso (múltiplas bicicletas)
- ✅ Lista vazia (nenhuma bicicleta cadastrada)

#### 2. POST /bicicleta
- ✅ Cadastro com sucesso
- ✅ Erro: Número duplicado
- ✅ Erro: Dados inválidos
- ✅ Erro: Campos obrigatórios faltando
- ✅ Exceção genérica

#### 3. GET /bicicleta/{id}
- ✅ Obtenção com sucesso
- ✅ Erro: Bicicleta não encontrada

#### 4. PUT /bicicleta/{id}
- ✅ Edição com sucesso
- ✅ Erro: Bicicleta não encontrada
- ✅ Erro: Número duplicado
- ✅ Exceção genérica

#### 5. DELETE /bicicleta/{id}
- ✅ Remoção com sucesso
- ✅ Erro: Bicicleta não encontrada

#### 6. POST /bicicleta/{id}/status/{acao}
- ✅ Alteração de status com sucesso
- ✅ Teste de todos os 6 status válidos
- ✅ Erro: Status inválido
- ✅ Erro: Bicicleta não encontrada
- ✅ Case insensitive (aceita minúsculas)

#### 7. POST /bicicleta/integrarNaRede
- ✅ Integração com status NOVA (sucesso)
- ✅ Integração com status EM_REPARO (sucesso)
- ✅ Erro: Bicicleta não encontrada
- ✅ Erro: Tranca não encontrada
- ✅ Erro: Status da bicicleta inválido
- ✅ Erro: Tranca ocupada

#### 8. POST /bicicleta/retirarDaRede
- ✅ Retirada para reparo (sucesso)
- ✅ Retirada para aposentadoria (sucesso)
- ✅ Erro: Bicicleta não encontrada
- ✅ Erro: Tranca não encontrada
- ✅ Erro: Bicicleta não está na tranca
- ✅ Erro: Status de destino inválido
- ✅ Case insensitive

## 🚀 Como Executar os Testes

### 1. Executar todos os testes

```bash
poetry run pytest
```

### 2. Executar testes de bicicletas com cobertura

```bash
poetry run pytest tests/test_bicicleta_endpoints.py -v --cov=routers.bicicleta --cov-report=term-missing
```

### 3. Executar todos os testes com cobertura geral

```bash
poetry run pytest --cov=. --cov-report=term-missing --cov-report=html
```

O relatório HTML será gerado em `htmlcov/index.html`.

### 4. Executar testes em modo verboso

```bash
poetry run pytest -v
```

### 5. Executar teste específico

```bash
poetry run pytest tests/test_bicicleta_endpoints.py::test_listar_bicicletas_sucesso -v
```

### 6. Executar testes com output de print

```bash
poetry run pytest -s
```

## 📊 Relatório de Cobertura

### Visualizar cobertura no terminal
```bash
poetry run pytest --cov=routers --cov-report=term
```

### Gerar relatório HTML
```bash
poetry run pytest --cov=routers --cov-report=html
```

Abra `htmlcov/index.html` no navegador para visualizar o relatório interativo.

## 🔧 Tecnologias Utilizadas

- **pytest**: Framework de testes
- **pytest-cov**: Plugin para cobertura de código
- **pytest-mock**: Plugin para mocking
- **httpx**: Cliente HTTP para testes de API
- **unittest.mock**: Biblioteca de mocking do Python

## 📝 Padrões de Teste

### 1. Uso de Fixtures

```python
@pytest.fixture
def bicicleta_exemplo():
    """Bicicleta de exemplo para testes"""
    return Bicicleta(
        id=1,
        marca="Caloi",
        modelo="Mountain Bike",
        ano="2023",
        numero=100,
        status=StatusBicicleta.DISPONIVEL
    )
```

### 2. Uso de Mocks

```python
with patch('routers.bicicleta.get_db'), \
     patch('routers.bicicleta.BicicletaRepository') as mock_repo:
    
    mock_repo_instance = Mock()
    mock_repo.return_value = mock_repo_instance
    mock_repo_instance.get_all.return_value = [...]
    
    response = client.get("/bicicleta")
```

### 3. Asserções

```python
assert response.status_code == 200
assert len(response.json()) == 2
assert "ERRO_CODIGO" in str(response.json())
mock_repo_instance.get_all.assert_called_once()
```

## ✅ Checklist de Qualidade

- [x] Testes unitários com cobertura de 80%+ 
- [x] Uso de mocks para isolamento
- [x] Testes de cenários de sucesso
- [x] Testes de cenários de erro (404, 422)
- [x] Testes de validações
- [x] Testes de edge cases
- [x] Documentação dos testes
- [ ] Integração com SonarCloud (próxima etapa)
- [ ] Integração com CI/CD (próxima etapa)

## 🎯 Próximas Etapas

1. ✅ **Testes de Bicicletas** - CONCLUÍDO (100% cobertura - 33 testes)
2. ✅ **Testes de Totens** - CONCLUÍDO (100% cobertura - 36 testes)
3. ⏳ **Testes de Trancas** - Pendente (~40 testes estimados)
4. ⏳ **Testes de Repositórios** - Pendente
5. ⏳ **Testes de Integração** - Pendente

## 📚 Referências

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Python Mock Documentation](https://docs.python.org/3/library/unittest.mock.html)

## 🐛 Troubleshooting

### Erro: ModuleNotFoundError
```bash
# Sempre use poetry run antes dos comandos
poetry run pytest
```

### Erro: Database file locked
```bash
# Pare o servidor antes de rodar os testes
# Os testes usam mocks e não acessam o DB real
```

### Cobertura baixa
```bash
# Verifique quais linhas não estão cobertas
poetry run pytest --cov=routers --cov-report=term-missing
```

## 📞 Suporte

Para dúvidas sobre os testes, consulte:
- A documentação do pytest
- Os exemplos nos arquivos de teste
- O arquivo `conftest.py` para configurações globais
