# Endpoints de Trancas - Documentação

Este documento descreve todos os endpoints implementados para o gerenciamento de trancas no sistema de bicicletário.

## Índice
- [Listar Trancas](#listar-trancas)
- [Cadastrar Tranca](#cadastrar-tranca)
- [Obter Tranca](#obter-tranca)
- [Editar Tranca](#editar-tranca)
- [Remover Tranca](#remover-tranca)
- [Obter Bicicleta na Tranca](#obter-bicicleta-na-tranca)
- [Trancar](#trancar)
- [Destrancar](#destrancar)
- [Alterar Status](#alterar-status)
- [Integrar na Rede](#integrar-na-rede)
- [Retirar da Rede](#retirar-da-rede)

---

## Listar Trancas

**GET** `/tranca`

Lista todas as trancas cadastradas no sistema.

### Response
- **200 OK**: Lista de trancas
```json
[
  {
    "id": 1,
    "numero": 1,
    "localizacao": "-22.9068,-43.1729",
    "anoDeFabricacao": "2023",
    "modelo": "Modelo X1",
    "status": "LIVRE",
    "bicicleta": null
  }
]
```

---

## Cadastrar Tranca

**POST** `/tranca`

Cadastra uma nova tranca no sistema.

### Request Body
```json
{
  "numero": 1,
  "localizacao": "-22.9068,-43.1729",
  "anoDeFabricacao": "2023",
  "modelo": "Modelo X1",
  "status": "NOVA"
}
```

### Validações
- `numero` deve ser positivo e único
- `localizacao` deve estar em formato de coordenadas
- `anoDeFabricacao` deve ser um ano válido
- `status` deve ser um dos valores: LIVRE, OCUPADA, NOVA, APOSENTADA, EM_REPARO

### Response
- **200 OK**: Tranca cadastrada
```json
{
  "id": 1,
  "numero": 1,
  "localizacao": "-22.9068,-43.1729",
  "anoDeFabricacao": "2023",
  "modelo": "Modelo X1",
  "status": "NOVA",
  "bicicleta": null
}
```

- **422 Unprocessable Entity**: Dados inválidos
```json
[
  {
    "codigo": "NUMERO_DUPLICADO",
    "mensagem": "Já existe uma tranca com o número 1"
  }
]
```

---

## Obter Tranca

**GET** `/tranca/{idTranca}`

Obtém os dados de uma tranca específica.

### Path Parameters
- `idTranca` (integer): ID da tranca

### Response
- **200 OK**: Tranca encontrada
```json
{
  "id": 1,
  "numero": 1,
  "localizacao": "-22.9068,-43.1729",
  "anoDeFabricacao": "2023",
  "modelo": "Modelo X1",
  "status": "LIVRE",
  "bicicleta": null
}
```

- **404 Not Found**: Tranca não encontrada
```json
{
  "codigo": "TRANCA_NAO_ENCONTRADA",
  "mensagem": "Tranca com ID 1 não encontrada"
}
```

---

## Editar Tranca

**PUT** `/tranca/{idTranca}`

Atualiza os dados de uma tranca existente.

### Path Parameters
- `idTranca` (integer): ID da tranca

### Request Body
```json
{
  "numero": 1,
  "localizacao": "-22.9068,-43.1729",
  "anoDeFabricacao": "2023",
  "modelo": "Modelo X2",
  "status": "LIVRE"
}
```

### Response
- **200 OK**: Tranca atualizada
- **404 Not Found**: Tranca não encontrada
- **422 Unprocessable Entity**: Dados inválidos

---

## Remover Tranca

**DELETE** `/tranca/{idTranca}`

Remove uma tranca do sistema.

### Path Parameters
- `idTranca` (integer): ID da tranca

### Response
- **200 OK**: Tranca removida
```json
{
  "mensagem": "Tranca removida com sucesso"
}
```

- **404 Not Found**: Tranca não encontrada
```json
{
  "codigo": "TRANCA_NAO_ENCONTRADA",
  "mensagem": "Tranca com ID 1 não encontrada"
}
```

---

## Obter Bicicleta na Tranca

**GET** `/tranca/{idTranca}/bicicleta`

Obtém a bicicleta associada a uma tranca.

### Path Parameters
- `idTranca` (integer): ID da tranca

### Response
- **200 OK**: Bicicleta encontrada
```json
{
  "id": 1,
  "marca": "Caloi",
  "modelo": "Mountain Bike",
  "ano": "2023",
  "numero": 101,
  "status": "DISPONIVEL"
}
```

- **404 Not Found**: Tranca ou bicicleta não encontrada
```json
{
  "codigo": "BICICLETA_NAO_ENCONTRADA",
  "mensagem": "Não há bicicleta na tranca 1"
}
```

- **422 Unprocessable Entity**: ID inválido
```json
{
  "codigo": "ID_INVALIDO",
  "mensagem": "O ID da tranca deve ser um número positivo"
}
```

---

## Trancar

**POST** `/tranca/{idTranca}/trancar`

Realiza o trancamento da tranca. Opcionalmente associa uma bicicleta à tranca.

### Path Parameters
- `idTranca` (integer): ID da tranca

### Request Body (Opcional)
```json
{
  "bicicleta": 1
}
```

### Comportamento
1. Se `bicicleta` for fornecido:
   - Associa a bicicleta à tranca
   - Atualiza status da bicicleta para DISPONIVEL
2. Atualiza status da tranca para OCUPADA

### Response
- **200 OK**: Tranca trancada
```json
{
  "id": 1,
  "numero": 1,
  "localizacao": "-22.9068,-43.1729",
  "anoDeFabricacao": "2023",
  "modelo": "Modelo X1",
  "status": "OCUPADA",
  "bicicleta": 1
}
```

- **404 Not Found**: Tranca ou bicicleta não encontrada
- **422 Unprocessable Entity**: Tranca já trancada
```json
[
  {
    "codigo": "TRANCA_JA_TRANCADA",
    "mensagem": "A tranca 1 já está trancada"
  }
]
```

---

## Destrancar

**POST** `/tranca/{idTranca}/destrancar`

Realiza o destrancamento da tranca. Opcionalmente desassocia uma bicicleta da tranca.

### Path Parameters
- `idTranca` (integer): ID da tranca

### Request Body (Opcional)
```json
{
  "bicicleta": 1
}
```

### Comportamento
1. Se `bicicleta` for fornecido:
   - Verifica se a bicicleta está na tranca
   - Desassocia a bicicleta da tranca
   - Atualiza status da bicicleta para EM_USO
2. Atualiza status da tranca para LIVRE

### Response
- **200 OK**: Tranca destrancada
```json
{
  "id": 1,
  "numero": 1,
  "localizacao": "-22.9068,-43.1729",
  "anoDeFabricacao": "2023",
  "modelo": "Modelo X1",
  "status": "LIVRE",
  "bicicleta": null
}
```

- **404 Not Found**: Tranca ou bicicleta não encontrada
- **422 Unprocessable Entity**: Bicicleta não está na tranca
```json
[
  {
    "codigo": "BICICLETA_NAO_ESTA_NA_TRANCA",
    "mensagem": "A bicicleta 1 não está na tranca 1"
  }
]
```

---

## Alterar Status

**POST** `/tranca/{idTranca}/status/{acao}`

Altera o status de uma tranca (TRANCAR ou DESTRANCAR).

### Path Parameters
- `idTranca` (integer): ID da tranca
- `acao` (string): Ação a ser realizada (TRANCAR ou DESTRANCAR)

### Ações Válidas
- **TRANCAR**: Altera status para OCUPADA
- **DESTRANCAR**: Altera status para LIVRE

### Response
- **200 OK**: Status alterado
```json
{
  "id": 1,
  "numero": 1,
  "localizacao": "-22.9068,-43.1729",
  "anoDeFabricacao": "2023",
  "modelo": "Modelo X1",
  "status": "OCUPADA",
  "bicicleta": null
}
```

- **404 Not Found**: Tranca não encontrada
- **422 Unprocessable Entity**: Ação inválida
```json
[
  {
    "codigo": "ACAO_INVALIDA",
    "mensagem": "Ação 'INVALIDA' inválida. Valores permitidos: TRANCAR, DESTRANCAR"
  }
]
```

---

## Integrar na Rede

**POST** `/tranca/integrarNaRede`

Coloca uma tranca nova ou retornando de reparo de volta na rede de totems.

### Request Body
```json
{
  "idTotem": 1,
  "idTranca": 1,
  "idFuncionario": 1
}
```

### Validações
- Tranca deve existir
- Totem deve existir
- Tranca deve estar com status NOVA ou EM_REPARO

### Comportamento
1. Associa tranca ao totem
2. Atualiza status da tranca para LIVRE

### Response
- **200 OK**: Tranca integrada
```json
{
  "mensagem": "Tranca integrada na rede com sucesso",
  "idTranca": 1,
  "idTotem": 1,
  "idFuncionario": 1
}
```

- **404 Not Found**: Tranca ou totem não encontrado
- **422 Unprocessable Entity**: Status inválido
```json
[
  {
    "codigo": "STATUS_TRANCA_INVALIDO",
    "mensagem": "Tranca deve estar com status NOVA ou EM_REPARO. Status atual: LIVRE"
  }
]
```

---

## Retirar da Rede

**POST** `/tranca/retirarDaRede`

Retira uma tranca para reparo ou aposentadoria.

### Request Body
```json
{
  "idTotem": 1,
  "idTranca": 1,
  "idFuncionario": 1,
  "statusAcaoReparador": "EM_REPARO"
}
```

### Validações
- Tranca deve existir
- Totem deve existir
- Tranca deve estar no totem informado
- `statusAcaoReparador` deve ser 'APOSENTADA' ou 'EM_REPARO'

### Comportamento
1. Atualiza status da tranca para o status informado
2. Desassocia tranca do totem

### Response
- **200 OK**: Tranca retirada
```json
{
  "mensagem": "Tranca retirada da rede com sucesso",
  "idTranca": 1,
  "idTotem": 1,
  "novoStatus": "EM_REPARO",
  "idFuncionario": 1
}
```

- **404 Not Found**: Tranca ou totem não encontrado
- **422 Unprocessable Entity**: Dados inválidos
```json
[
  {
    "codigo": "TRANCA_NAO_ESTA_NO_TOTEM",
    "mensagem": "A tranca 1 não está no totem 1"
  }
]
```

---

## Status de Trancas

### Estados Possíveis
- **LIVRE**: Tranca disponível, sem bicicleta
- **OCUPADA**: Tranca com bicicleta
- **NOVA**: Tranca recém-cadastrada, não integrada
- **APOSENTADA**: Tranca fora de operação permanentemente
- **EM_REPARO**: Tranca em manutenção

### Transições de Estado Válidas

```
NOVA -> LIVRE (via integrarNaRede)
LIVRE -> OCUPADA (via trancar)
OCUPADA -> LIVRE (via destrancar)
LIVRE -> EM_REPARO (via retirarDaRede)
LIVRE -> APOSENTADA (via retirarDaRede)
EM_REPARO -> LIVRE (via integrarNaRede)
```

---

## Exemplos de Uso

### 1. Cadastrar e Integrar Nova Tranca

```bash
# 1. Cadastrar tranca
curl -X POST http://localhost:8000/tranca \
  -H "Content-Type: application/json" \
  -d '{
    "numero": 10,
    "localizacao": "-22.9068,-43.1729",
    "anoDeFabricacao": "2024",
    "modelo": "Modelo X1",
    "status": "NOVA"
  }'

# 2. Integrar na rede
curl -X POST http://localhost:8000/tranca/integrarNaRede \
  -H "Content-Type: application/json" \
  -d '{
    "idTotem": 1,
    "idTranca": 10,
    "idFuncionario": 1
  }'
```

### 2. Ciclo de Aluguel (Destrancar e Trancar)

```bash
# 1. Destrancar para retirada
curl -X POST http://localhost:8000/tranca/1/destrancar \
  -H "Content-Type: application/json" \
  -d '{
    "bicicleta": 1
  }'

# 2. Trancar na devolução
curl -X POST http://localhost:8000/tranca/1/trancar \
  -H "Content-Type: application/json" \
  -d '{
    "bicicleta": 1
  }'
```

### 3. Enviar Tranca para Reparo

```bash
# 1. Retirar da rede
curl -X POST http://localhost:8000/tranca/retirarDaRede \
  -H "Content-Type: application/json" \
  -d '{
    "idTotem": 1,
    "idTranca": 1,
    "idFuncionario": 1,
    "statusAcaoReparador": "EM_REPARO"
  }'

# 2. Após reparo, integrar novamente
curl -X POST http://localhost:8000/tranca/integrarNaRede \
  -H "Content-Type: application/json" \
  -d '{
    "idTotem": 1,
    "idTranca": 1,
    "idFuncionario": 1
  }'
```

---

## Regras de Negócio

### Associação Tranca-Bicicleta
- Uma tranca pode ter no máximo uma bicicleta
- Uma bicicleta pode estar em no máximo uma tranca
- Ao trancar com bicicleta, a bicicleta fica DISPONIVEL
- Ao destrancar com bicicleta, a bicicleta fica EM_USO

### Associação Tranca-Totem
- Uma tranca pode estar em no máximo um totem
- Um totem pode ter múltiplas trancas
- Ao integrar na rede, a tranca é associada ao totem
- Ao retirar da rede, a associação é removida

### Validações de Status
- Não é possível trancar uma tranca já trancada
- Integrar na rede só é permitido para trancas NOVA ou EM_REPARO
- Retirar da rede requer que a tranca esteja no totem informado

---

## Códigos de Erro

| Código | Descrição |
|--------|-----------|
| TRANCA_NAO_ENCONTRADA | Tranca com ID especificado não existe |
| BICICLETA_NAO_ENCONTRADA | Bicicleta especificada não existe ou não está na tranca |
| TOTEM_NAO_ENCONTRADO | Totem especificado não existe |
| NUMERO_DUPLICADO | Já existe tranca com o número informado |
| ID_INVALIDO | ID fornecido é inválido (ex: negativo, zero) |
| TRANCA_JA_TRANCADA | Tentativa de trancar uma tranca já trancada |
| BICICLETA_NAO_ESTA_NA_TRANCA | Bicicleta especificada não está na tranca |
| STATUS_TRANCA_INVALIDO | Status atual da tranca não permite a operação |
| TRANCA_NAO_ESTA_NO_TOTEM | Tranca não está associada ao totem informado |
| STATUS_DESTINO_INVALIDO | Status de destino inválido para retirada da rede |
| ACAO_INVALIDA | Ação de status não é TRANCAR nem DESTRANCAR |
| DADOS_INVALIDOS | Erro genérico de validação de dados |

---

## Total de Endpoints

✅ **11 endpoints implementados:**

1. GET `/tranca` - Listar trancas
2. POST `/tranca` - Cadastrar tranca
3. GET `/tranca/{idTranca}` - Obter tranca
4. PUT `/tranca/{idTranca}` - Editar tranca
5. DELETE `/tranca/{idTranca}` - Remover tranca
6. GET `/tranca/{idTranca}/bicicleta` - Obter bicicleta na tranca
7. POST `/tranca/{idTranca}/trancar` - Trancar
8. POST `/tranca/{idTranca}/destrancar` - Destrancar
9. POST `/tranca/{idTranca}/status/{acao}` - Alterar status
10. POST `/tranca/integrarNaRede` - Integrar na rede
11. POST `/tranca/retirarDaRede` - Retirar da rede

---

## Documentação Swagger

Acesse a documentação interativa em:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

*Última atualização: 08/11/2025*
