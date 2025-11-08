"""
Script para testar os endpoints de totems implementados.
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


def test_listar_totems():
    """Testa GET /totem"""
    print_separator("Teste 1: Listar todos os totems")
    
    try:
        response = httpx.get(f"{BASE_URL}/totem")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            totems = response.json()
            print(f"✅ {len(totems)} totems encontrados:")
            for totem in totems:
                print(f"   - ID {totem['id']}: {totem.get('descricao', 'Sem descrição')}")
                print(f"     Localização: {totem['localizacao']}")
        else:
            print(f"❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")


def test_cadastrar_totem():
    """Testa POST /totem"""
    print_separator("Teste 2: Cadastrar novo totem")
    
    novo_totem = {
        "localizacao": "-22.9200, -43.1800",
        "descricao": "Totem do Parque das Bicicletas - Teste"
    }
    
    try:
        response = httpx.post(
            f"{BASE_URL}/totem",
            json=novo_totem,
            timeout=10.0
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            totem = response.json()
            print(f"✅ Totem cadastrado com ID {totem['id']}:")
            print(json.dumps(totem, indent=2, ensure_ascii=False))
            return totem['id']
        else:
            print(f"❌ Erro: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return None


def test_editar_totem(totem_id):
    """Testa PUT /totem/{id}"""
    print_separator(f"Teste 3: Editar totem (ID {totem_id})")
    
    if not totem_id:
        print("⚠️  Pulando teste: ID não disponível")
        return
    
    dados_atualizados = {
        "localizacao": "-22.9200, -43.1800",
        "descricao": "Totem do Parque das Bicicletas - Atualizado"
    }
    
    try:
        response = httpx.put(
            f"{BASE_URL}/totem/{totem_id}",
            json=dados_atualizados,
            timeout=10.0
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            totem = response.json()
            print("✅ Totem atualizado:")
            print(json.dumps(totem, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")


def test_listar_trancas_do_totem():
    """Testa GET /totem/{id}/trancas"""
    print_separator("Teste 4: Listar trancas do totem 1")
    
    try:
        response = httpx.get(f"{BASE_URL}/totem/1/trancas", timeout=10.0)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            trancas = response.json()
            print(f"✅ {len(trancas)} trancas encontradas no totem 1:")
            for tranca in trancas:
                bici_info = f"Bicicleta: {tranca['bicicleta']}" if tranca['bicicleta'] else "Sem bicicleta"
                print(f"   - Tranca #{tranca['numero']} (ID {tranca['id']}) - Status: {tranca['status']} - {bici_info}")
        else:
            print(f"❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")


def test_listar_bicicletas_do_totem():
    """Testa GET /totem/{id}/bicicletas"""
    print_separator("Teste 5: Listar bicicletas do totem 1")
    
    try:
        response = httpx.get(f"{BASE_URL}/totem/1/bicicletas", timeout=10.0)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            bicicletas = response.json()
            if len(bicicletas) > 0:
                print(f"✅ {len(bicicletas)} bicicletas encontradas no totem 1:")
                for bici in bicicletas:
                    print(f"   - ID {bici['id']}: {bici['marca']} {bici['modelo']} - Status: {bici['status']}")
            else:
                print("✅ Nenhuma bicicleta encontrada no totem 1 (totens podem estar sem bicicletas)")
        else:
            print(f"❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")


def test_remover_totem(totem_id):
    """Testa DELETE /totem/{id}"""
    print_separator(f"Teste 6: Remover totem (ID {totem_id})")
    
    if not totem_id:
        print("⚠️  Pulando teste: ID não disponível")
        return
    
    try:
        response = httpx.delete(
            f"{BASE_URL}/totem/{totem_id}",
            timeout=10.0
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            resultado = response.json()
            print(f"✅ {resultado.get('mensagem', 'Totem removido')}")
        else:
            print(f"❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")


def test_totem_nao_encontrado():
    """Testa erro 404"""
    print_separator("Teste 7: Tentar obter totem inexistente")
    
    try:
        response = httpx.get(f"{BASE_URL}/totem/99999/trancas")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 404:
            erro = response.json()
            print("✅ Erro 404 retornado corretamente:")
            print(json.dumps(erro, indent=2, ensure_ascii=False))
        else:
            print(f"⚠️  Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")


def test_id_invalido():
    """Testa erro 422 com ID inválido"""
    print_separator("Teste 8: Tentar usar ID inválido (negativo)")
    
    try:
        response = httpx.get(f"{BASE_URL}/totem/-1/trancas")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 422:
            erro = response.json()
            print("✅ Erro 422 retornado corretamente:")
            print(json.dumps(erro, indent=2, ensure_ascii=False))
        else:
            print(f"⚠️  Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")


def main():
    print("\n" + "🏪" * 35)
    print("  TESTES DOS ENDPOINTS DE TOTEMS")
    print("🏪" * 35)
    
    # Executa os testes
    test_listar_totems()
    
    # Testa cadastro e obtém o ID
    totem_id = test_cadastrar_totem()
    
    # Testa edição
    test_editar_totem(totem_id)
    
    # Testa listagem de trancas
    test_listar_trancas_do_totem()
    
    # Testa listagem de bicicletas
    test_listar_bicicletas_do_totem()
    
    # Testa remoção
    test_remover_totem(totem_id)
    
    # Testa erros
    test_totem_nao_encontrado()
    test_id_invalido()
    
    print_separator("✅ TESTES CONCLUÍDOS!")
    print("\nAcesse http://localhost:8000/docs para ver a documentação completa da API.")


if __name__ == "__main__":
    main()
