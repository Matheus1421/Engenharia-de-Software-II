"""
Script para testar o endpoint /restaurarBanco via HTTP
"""

import httpx
import json


def test_restaurar_banco():
    """Testa o endpoint de restauração do banco de dados"""
    
    print("🧪 Testando endpoint /restaurarBanco")
    print("-" * 60)
    
    url = "http://localhost:8000/restaurarBanco"
    
    try:
        # Faz a requisição GET
        response = httpx.get(url, timeout=10.0)
        
        # Verifica o status code
        print(f"\n📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Requisição bem-sucedida!\n")
            
            # Parse do JSON
            data = response.json()
            
            # Exibe a resposta formatada
            print("📦 Resposta:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Verifica os dados
            if 'mensagem' in data and 'dados_inseridos' in data:
                print("\n✅ Estrutura da resposta está correta!")
                
                dados = data['dados_inseridos']
                print(f"\n📈 Dados inseridos:")
                print(f"   - Bicicletas: {dados.get('bicicletas', 0)}")
                print(f"   - Trancas: {dados.get('trancas', 0)}")
                print(f"   - Totems: {dados.get('totems', 0)}")
                print(f"   - Relacionamentos: {dados.get('relacionamentos', 0)}")
            else:
                print("\n⚠️  Estrutura da resposta inesperada")
        else:
            print(f"❌ Erro: Status code {response.status_code}")
            print(f"Resposta: {response.text}")
    
    except httpx.ConnectError:
        print("❌ Erro: Não foi possível conectar ao servidor")
        print("   Verifique se o servidor está rodando em http://localhost:8000")
        print("   Execute: poetry run uvicorn main:app --reload")
    
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
    
    print("\n" + "-" * 60)


if __name__ == "__main__":
    test_restaurar_banco()
