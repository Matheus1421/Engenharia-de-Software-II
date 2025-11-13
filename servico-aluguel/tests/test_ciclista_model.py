"""
Testes unitários de validações do modelo Ciclista.
Testa as regras de negócio do UC01 implementadas via Pydantic.
"""
import pytest
from pydantic import ValidationError
from datetime import date
from models.ciclista_model import (
    NovoCiclista, Passaporte, Nacionalidade, Ciclista, StatusCiclista, CiclistaCadastro
)


#   TESTES DE NOVOCICLISTA - VALIDAÇÕES

def test_ciclista_cpf_valido_11_digitos():
    """UC01 - R1: Testa que CPF com exatamente 11 dígitos é aceito"""
    ciclista = NovoCiclista(
        nome="João Silva",
        nascimento=date(1990, 1, 1),
        cpf="12345678901",
        email="joao@email.com",
        nacionalidade=Nacionalidade.BRASILEIRO,
        urlFotoDocumento="http://exemplo.com/foto.jpg"
    )
    assert ciclista.cpf == "12345678901"


def test_ciclista_cpf_invalido_menos_11_digitos():
    """UC01 - R1: Testa que CPF com menos de 11 dígitos falha"""
    with pytest.raises(ValidationError) as exc:
        NovoCiclista(
            nome="João Silva",
            nascimento=date(1990, 1, 1),
            cpf="123456789",  # 9 dígitos
            email="joao@email.com",
            nacionalidade=Nacionalidade.BRASILEIRO,
            urlFotoDocumento="http://exemplo.com/foto.jpg"
        )
    assert "cpf" in str(exc.value).lower()


def test_ciclista_cpf_invalido_mais_11_digitos():
    """UC01 - R1: Testa que CPF com mais de 11 dígitos falha"""
    with pytest.raises(ValidationError) as exc:
        NovoCiclista(
            nome="João Silva",
            nascimento=date(1990, 1, 1),
            cpf="123456789012",  # 12 dígitos
            email="joao@email.com",
            nacionalidade=Nacionalidade.BRASILEIRO,
            urlFotoDocumento="http://exemplo.com/foto.jpg"
        )
    assert "cpf" in str(exc.value).lower()


def test_ciclista_cpf_invalido_nao_numerico():
    """UC01 - R1: Testa que CPF com caracteres não numéricos falha"""
    with pytest.raises(ValidationError) as exc:
        NovoCiclista(
            nome="João Silva",
            nascimento=date(1990, 1, 1),
            cpf="123.456.789-01",  # Com pontuação
            email="joao@email.com",
            nacionalidade=Nacionalidade.BRASILEIRO,
            urlFotoDocumento="http://exemplo.com/foto.jpg"
        )
    assert "cpf" in str(exc.value).lower()


def test_ciclista_email_valido():
    """UC01 - R3: Testa que email válido é aceito"""
    ciclista = NovoCiclista(
        nome="João Silva",
        nascimento=date(1990, 1, 1),
        cpf="12345678901",
        email="joao.silva@exemplo.com.br",
        nacionalidade=Nacionalidade.BRASILEIRO,
        urlFotoDocumento="http://exemplo.com/foto.jpg"
    )
    assert ciclista.email == "joao.silva@exemplo.com.br"


def test_ciclista_email_invalido_sem_arroba():
    """UC01 - R3: Testa que email sem @ falha"""
    with pytest.raises(ValidationError) as exc:
        NovoCiclista(
            nome="João Silva",
            nascimento=date(1990, 1, 1),
            cpf="12345678901",
            email="joaoemail.com",  # Sem @
            nacionalidade=Nacionalidade.BRASILEIRO,
            urlFotoDocumento="http://exemplo.com/foto.jpg"
        )
    assert "email" in str(exc.value).lower()


def test_ciclista_email_invalido_sem_dominio():
    """UC01 - R3: Testa que email sem domínio falha"""
    with pytest.raises(ValidationError) as exc:
        NovoCiclista(
            nome="João Silva",
            nascimento=date(1990, 1, 1),
            cpf="12345678901",
            email="joao@",  # Sem domínio
            nacionalidade=Nacionalidade.BRASILEIRO,
            urlFotoDocumento="http://exemplo.com/foto.jpg"
        )
    assert "email" in str(exc.value).lower()


def test_ciclista_data_nascimento_valida():
    """Testa que data de nascimento no passado é aceita"""
    ciclista = NovoCiclista(
        nome="João Silva",
        nascimento=date(1990, 1, 1),
        cpf="12345678901",
        email="joao@email.com",
        nacionalidade=Nacionalidade.BRASILEIRO,
        urlFotoDocumento="http://exemplo.com/foto.jpg"
    )
    assert ciclista.nascimento == date(1990, 1, 1)


def test_ciclista_data_nascimento_futura_invalida():
    """Testa que data de nascimento futura falha (validação técnica)"""
    with pytest.raises(ValidationError) as exc:
        NovoCiclista(
            nome="João Silva",
            nascimento=date(2030, 1, 1),  # Futura
            cpf="12345678901",
            email="joao@email.com",
            nacionalidade=Nacionalidade.BRASILEIRO,
            urlFotoDocumento="http://exemplo.com/foto.jpg"
        )
    assert "nascimento" in str(exc.value).lower() or "futura" in str(exc.value).lower()


def test_ciclista_nome_minimo_3_caracteres():
    """Testa que nome com 3 caracteres é aceito"""
    ciclista = NovoCiclista(
        nome="Ana",  # 3 caracteres
        nascimento=date(1990, 1, 1),
        cpf="12345678901",
        email="ana@email.com",
        nacionalidade=Nacionalidade.BRASILEIRO,
        urlFotoDocumento="http://exemplo.com/foto.jpg"
    )
    assert ciclista.nome == "Ana"


def test_ciclista_nome_vazio_invalido():
    """Testa que nome vazio falha"""
    with pytest.raises(ValidationError) as exc:
        NovoCiclista(
            nome="",  # Vazio
            nascimento=date(1990, 1, 1),
            cpf="12345678901",
            email="joao@email.com",
            nacionalidade=Nacionalidade.BRASILEIRO,
            urlFotoDocumento="http://exemplo.com/foto.jpg"
        )
    assert "nome" in str(exc.value).lower()


def test_ciclista_nome_muito_curto_invalido():
    """Testa que nome com menos de 3 caracteres falha"""
    with pytest.raises(ValidationError) as exc:
        NovoCiclista(
            nome="Jo",  # 2 caracteres
            nascimento=date(1990, 1, 1),
            cpf="12345678901",
            email="joao@email.com",
            nacionalidade=Nacionalidade.BRASILEIRO,
            urlFotoDocumento="http://exemplo.com/foto.jpg"
        )
    assert "nome" in str(exc.value).lower()


def test_ciclista_nacionalidade_brasileiro():
    """Testa que nacionalidade BRASILEIRO é aceita"""
    ciclista = NovoCiclista(
        nome="João Silva",
        nascimento=date(1990, 1, 1),
        cpf="12345678901",
        email="joao@email.com",
        nacionalidade=Nacionalidade.BRASILEIRO,
        urlFotoDocumento="http://exemplo.com/foto.jpg"
    )
    assert ciclista.nacionalidade == Nacionalidade.BRASILEIRO


def test_ciclista_nacionalidade_estrangeiro():
    """Testa que nacionalidade ESTRANGEIRO é aceita"""
    ciclista = NovoCiclista(
        nome="John Doe",
        nascimento=date(1985, 5, 10),
        email="john@email.com",
        nacionalidade=Nacionalidade.ESTRANGEIRO,
        urlFotoDocumento="http://exemplo.com/foto.jpg",
        passaporte=Passaporte(
            numero="AB123456",
            validade=date(2030, 12, 31),
            pais="USA"
        )
    )
    assert ciclista.nacionalidade == Nacionalidade.ESTRANGEIRO


def test_ciclista_url_foto_valida():
    """Testa que URL de foto válida é aceita"""
    ciclista = NovoCiclista(
        nome="João Silva",
        nascimento=date(1990, 1, 1),
        cpf="12345678901",
        email="joao@email.com",
        nacionalidade=Nacionalidade.BRASILEIRO,
        urlFotoDocumento="https://exemplo.com/fotos/documento123.jpg"
    )
    assert "https://exemplo.com" in ciclista.urlFotoDocumento


#   TESTES DE PASSAPORTE

def test_passaporte_valido():
    """Testa criação de passaporte válido"""
    passaporte = Passaporte(
        numero="AB123456",
        validade=date(2030, 12, 31),
        pais="USA"
    )
    assert passaporte.numero == "AB123456"
    assert passaporte.pais == "USA"


def test_passaporte_numero_minimo_4_caracteres():
    """Testa que número de passaporte com 4 caracteres é aceito"""
    passaporte = Passaporte(
        numero="A123",  # 4 caracteres
        validade=date(2030, 12, 31),
        pais="USA"
    )
    assert passaporte.numero == "A123"


def test_passaporte_numero_muito_curto_invalido():
    """Testa que número de passaporte com menos de 4 caracteres falha"""
    with pytest.raises(ValidationError) as exc:
        Passaporte(
            numero="A12",  # 3 caracteres
            validade=date(2030, 12, 31),
            pais="USA"
        )
    assert "numero" in str(exc.value).lower()


#   TESTES DE CICLISTA COMPLETO

def test_ciclista_com_todos_campos():
    """Testa criação de Ciclista completo (modelo retornado pela API)"""
    ciclista = Ciclista(
        id=1,
        nome="João Silva",
        nascimento=date(1990, 1, 1),
        cpf="12345678901",
        email="joao@email.com",
        nacionalidade=Nacionalidade.BRASILEIRO,
        urlFotoDocumento="http://exemplo.com/foto.jpg",
        status=StatusCiclista.ATIVO,
        senha="senha123",
        dataConfirmacao="2024-01-15T10:00:00Z"
    )
    assert ciclista.id == 1
    assert ciclista.status == StatusCiclista.ATIVO


def test_ciclista_status_aguardando_confirmacao():
    """Testa Ciclista com status AGUARDANDO_CONFIRMACAO"""
    ciclista = Ciclista(
        id=2,
        nome="Maria Santos",
        nascimento=date(1995, 5, 10),
        cpf="98765432100",
        email="maria@email.com",
        nacionalidade=Nacionalidade.BRASILEIRO,
        urlFotoDocumento="http://exemplo.com/foto.jpg",
        status=StatusCiclista.AGUARDANDO_CONFIRMACAO,
        senha="senha456",
        dataConfirmacao=None
    )
    assert ciclista.status == StatusCiclista.AGUARDANDO_CONFIRMACAO
    assert ciclista.dataConfirmacao is None


#   TESTES DE CICLISTACADASTRO (WRAPPER COM SENHA)

def test_ciclista_cadastro_senhas_iguais():
    """UC01 - R2: Testa que senhas iguais passam na validação"""
    cadastro = CiclistaCadastro(
        ciclista=NovoCiclista(
            nome="João Silva",
            nascimento=date(1990, 1, 1),
            cpf="12345678901",
            email="joao@email.com",
            nacionalidade=Nacionalidade.BRASILEIRO,
            urlFotoDocumento="http://exemplo.com/foto.jpg"
        ),
        senha="minhasenha123",
        confirmacaoSenha="minhasenha123"
    )
    assert cadastro.senha == "minhasenha123"


def test_ciclista_cadastro_senhas_diferentes_invalido():
    """UC01 - R2: Testa que senhas diferentes falham"""
    with pytest.raises(ValidationError) as exc:
        CiclistaCadastro(
            ciclista=NovoCiclista(
                nome="João Silva",
                nascimento=date(1990, 1, 1),
                cpf="12345678901",
                email="joao@email.com",
                nacionalidade=Nacionalidade.BRASILEIRO,
                urlFotoDocumento="http://exemplo.com/foto.jpg"
            ),
            senha="senha123",
            confirmacaoSenha="senha456"  # Diferente
        )
    assert "senha" in str(exc.value).lower()
