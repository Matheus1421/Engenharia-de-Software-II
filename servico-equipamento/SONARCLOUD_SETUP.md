# 🔍 Configuração do SonarCloud

## 📋 Pré-requisitos

- Conta no [SonarCloud](https://sonarcloud.io)
- Repositório no GitHub/GitLab
- Acesso administrativo ao repositório

## 🚀 Passo a Passo

### 1. Criar Conta no SonarCloud

1. Acesse https://sonarcloud.io
2. Faça login com GitHub/GitLab/Bitbucket
3. Autorize o SonarCloud a acessar seus repositórios

### 2. Adicionar Projeto

1. Clique em **"+"** no canto superior direito
2. Selecione **"Analyze new project"**
3. Escolha a organização (es220252)
4. Selecione o repositório **Engenharia-de-Software-II**
5. Clique em **"Set Up"**

### 3. Configurar o Projeto

#### Arquivo: `sonar-project.properties`

```properties
# Organization and project keys
sonar.organization=es220252
sonar.projectKey=Engenharia-de-Software-II

# Project info
sonar.projectName=Sistema de Bicicletário - Equipamentos
sonar.projectVersion=1.0

# Source code location
sonar.sources=servico-equipamento
sonar.tests=servico-equipamento/tests

# Exclusions
sonar.exclusions=**/__pycache__/**,**/venv/**,**/htmlcov/**,**/.pytest_cache/**,**/exemplo_banco.py,**/test_*.py

# Test exclusions
sonar.test.exclusions=**/tests/**,**/test_*.py

# Python coverage
sonar.python.coverage.reportPaths=servico-equipamento/coverage.xml

# Language
sonar.language=py
sonar.sourceEncoding=UTF-8

# Coverage exclusions (não analisar testes)
sonar.coverage.exclusions=**/tests/**,**/test_*.py,**/conftest.py
```

### 4. Gerar Relatório de Cobertura em XML

```bash
# No diretório servico-equipamento
poetry run pytest --cov=. --cov-report=xml --cov-report=term
```

Isso gera o arquivo `coverage.xml` que o SonarCloud usa.

### 5. Configurar GitHub Actions (CI/CD)

Crie o arquivo `.github/workflows/sonarcloud.yml`:

```yaml
name: SonarCloud Analysis

on:
  push:
    branches:
      - main
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  sonarcloud:
    name: SonarCloud
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Shallow clones should be disabled for better analysis
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -
          echo "$HOME/.local/bin" >> $GITHUB_PATH
      
      - name: Install dependencies
        working-directory: servico-equipamento
        run: |
          poetry install
      
      - name: Run tests with coverage
        working-directory: servico-equipamento
        run: |
          poetry run pytest --cov=. --cov-report=xml --cov-report=term
      
      - name: SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### 6. Adicionar Token do SonarCloud ao GitHub

1. No SonarCloud, vá em **My Account** → **Security**
2. Gere um novo token
3. No GitHub, vá em **Settings** → **Secrets and variables** → **Actions**
4. Adicione um novo secret: `SONAR_TOKEN` com o valor do token

## 📊 Métricas do SonarCloud

### Objetivos do Projeto

| Métrica | Meta | Status |
|---------|------|--------|
| Bugs | 0 | ⏳ |
| Vulnerabilities | 0 | ⏳ |
| Code Smells (Blocker) | 0 | ⏳ |
| Code Smells (Critical) | 0 | ⏳ |
| Code Smells (Major) | 0 | ⏳ |
| Coverage | ≥ 80% | ✅ (100% bicicletas) |
| Duplicação | < 1% | ⏳ |

## 🛠️ Executar Análise Local

### Instalar SonarScanner

```bash
# Windows (usando Chocolatey)
choco install sonarscanner

# Linux/Mac (usando Homebrew)
brew install sonar-scanner
```

### Executar Scanner Localmente

```bash
# No diretório raiz do projeto
sonar-scanner \
  -Dsonar.organization=es220252 \
  -Dsonar.projectKey=Engenharia-de-Software-II \
  -Dsonar.sources=servico-equipamento \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.login=SEU_TOKEN_AQUI
```

## 📈 Melhorar Qualidade do Código

### Corrigir Code Smells

```bash
# Usar ferramentas de linting
poetry add --group dev pylint black isort mypy

# Executar formatação
poetry run black servico-equipamento
poetry run isort servico-equipamento

# Executar linting
poetry run pylint servico-equipamento
```

### Aumentar Cobertura

```bash
# Ver relatório detalhado
poetry run pytest --cov=. --cov-report=html
# Abrir: htmlcov/index.html

# Identificar código não coberto
poetry run pytest --cov=. --cov-report=term-missing
```

## 🎯 Quality Gate

### Configuração Recomendada

- **New Code Coverage**: ≥ 80%
- **Duplicated Lines**: ≤ 1%
- **Maintainability Rating**: A
- **Reliability Rating**: A
- **Security Rating**: A

## 📝 Boas Práticas

### 1. Commits Frequentes
- Commit após cada feature
- Mensagens descritivas
- Referenciar issues quando aplicável

### 2. Pull Requests
- Criar PR para cada feature
- Aguardar análise do SonarCloud
- Corrigir issues antes de merge

### 3. Monitoramento
- Verificar dashboard diariamente
- Corrigir issues críticos imediatamente
- Manter métricas verdes

## 🔧 Troubleshooting

### Erro: "No coverage report found"
```bash
# Certifique-se de gerar coverage.xml
poetry run pytest --cov=. --cov-report=xml
```

### Erro: "Authentication failed"
```bash
# Verifique se o SONAR_TOKEN está correto
# Regenere o token se necessário
```

### Erro: "Project not found"
```bash
# Verifique sonar.projectKey em sonar-project.properties
# Confirme que o projeto existe no SonarCloud
```

## 📚 Recursos

- [SonarCloud Documentation](https://docs.sonarcloud.io/)
- [Python Coverage](https://coverage.readthedocs.io/)
- [Quality Gate Docs](https://docs.sonarcloud.io/improving/quality-gates/)

## ✅ Checklist

- [ ] Conta criada no SonarCloud
- [ ] Projeto configurado
- [ ] sonar-project.properties criado
- [ ] Token adicionado ao GitHub
- [ ] GitHub Actions configurado
- [ ] Primeira análise executada
- [ ] Métricas verificadas
- [ ] Quality Gate configurado

---

**Próximos Passos**: Após configurar o SonarCloud, trabalhar para atingir todas as métricas de qualidade.
