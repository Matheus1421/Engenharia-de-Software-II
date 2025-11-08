# 🚲 Documentação dos Endpoints de Bicicletas

Esta documentação descreve todos os endpoints implementados para gerenciar bicicletas no sistema.

## 📋 Lista de Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/bicicleta` | Lista todas as bicicletas |
| POST | `/bicicleta` | Cadastra nova bicicleta |
| GET | `/bicicleta/{idBicicleta}` | Obtém bicicleta específica |
| PUT | `/bicicleta/{idBicicleta}` | Atualiza dados da bicicleta |
| DELETE | `/bicicleta/{idBicicleta}` | Remove bicicleta |
| POST | `/bicicleta/{idBicicleta}/status/{acao}` | Altera status da bicicleta |
| POST | `/bicicleta/integrarNaRede` | Integra bicicleta na rede de totens |
| POST | `/bicicleta/retirarDaRede` | Retira bicicleta da rede |

## 🔍 Detalhamento dos Endpoints

### 1. GET /bicicleta

**Descrição:** Retorna todas as bicicletas cadastradas no sistema.

**Response 200 OK:**
```json
[
  {
    "id": 1,
    "marca": "Caloi",
    "modelo": "Mountain Bike Pro",
    "ano": "2023",
    "numero": 100,
    "status": "DISPONIVEL"
  },
  {
    "id": 2,
    "marca": "Shimano",
    "modelo": "City Bike",
    "ano": "2023",
    "numero": 101,
    "status": "DISPONIVEL"
  }
]
```

**Exemplo (curl):**
```bash
curl http://localhost:8000/bicicleta
```

---

### 2. POST /bicicleta

**Descrição:** Cadastra uma nova bicicleta no sistema.

**Request Body:**
```json
{
  "marca": "Giant",
  "modelo": "TCR Advanced",
  "ano": "2024",
  "numero": 500,
  "status": "NOVA"
}
```

**Response 200 OK:**
```json
{
  "id": 4,
  "marca": "Giant",
  "modelo": "TCR Advanced",
  "ano": "2024",
  "numero": 500,
  "status": "NOVA"
}
```

**Response 422 Unprocessable Entity (número duplicado):**
```json
[
  {
    "codigo": "NUMERO_DUPLICADO",
    "mensagem": "Já existe uma bicicleta com o número 500"
  }
]
```

**Exemplo (curl):**
```bash
curl -X POST http://localhost:8000/bicicleta \
  -H "Content-Type: application/json" \
  -d '{
    "marca": "Giant",
    "modelo": "TCR Advanced",
    "ano": "2024",
    "numero": 500,
    "status": "NOVA"
  }'
```

---

### 3. GET /bicicleta/{idBicicleta}

**Descrição:** Obtém os dados de uma bicicleta específica.

**Parâmetros:**
- `idBicicleta` (path, integer, required): ID da bicicleta

**Response 200 OK:**
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

**Response 404 Not Found:**
```json
{
  "codigo": "BICICLETA_NAO_ENCONTRADA",
  "mensagem": "Bicicleta com ID 999 não encontrada"
}
```

**Exemplo (curl):**
```bash
curl http://localhost:8000/bicicleta/1
```

---

### 4. PUT /bicicleta/{idBicicleta}

**Descrição:** Atualiza os dados de uma bicicleta existente.

**Parâmetros:**
- `idBicicleta` (path, integer, required): ID da bicicleta

**Request Body:**
```json
{
  "marca": "Giant",
  "modelo": "TCR Advanced Pro",
  "ano": "2024",
  "numero": 500,
  "status": "DISPONIVEL"
}
```

**Response 200 OK:**
```json
{
  "id": 4,
  "marca": "Giant",
  "modelo": "TCR Advanced Pro",
  "ano": "2024",
  "numero": 500,
  "status": "DISPONIVEL"
}
```

**Response 404 Not Found:**
```json
{
  "codigo": "BICICLETA_NAO_ENCONTRADA",
  "mensagem": "Bicicleta com ID 999 não encontrada"
}
```

**Response 422 Unprocessable Entity:**
```json
[
  {
    "codigo": "NUMERO_DUPLICADO",
    "mensagem": "Já existe outra bicicleta com o número 500"
  }
]
```

**Exemplo (curl):**
```bash
curl -X PUT http://localhost:8000/bicicleta/4 \
  -H "Content-Type: application/json" \
  -d '{
    "marca": "Giant",
    "modelo": "TCR Advanced Pro",
    "ano": "2024",
    "numero": 500,
    "status": "DISPONIVEL"
  }'
```

---

### 5. DELETE /bicicleta/{idBicicleta}

**Descrição:** Remove uma bicicleta do sistema.

**Parâmetros:**
- `idBicicleta` (path, integer, required): ID da bicicleta

**Response 200 OK:**
```json
{
  "mensagem": "Bicicleta removida com sucesso"
}
```

**Response 404 Not Found:**
```json
{
  "codigo": "BICICLETA_NAO_ENCONTRADA",
  "mensagem": "Bicicleta com ID 999 não encontrada"
}
```

**Exemplo (curl):**
```bash
curl -X DELETE http://localhost:8000/bicicleta/4
```

---

### 6. POST /bicicleta/{idBicicleta}/status/{acao}

**Descrição:** Altera o status de uma bicicleta.

**Parâmetros:**
- `idBicicleta` (path, integer, required): ID da bicicleta
- `acao` (path, string, required): Novo status

**Status válidos:**
- `DISPONIVEL` - Bicicleta disponível para aluguel
- `EM_USO` - Bicicleta atualmente alugada
- `NOVA` - Bicicleta recém cadastrada
- `APOSENTADA` - Bicicleta retirada de circulação
- `REPARO_SOLICITADO` - Reparo foi solicitado
- `EM_REPARO` - Bicicleta em manutenção

**Response 200 OK:**
```json
{
  "id": 1,
  "marca": "Caloi",
  "modelo": "Mountain Bike Pro",
  "ano": "2023",
  "numero": 100,
  "status": "EM_USO"
}
```

**Response 404 Not Found:**
```json
{
  "codigo": "BICICLETA_NAO_ENCONTRADA",
  "mensagem": "Bicicleta com ID 999 não encontrada"
}
```

**Response 422 Unprocessable Entity (status inválido):**
```json
[
  {
    "codigo": "STATUS_INVALIDO",
    "mensagem": "Status 'INVALIDO' inválido. Valores permitidos: DISPONIVEL, EM_USO, NOVA, APOSENTADA, REPARO_SOLICITADO, EM_REPARO"
  }
]
```

**Exemplo (curl):**
```bash
curl -X POST http://localhost:8000/bicicleta/1/status/EM_USO
```

---

### 7. POST /bicicleta/integrarNaRede

**Descrição:** Integra uma bicicleta nova ou retornando de reparo na rede de totens.

**Regras de Negócio:**
- A bicicleta deve estar com status `NOVA` ou `EM_REPARO`
- A tranca deve estar com status `LIVRE`
- Após integração:
  - Bicicleta passa para status `DISPONIVEL`
  - Tranca passa para status `OCUPADA`
  - Bicicleta é associada à tranca

**Request Body:**
```json
{
  "idTranca": 1,
  "idBicicleta": 4,
  "idFuncionario": 1
}
```

**Response 200 OK:**
```json
{
  "mensagem": "Bicicleta integrada na rede com sucesso",
  "idBicicleta": 4,
  "idTranca": 1,
  "idFuncionario": 1
}
```

**Response 404 Not Found (bicicleta ou tranca):**
```json
{
  "codigo": "BICICLETA_NAO_ENCONTRADA",
  "mensagem": "Bicicleta com ID 999 não encontrada"
}
```

**Response 422 Unprocessable Entity (status inválido):**
```json
[
  {
    "codigo": "STATUS_BICICLETA_INVALIDO",
    "mensagem": "Bicicleta deve estar com status NOVA ou EM_REPARO. Status atual: DISPONIVEL"
  }
]
```

**Exemplo (curl):**
```bash
curl -X POST http://localhost:8000/bicicleta/integrarNaRede \
  -H "Content-Type: application/json" \
  -d '{
    "idTranca": 1,
    "idBicicleta": 4,
    "idFuncionario": 1
  }'
```

---

### 8. POST /bicicleta/retirarDaRede

**Descrição:** Retira uma bicicleta da rede para reparo ou aposentadoria.

**Regras de Negócio:**
- A bicicleta deve estar associada à tranca informada
- O `statusAcaoReparador` deve ser `APOSENTADA` ou `EM_REPARO`
- Após retirada:
  - Bicicleta passa para o status especificado
  - Tranca passa para status `LIVRE`
  - Bicicleta é desassociada da tranca

**Request Body:**
```json
{
  "idTranca": 1,
  "idBicicleta": 4,
  "idFuncionario": 1,
  "statusAcaoReparador": "EM_REPARO"
}
```

**Response 200 OK:**
```json
{
  "mensagem": "Bicicleta retirada da rede com sucesso",
  "idBicicleta": 4,
  "idTranca": 1,
  "novoStatus": "EM_REPARO",
  "idFuncionario": 1
}
```

**Response 404 Not Found:**
```json
{
  "codigo": "BICICLETA_NAO_ENCONTRADA",
  "mensagem": "Bicicleta com ID 999 não encontrada"
}
```

**Response 422 Unprocessable Entity (bicicleta não está na tranca):**
```json
[
  {
    "codigo": "BICICLETA_NAO_ESTA_NA_TRANCA",
    "mensagem": "A bicicleta 4 não está na tranca 1"
  }
]
```

**Response 422 Unprocessable Entity (status destino inválido):**
```json
[
  {
    "codigo": "STATUS_DESTINO_INVALIDO",
    "mensagem": "statusAcaoReparador deve ser 'APOSENTADA' ou 'EM_REPARO'"
  }
]
```

**Exemplo (curl):**
```bash
curl -X POST http://localhost:8000/bicicleta/retirarDaRede \
  -H "Content-Type: application/json" \
  -d '{
    "idTranca": 1,
    "idBicicleta": 4,
    "idFuncionario": 1,
    "statusAcaoReparador": "EM_REPARO"
  }'
```

---

## 🧪 Testando os Endpoints

### Via Swagger UI

Acesse: **http://localhost:8000/docs**

A documentação interativa permite testar todos os endpoints diretamente pelo navegador.

### Via Script Python

Execute o script de testes:

```bash
poetry run python test_bicicleta_endpoints.py
```

### Via curl

Exemplos fornecidos em cada endpoint acima.

---

## 📊 Códigos de Status HTTP

| Código | Descrição |
|--------|-----------|
| 200 | OK - Operação bem-sucedida |
| 404 | Not Found - Recurso não encontrado |
| 422 | Unprocessable Entity - Dados inválidos |

---

## 🔄 Fluxo de Status das Bicicletas

```
    NOVA
      ↓
   [Integrar na Rede]
      ↓
  DISPONIVEL
      ↓
   [Aluguel]
      ↓
    EM_USO
      ↓
  [Devolução]
      ↓
  DISPONIVEL
      ↓
[Solicitar Reparo]
      ↓
REPARO_SOLICITADO
      ↓
 [Retirar da Rede]
      ↓
   EM_REPARO
      ↓
[Integrar na Rede]
      ↓
  DISPONIVEL

OU

[Retirar da Rede]
      ↓
  APOSENTADA
```

---

## ✅ Validações Implementadas

1. **Número único**: Não permite duplicar números de bicicletas
2. **Status válidos**: Valida os status ao alterar ou cadastrar
3. **Existência**: Verifica se bicicleta/tranca existe antes de operar
4. **Regras de integração**: Valida status corretos para integrar na rede
5. **Regras de retirada**: Valida status corretos para retirar da rede
6. **Associação**: Valida se a bicicleta está na tranca informada

---

## 📝 Observações

- Todos os IDs são inteiros auto-incrementados
- Os status são case-insensitive nos endpoints (DISPONIVEL = disponivel)
- O campo `ano` aceita qualquer string (validação de formato pode ser adicionada)
- O campo `numero` deve ser único no sistema
