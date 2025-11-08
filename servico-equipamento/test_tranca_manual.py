"""
Script de teste dos endpoints de trancas
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("=" * 60)
print("TESTES DOS ENDPOINTS DE TRANCAS")
print("=" * 60)

# 1. Listar trancas
print("\n1. GET /tranca - Listar todas as trancas")
response = client.get("/tranca")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    trancas = response.json()
    print(f"   Total: {len(trancas)} trancas")
    for t in trancas[:3]:  # Mostra as 3 primeiras
        print(f"   - Tranca {t['id']}: número {t['numero']}, status {t['status']}")

# 2. Obter tranca específica
print("\n2. GET /tranca/1 - Obter tranca específica")
response = client.get("/tranca/1")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    tranca = response.json()
    print(f"   Tranca: {tranca['id']}, Número: {tranca['numero']}, Status: {tranca['status']}")

# 3. Cadastrar nova tranca
print("\n3. POST /tranca - Cadastrar nova tranca")
nova_tranca = {
    "numero": 10,
    "localizacao": "-22.9068,-43.1729",
    "anoDeFabricacao": "2024",
    "modelo": "Modelo X1",
    "status": "NOVA"
}
response = client.post("/tranca", json=nova_tranca)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    tranca = response.json()
    print(f"   Tranca criada: ID {tranca['id']}, Número {tranca['numero']}")
    tranca_id = tranca['id']
else:
    print(f"   Erro: {response.json()}")
    tranca_id = 1  # Usar tranca existente

# 4. Editar tranca
print(f"\n4. PUT /tranca/{tranca_id} - Editar tranca")
tranca_editada = {
    "numero": 10,
    "localizacao": "-22.9068,-43.1729",
    "anoDeFabricacao": "2024",
    "modelo": "Modelo X2 ATUALIZADO",
    "status": "NOVA"
}
response = client.put(f"/tranca/{tranca_id}", json=tranca_editada)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    tranca = response.json()
    print(f"   Tranca atualizada: Modelo {tranca['modelo']}")

# 5. Obter bicicleta na tranca (sem bicicleta)
print("\n5. GET /tranca/1/bicicleta - Obter bicicleta na tranca")
response = client.get("/tranca/1/bicicleta")
print(f"   Status: {response.status_code}")
if response.status_code == 404:
    print(f"   Esperado: {response.json()}")

# 6. Integrar na rede
print(f"\n6. POST /tranca/integrarNaRede - Integrar tranca na rede")
integracao = {
    "idTotem": 1,
    "idTranca": tranca_id,
    "idFuncionario": 1
}
response = client.post("/tranca/integrarNaRede", json=integracao)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print(f"   Mensagem: {response.json()['mensagem']}")

# 7. Trancar (sem bicicleta)
print(f"\n7. POST /tranca/{tranca_id}/trancar - Trancar tranca")
response = client.post(f"/tranca/{tranca_id}/trancar", json={})
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    tranca = response.json()
    print(f"   Status após trancar: {tranca['status']}")

# 8. Destrancar
print(f"\n8. POST /tranca/{tranca_id}/destrancar - Destrancar tranca")
response = client.post(f"/tranca/{tranca_id}/destrancar", json={})
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    tranca = response.json()
    print(f"   Status após destrancar: {tranca['status']}")

# 9. Alterar status via ação
print(f"\n9. POST /tranca/{tranca_id}/status/TRANCAR - Alterar status")
response = client.post(f"/tranca/{tranca_id}/status/TRANCAR")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    tranca = response.json()
    print(f"   Status após ação: {tranca['status']}")

# 10. Retirar da rede
print(f"\n10. POST /tranca/retirarDaRede - Retirar tranca da rede")
retirada = {
    "idTotem": 1,
    "idTranca": tranca_id,
    "idFuncionario": 1,
    "statusAcaoReparador": "EM_REPARO"
}
response = client.post("/tranca/retirarDaRede", json=retirada)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print(f"   Mensagem: {response.json()['mensagem']}")
    print(f"   Novo status: {response.json()['novoStatus']}")

# 11. Remover tranca
print(f"\n11. DELETE /tranca/{tranca_id} - Remover tranca")
response = client.delete(f"/tranca/{tranca_id}")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print(f"   Mensagem: {response.json()['mensagem']}")

# Testes de validação
print("\n" + "=" * 60)
print("TESTES DE VALIDAÇÃO")
print("=" * 60)

# Tranca não encontrada
print("\n12. GET /tranca/9999 - Tranca inexistente")
response = client.get("/tranca/9999")
print(f"   Status: {response.status_code}")
if response.status_code == 404:
    erro = response.json()
    print(f"   Código: {erro['codigo']}")
    print(f"   Mensagem: {erro['mensagem']}")

# ID inválido para obter bicicleta
print("\n13. GET /tranca/0/bicicleta - ID inválido")
response = client.get("/tranca/0/bicicleta")
print(f"   Status: {response.status_code}")
if response.status_code == 422:
    erro = response.json()
    print(f"   Código: {erro['codigo']}")
    print(f"   Mensagem: {erro['mensagem']}")

# Ação inválida
print("\n14. POST /tranca/1/status/INVALIDA - Ação inválida")
response = client.post("/tranca/1/status/INVALIDA")
print(f"   Status: {response.status_code}")
if response.status_code == 422:
    erros = response.json()
    print(f"   Código: {erros[0]['codigo']}")
    print(f"   Mensagem: {erros[0]['mensagem']}")

# Número duplicado
print("\n15. POST /tranca - Número duplicado")
nova_tranca_dup = {
    "numero": 1,  # Já existe
    "localizacao": "-22.9068,-43.1729",
    "anoDeFabricacao": "2024",
    "modelo": "Modelo X1",
    "status": "NOVA"
}
response = client.post("/tranca", json=nova_tranca_dup)
print(f"   Status: {response.status_code}")
if response.status_code == 422:
    erros = response.json()
    print(f"   Código: {erros[0]['codigo']}")
    print(f"   Mensagem: {erros[0]['mensagem']}")

print("\n" + "=" * 60)
print("✓ TODOS OS TESTES CONCLUÍDOS")
print("=" * 60)
