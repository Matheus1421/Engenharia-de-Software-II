# ⚠️ Como Executar os Scripts Corretamente

## ❌ Problema Comum

Se você está recebendo erro ao executar o script `exemplo_banco.py`, provavelmente está tentando executar diretamente com Python ao invés de usar o Poetry:

```bash
# ❌ ERRADO - Não funciona
python exemplo_banco.py
```

**Erro esperado:**
```
ModuleNotFoundError: No module named 'tinydb'
# ou
ModuleNotFoundError: No module named 'pydantic'
```

## ✅ Solução

O projeto usa **Poetry** para gerenciar dependências. Você **DEVE** executar os scripts através do Poetry:

```bash
# ✅ CORRETO - Use isso
poetry run python exemplo_banco.py
```

## 🔍 Por que isso acontece?

O Poetry cria um ambiente virtual isolado com todas as dependências instaladas (TinyDB, FastAPI, Pydantic, etc.). Quando você executa com `poetry run`, ele ativa automaticamente esse ambiente.

Quando você tenta executar com Python diretamente, ele usa o Python global do sistema, que não tem essas dependências instaladas.

## 📋 Comandos Corretos para Executar os Scripts

### 1. Executar o exemplo do banco de dados
```bash
cd c:\TrabalhoES2\Engenharia-de-Software-II\servico-equipamento
poetry run python exemplo_banco.py
```

### 2. Iniciar o servidor FastAPI
```bash
cd c:\TrabalhoES2\Engenharia-de-Software-II\servico-equipamento
poetry run uvicorn main:app --reload
```

### 3. Executar testes
```bash
cd c:\TrabalhoES2\Engenharia-de-Software-II\servico-equipamento
poetry run pytest
```

## 🔧 Alternativa: Ativar o Ambiente Virtual Manualmente

Se você preferir não usar `poetry run` toda vez, pode ativar o ambiente virtual:

### No Windows PowerShell:
```powershell
cd c:\TrabalhoES2\Engenharia-de-Software-II\servico-equipamento
poetry shell
```

Depois disso, você pode executar os scripts normalmente:
```powershell
python exemplo_banco.py
python main.py
```

Para sair do ambiente virtual:
```powershell
exit
```

### No Windows CMD:
```cmd
cd c:\TrabalhoES2\Engenharia-de-Software-II\servico-equipamento
poetry shell
```

## 🐛 Ainda com problemas?

### Erro: "Poetry not found" ou "poetry não reconhecido"
Você precisa instalar o Poetry primeiro:
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### Erro: "No pyproject.toml found"
Certifique-se de estar no diretório correto:
```powershell
cd c:\TrabalhoES2\Engenharia-de-Software-II\servico-equipamento
```

### Erro: "Dependencies not installed"
Instale as dependências:
```powershell
poetry install
```

## 📝 Resumo Rápido

| ❌ Não Funciona | ✅ Funciona |
|----------------|------------|
| `python exemplo_banco.py` | `poetry run python exemplo_banco.py` |
| `python main.py` | `poetry run uvicorn main:app --reload` |
| `pytest` | `poetry run pytest` |

## 💡 Dica para VS Code

Se você usa VS Code, pode configurar o interpretador Python para usar o ambiente virtual do Poetry:

1. Pressione `Ctrl + Shift + P`
2. Digite "Python: Select Interpreter"
3. Escolha o interpretador do Poetry (geralmente algo como `.venv\Scripts\python.exe`)

Depois disso, você pode executar scripts diretamente pelo VS Code usando o botão "Run" ▶️.

---

**Lembre-se:** Sempre use `poetry run` antes dos comandos Python quando estiver trabalhando com este projeto! 🚀
