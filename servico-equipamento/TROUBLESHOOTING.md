# 🔧 Guia de Troubleshooting - Resolvendo Erros

## 🐍 Problema: Você está usando Python 3.13

O contexto mostra que você está usando:
```
C:/Users/User/AppData/Local/Programs/Python/Python313/python.exe
```

O projeto foi configurado para **Python 3.11+**. Python 3.13 pode ter problemas de compatibilidade com algumas bibliotecas.

### ✅ Solução Recomendada

**Use o Poetry para gerenciar tudo:**

```powershell
cd c:\TrabalhoES2\Engenharia-de-Software-II\servico-equipamento
poetry install
poetry run python exemplo_banco.py
```

O Poetry vai criar um ambiente virtual com a versão correta do Python (3.11 ou 3.12) e instalar todas as dependências compatíveis.

## 🚨 Erros Comuns e Soluções

### Erro 1: `ModuleNotFoundError: No module named 'tinydb'`

**Causa:** Você está executando com Python global ao invés do ambiente virtual do Poetry.

**Solução:**
```powershell
# Sempre use poetry run
poetry run python exemplo_banco.py

# OU ative o ambiente virtual primeiro
poetry shell
python exemplo_banco.py
```

### Erro 2: `Import "tinydb" could not be resolved` (no editor)

**Causa:** VS Code não está usando o interpretador Python correto.

**Solução:**
1. Abra a Paleta de Comandos: `Ctrl + Shift + P`
2. Digite: `Python: Select Interpreter`
3. Escolha o interpretador do Poetry (procure por algo como: `.venv\Scripts\python.exe` ou `Poetry (servico-equipamento)`)

### Erro 3: `poetry: command not found`

**Causa:** Poetry não está instalado ou não está no PATH.

**Solução (Windows PowerShell):**
```powershell
# Instalar Poetry
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Adicionar ao PATH (reinicie o PowerShell depois)
$env:Path += ";$env:APPDATA\Python\Scripts"
```

**Verificar instalação:**
```powershell
poetry --version
```

### Erro 4: `pyproject.toml changed significantly`

**Causa:** O arquivo de lock do Poetry está desatualizado.

**Solução:**
```powershell
poetry lock
poetry install
```

### Erro 5: Erro ao executar `main.py` diretamente

**Causa:** Você está tentando executar `python main.py` ao invés de usar o uvicorn.

**Solução:**
```powershell
# ❌ Errado
poetry run python main.py

# ✅ Correto
poetry run uvicorn main:app --reload
```

### Erro 6: `SyntaxError` ou problemas com enums

**Causa:** Pode ser incompatibilidade com Python 3.13.

**Solução 1 - Força Python 3.11 ou 3.12:**
```powershell
# Se você tem Python 3.11 ou 3.12 instalado
poetry env use python3.11
poetry install
```

**Solução 2 - Atualizar pyproject.toml para aceitar 3.13:**
Edite o `pyproject.toml` e mude:
```toml
python = "^3.11"
```
Para:
```toml
python = ">=3.11,<3.14"
```

Depois:
```powershell
poetry lock
poetry install
```

## 🧪 Verificar se está tudo funcionando

Execute estes comandos em ordem:

```powershell
# 1. Navegar para o diretório
cd c:\TrabalhoES2\Engenharia-de-Software-II\servico-equipamento

# 2. Verificar versão do Poetry
poetry --version

# 3. Verificar qual Python o Poetry está usando
poetry env info

# 4. Instalar/atualizar dependências
poetry install

# 5. Testar o exemplo
poetry run python exemplo_banco.py

# 6. Iniciar o servidor
poetry run uvicorn main:app --reload
```

**Saída esperada do passo 3:**
```
Virtualenv
Python:         3.11.x (ou 3.12.x)
Implementation: CPython
Path:           C:\Users\User\AppData\Local\pypoetry\Cache\virtualenvs\...
```

## 📝 Checklist de Diagnóstico

Execute cada comando e anote o resultado:

- [ ] `poetry --version` → Deve mostrar a versão do Poetry
- [ ] `poetry env info` → Deve mostrar Python 3.11 ou 3.12
- [ ] `poetry install` → Deve instalar sem erros
- [ ] `poetry run python --version` → Deve mostrar a versão do Python no ambiente virtual
- [ ] `poetry run python -c "import tinydb; print('OK')"` → Deve imprimir "OK"
- [ ] `poetry run python exemplo_banco.py` → Deve executar sem erros

Se todos os checkboxes acima passarem, o ambiente está configurado corretamente! ✅

## 🆘 Ainda com problemas?

Se nada disso resolver, forneça as seguintes informações:

1. **Saída do comando:**
   ```powershell
   poetry env info
   ```

2. **Erro completo** (copie toda a mensagem de erro)

3. **O que você tentou executar:**
   ```powershell
   # Cole aqui o comando que você executou
   ```

4. **Versão do Python:**
   ```powershell
   python --version
   poetry run python --version
   ```

## 💡 Dicas Importantes

1. **SEMPRE use `poetry run`** antes de comandos Python neste projeto
2. **NÃO tente instalar** as dependências com `pip install` globalmente
3. **Use o ambiente virtual** do Poetry para tudo relacionado a este projeto
4. **Se editar pyproject.toml**, sempre execute `poetry lock` depois

---

**Lembre-se:** O Poetry gerencia tudo! Confie nele e use `poetry run`. 🚀
