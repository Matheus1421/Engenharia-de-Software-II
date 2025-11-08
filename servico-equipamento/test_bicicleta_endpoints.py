"""
Script para testar os endpoints de bicicletas implementados.
"""

import httpx
import json


BASE_URL = "http://localhost:8000"


def print_separator(title=""):
    print("\n" + "="*70)
    if title:
        print(f"  {title}")
        print("="*70)
    print()


def test_listar_bicicletas():
    """Testa GET /bicicleta"""
    print_separator("Teste 1: Listar todas as bicicletas")
    
    try:
        response = httpx.get(f"{BASE_URL}/bicicleta")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            bicicletas = response.json()
            print(f"✅ {len(bicicletas)} bicicletas encontradas:")
            for bici in bicicletas:
                print(f"   - ID {bici['id']}: {bici['marca']} {bici['modelo']} (Status: {bici['status']})")
        else:
            print(f"❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")


def test_obter_bicicleta():
    """Testa GET /bicicleta/{id}"""
    print_separator("Teste 2: Obter bicicleta específica (ID 1)")
    
    try:
        response = httpx.get(f"{BASE_URL}/bicicleta/1")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            bici = response.json()
            print(f"✅ Bicicleta encontrada:")
            print(json.dumps(bici, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")


def test_cadastrar_bicicleta():
    """Testa POST /bicicleta"""
    print_separator("Teste 3: Cadastrar nova bicicleta")
    
    nova_bicicleta = {
        "marca": "Giant",
        "modelo": "TCR Advanced",
        "ano": "2024",
        "numero": 500,
        "status": "NOVA"
    }
    
    try:
        response = httpx.post(
            f"{BASE_URL}/bicicleta",
            json=nova_bicicleta,
            timeout=10.0
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            bici = response.json()
            print(f"✅ Bicicleta cadastrada com ID {bici['id']}:")
            print(json.dumps(bici, indent=2, ensure_ascii=False))
            return bici['id']
        else:
            print(f"❌ Erro: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return None


def test_atualizar_bicicleta(bici_id):
    """Testa PUT /bicicleta/{id}"""
    print_separator(f"Teste 4: Atualizar bicicleta (ID {bici_id})")
    
    if not bici_id:
        print("⚠️  Pulando teste: ID não disponível")
        return
    
    dados_atualizados = {
        "marca": "Giant",
        "modelo": "TCR Advanced Pro",
        "ano": "2024",
        "numero": 500,
        "status": "NOVA"
    }
    
    try:
        response = httpx.put(
            f"{BASE_URL}/bicicleta/{bici_id}",
            json=dados_atualizados,
            timeout=10.0
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            bici = response.json()
            print(f"✅ Bicicleta atualizada:")
            print(json.dumps(bici, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")


def test_alterar_status(bici_id):
    """Testa POST /bicicleta/{id}/status/{acao}"""
    print_separator(f"Teste 5: Alterar status da bicicleta (ID {bici_id})")
    
    if not bici_id:
        print("⚠️  Pulando teste: ID não disponível")
        return
    
    try:
        response = httpx.post(
            f"{BASE_URL}/bicicleta/{bici_id}/status/DISPONIVEL",
            timeout=10.0
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            bici = response.json()
            print(f"✅ Status alterado para: {bici['status']}")
        else:
            print(f"❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")


def test_integrar_na_rede():
    """Testa POST /bicicleta/integrarNaRede"""
    print_separator("Teste 6: Integrar bicicleta na rede")
    
    # Primeiro, vamos criar uma bicicleta com status NOVA
    nova_bici = {
        "marca": "Specialized",
        "modelo": "Roubaix",
        "ano": "2024",
        "numero": 600,
        "status": "NOVA"
    }
    
    try:
        # Cria a bicicleta
        response = httpx.post(f"{BASE_URL}/bicicleta", json=nova_bici, timeout=10.0)
        if response.status_code != 200:
            print(f"❌ Erro ao criar bicicleta: {response.text}")
            return
        
        bici_id = response.json()['id']
        print(f"Bicicleta criada com ID {bici_id}")
        
        # Tenta integrar na rede (tranca 1 deve estar livre)
        integracao = {
            "idTranca": 1,
            "idBicicleta": bici_id,
            "idFuncionario": 1
        }
        
        response = httpx.post(
            f"{BASE_URL}/bicicleta/integrarNaRede",
            json=integracao,
            timeout=10.0
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            resultado = response.json()
            print(f"✅ Bicicleta integrada na rede:")
            print(json.dumps(resultado, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")


def test_remover_bicicleta(bici_id):
    """Testa DELETE /bicicleta/{id}"""
    print_separator(f"Teste 7: Remover bicicleta (ID {bici_id})")
    
    if not bici_id:
        print("⚠️  Pulando teste: ID não disponível")
        return
    
    try:
        response = httpx.delete(
            f"{BASE_URL}/bicicleta/{bici_id}",
            timeout=10.0
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            resultado = response.json()
            print(f"✅ {resultado.get('mensagem', 'Bicicleta removida')}")
        else:
            print(f"❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")


def test_bicicleta_nao_encontrada():
    """Testa erro 404"""
    print_separator("Teste 8: Tentar obter bicicleta inexistente")
    
    try:
        response = httpx.get(f"{BASE_URL}/bicicleta/99999")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 404:
            erro = response.json()
            print(f"✅ Erro 404 retornado corretamente:")
            print(json.dumps(erro, indent=2, ensure_ascii=False))
        else:
            print(f"⚠️  Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")


def main():
    print("\n" + "🚲" * 35)
    print("  TESTES DOS ENDPOINTS DE BICICLETAS")
    print("🚲" * 35)
    
    # Executa os testes
    test_listar_bicicletas()
    test_obter_bicicleta()
    
    # Testa cadastro e obtém o ID
    bici_id = test_cadastrar_bicicleta()
    
    # Testa atualização
    test_atualizar_bicicleta(bici_id)
    
    # Testa alteração de status
    test_alterar_status(bici_id)
    
    # Testa integração na rede
    test_integrar_na_rede()
    
    # Testa remoção
    test_remover_bicicleta(bici_id)
    
    # Testa erro 404
    test_bicicleta_nao_encontrada()
    
    print_separator("✅ TESTES CONCLUÍDOS!")
    print("\nAcesse http://localhost:8000/docs para ver a documentação completa da API.")


if __name__ == "__main__":
    main()
