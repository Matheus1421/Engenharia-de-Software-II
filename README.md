# 🚲 Sistema de Controle de Bicicletário (SCB)

## 📘 Visão Geral
O **Sistema de Controle de Bicicletário (SCB)** é um projeto desenvolvido no contexto da disciplina **Engenharia de Software II (UNIRIO)**.  
O objetivo é implementar uma **arquitetura de microsserviços** voltada para o controle de bicicletas, totens, trancas, ciclistas e funcionários de um bicicletário público, utilizando **Python + FastAPI**.

---

## 🧩 Estrutura do Repositório

```text
/
├── servico-aluguel/          # YAML com fluxos de trabalho automatizados
├── servico-aluguel/          # Microsserviço responsável por aluguel de bicicletas e gestão de ciclistas/funcionários
├── servico-equipamento/      # Microsserviço responsável por bicicletas, totens e trancas
├── servico-externo/          # Microsserviço responsável por integrações externas (e-mail, cobrança)
├── README.md                 # Este arquivo
└── sonar-project.properties  # Arquivo de Configuração do Sonar
```

Cada pasta de microsserviço contém sua própria estrutura de código, testes e documentação, permitindo **desenvolvimento e implantação independentes**, tudo explicado no README da própria pasta.

---

## 🧠 Visão Geral dos Microsserviços

### 1) `servico-aluguel`
Gerencia **ciclistas, funcionários e operações de aluguel/devolução de bicicletas**.

**Endpoints principais:**
- Cadastro e consulta de ciclistas e funcionários  
- Realização de aluguel e devolução  
- Verificação de permissão para aluguel  

---

### 2) `servico-equipamento`
Gerencia **bicicletas, totens e trancas**.

**Endpoints principais:**
- Cadastro, consulta e atualização de bicicletas, totens e trancas  
- Integração e retirada de equipamentos da rede  
- Alteração de status de equipamentos  

---

### 3) `servico-externo`
Responsável por **integrações externas**, como envio de e-mails e cobranças.

**Endpoints principais:**
- Notificação por e-mail  
- Processamento e consulta de cobranças  
- Validação de cartão de crédito  

---

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologia |
|---|---|
| **Linguagem** | Python 3.10+ |
| **Framework Web** | FastAPI |
| **Testes** | pytest |
| **Gerenciador de Dependências** | Poetry |
| **Revisão Contínua de Código** | SonarCloud / Codacy |
| **Deploy** |Render |
| **Controle de Versão** | GitHub |

---

## ⚙️ Como Executar Localmente

Cada microsserviço pode ser executado de forma independente.  
Exemplo para o **serviço de aluguel**:

```bash
cd servico-aluguel
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 👥 Contribuidores

| Nome | Função |
|---|---|
| **Matheus Marques** | Tech Lead |
| **Alexandre Vidal** | Dev - Aluguel|
| **Camilo Lima** | Dev - Externo |
| **Alexandre Vidal** | Dev - Equipamento |
