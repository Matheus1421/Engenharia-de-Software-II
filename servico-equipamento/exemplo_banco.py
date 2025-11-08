"""
Script de exemplo para demonstrar o uso do banco de dados JSON.
Execute este script para ver o banco de dados em ação.
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from database.database import get_db
from database.init_data import init_db
from repositories.bicicleta_repository import BicicletaRepository
from repositories.tranca_repository import TrancaRepository
from repositories.totem_repository import TotemRepository
from models.bicicleta_model import NovaBicicleta, StatusBicicleta
from models.tranca_model import NovaTranca, StatusTranca
from models.totem_model import NovoTotem


def print_separator():
    print("\n" + "="*60 + "\n")


def main():
    print("🚲 Demonstração do Banco de Dados JSON - Serviço Equipamentos")
    print_separator()
    
    # Obtém a instância do banco
    db = get_db()
    
    # Inicializa com dados de exemplo
    print("📦 Inicializando banco de dados com dados de exemplo...")
    result = init_db(db)
    print(f"✓ Banco inicializado com:")
    print(f"  - {result['bicicletas']} bicicletas")
    print(f"  - {result['trancas']} trancas")
    print(f"  - {result['totems']} totems")
    print(f"  - {result['relacionamentos']} relacionamentos")
    
    print_separator()
    
    # Cria os repositórios
    bicicleta_repo = BicicletaRepository(db)
    tranca_repo = TrancaRepository(db)
    totem_repo = TotemRepository(db)
    
    # DEMONSTRAÇÃO 1: Listar todas as bicicletas
    print("📋 DEMONSTRAÇÃO 1: Listando todas as bicicletas")
    bicicletas = bicicleta_repo.get_all()
    for bici in bicicletas:
        print(f"  - ID {bici.id}: {bici.marca} {bici.modelo} ({bici.ano}) - Status: {bici.status}")
    
    print_separator()
    
    # DEMONSTRAÇÃO 2: Buscar uma bicicleta específica
    print("📋 DEMONSTRAÇÃO 2: Buscando bicicleta ID 1")
    bici = bicicleta_repo.get_by_id(1)
    if bici:
        print(f"  ✓ Encontrada: {bici.marca} {bici.modelo}")
        print(f"    Ano: {bici.ano}")
        print(f"    Número: {bici.numero}")
        print(f"    Status: {bici.status}")
    
    print_separator()
    
    # DEMONSTRAÇÃO 3: Criar uma nova bicicleta
    print("📋 DEMONSTRAÇÃO 3: Criando nova bicicleta")
    nova_bici = NovaBicicleta(
        marca="Scott",
        modelo="Scale 970",
        ano="2024",
        numero=200,
        status=StatusBicicleta.NOVA
    )
    bici_criada = bicicleta_repo.create(nova_bici)
    print(f"  ✓ Bicicleta criada com ID {bici_criada.id}")
    print(f"    {bici_criada.marca} {bici_criada.modelo}")
    
    print_separator()
    
    # DEMONSTRAÇÃO 4: Atualizar status de uma bicicleta
    print("📋 DEMONSTRAÇÃO 4: Atualizando status da bicicleta")
    bici_atualizada = bicicleta_repo.update_status(bici_criada.id, StatusBicicleta.DISPONIVEL)
    if bici_atualizada:
        print(f"  ✓ Status atualizado: {bici_atualizada.status}")
    
    print_separator()
    
    # DEMONSTRAÇÃO 5: Listar totems e suas trancas
    print("📋 DEMONSTRAÇÃO 5: Listando totems e suas trancas")
    totems = totem_repo.get_all()
    for totem in totems:
        print(f"\n  🏪 Totem ID {totem.id}: {totem.descricao}")
        print(f"     Localização: {totem.localizacao}")
        
        trancas_ids = totem_repo.get_trancas_ids(totem.id)
        print(f"     Trancas ({len(trancas_ids)}):")
        
        for tranca_id in trancas_ids:
            tranca = tranca_repo.get_by_id(tranca_id)
            if tranca:
                bici_id = "Nenhuma" if tranca.bicicleta is None else f"Bicicleta #{tranca.bicicleta}"
                print(f"       - Tranca #{tranca.numero} ({tranca.status}) - {bici_id}")
    
    print_separator()
    
    # DEMONSTRAÇÃO 6: Associar bicicleta a uma tranca
    print("📋 DEMONSTRAÇÃO 6: Associando bicicleta a uma tranca")
    tranca = tranca_repo.get_by_id(1)
    if tranca:
        print(f"  Antes: Tranca #{tranca.numero} - Status: {tranca.status}, Bicicleta: {tranca.bicicleta}")
        
        # Associa a bicicleta
        tranca_atualizada = tranca_repo.associar_bicicleta(1, 1)
        if tranca_atualizada:
            print(f"  Depois: Tranca #{tranca_atualizada.numero} - Status: {tranca_atualizada.status}, Bicicleta: {tranca_atualizada.bicicleta}")
    
    print_separator()
    
    # DEMONSTRAÇÃO 7: Remover uma bicicleta
    print("📋 DEMONSTRAÇÃO 7: Removendo uma bicicleta")
    print(f"  Removendo bicicleta ID {bici_criada.id}...")
    if bicicleta_repo.delete(bici_criada.id):
        print(f"  ✓ Bicicleta removida com sucesso")
        print(f"  Total de bicicletas agora: {len(bicicleta_repo.get_all())}")
    
    print_separator()
    
    print("✅ Demonstração concluída!")
    print("\nO banco de dados está localizado em:")
    print(f"  {Path(__file__).parent / 'database' / 'equipamentos.json'}")
    print("\nVocê pode abrir este arquivo para ver os dados em formato JSON.")


if __name__ == "__main__":
    main()
