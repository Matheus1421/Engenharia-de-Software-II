import os
import sys
import pytest

# Ensure the service root (where main.py lives) is on sys.path for test imports
CURRENT_DIR = os.path.dirname(__file__)
SERVICE_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if SERVICE_ROOT not in sys.path:
    sys.path.insert(0, SERVICE_ROOT)

from models.bicicleta_model import Bicicleta, StatusBicicleta
from models.tranca_model import Tranca, StatusTranca


# Fixtures compartilhadas para Bicicletas
@pytest.fixture
def bicicleta_padrao():
    """Bicicleta padrão disponível"""
    return Bicicleta(
        id=1,
        marca="Caloi",
        modelo="Mountain Bike",
        ano="2023",
        numero=100,
        status=StatusBicicleta.DISPONIVEL
    )


@pytest.fixture
def bicicleta_exemplo():
    """Alias para bicicleta_padrao (compatibilidade)"""
    return Bicicleta(
        id=1,
        marca="Caloi",
        modelo="Mountain Bike",
        ano="2023",
        numero=100,
        status=StatusBicicleta.DISPONIVEL
    )


# Fixtures compartilhadas para Trancas
@pytest.fixture
def tranca_livre():
    """Tranca livre (sem bicicleta)"""
    return Tranca(
        id=1,
        numero=1,
        localizacao="Zona Sul",
        anoDeFabricacao="2023",
        modelo="Modelo A",
        status=StatusTranca.LIVRE,
        bicicleta=None
    )


@pytest.fixture
def tranca_exemplo():
    """Alias para tranca_livre (compatibilidade)"""
    return Tranca(
        id=1,
        numero=1,
        localizacao="Zona Sul",
        anoDeFabricacao="2023",
        modelo="Modelo A",
        status=StatusTranca.LIVRE,
        bicicleta=None
    )


@pytest.fixture
def tranca_ocupada():
    """Tranca ocupada com bicicleta"""
    return Tranca(
        id=2,
        numero=2,
        localizacao="Zona Sul",
        anoDeFabricacao="2023",
        modelo="Modelo A",
        status=StatusTranca.OCUPADA,
        bicicleta=1
    )


@pytest.fixture
def tranca_com_bicicleta():
    """Alias para tranca_ocupada (compatibilidade)"""
    return Tranca(
        id=2,
        numero=2,
        localizacao="Zona Sul",
        anoDeFabricacao="2023",
        modelo="Modelo A",
        status=StatusTranca.OCUPADA,
        bicicleta=1
    )
