"""
Testes unitários de validações do modelo Funcionário.
Testa as regras de negócio do UC15 implementadas via Pydantic.
"""
import pytest
from pydantic import ValidationError
from models.funcionario_model import NovoFuncionario, Funcionario, FuncaoFuncionario


#   TESTES DE NOVOFUNCIONARIO - VALIDAÇÕES

def test_funcionario_idade_18_valida():
    """UC15 - R1: Testa que idade exatamente 18 anos é aceita"""
    funcionario = NovoFuncionario(
        nome="João Silva",
        idade=18,  # Limite inferior
        funcao=FuncaoFuncionario.ADMINISTRATIVO,
        cpf="12345678901",
        email="joao@scb.com",
        senha="senha123",
        confirmacaoSenha="senha123"
    )
    assert funcionario.idade == 18


def test_funcionario_idade_menor_18_invalida():
    """UC15 - R1: Testa que idade menor que 18 anos falha"""
    with pytest.raises(ValidationError) as exc:
        NovoFuncionario(
            nome="João Silva",
            idade=17,  # Menor de idade
            funcao=FuncaoFuncionario.ADMINISTRATIVO,
            cpf="12345678901",
            email="joao@scb.com",
            senha="senha123",
            confirmacaoSenha="senha123"
        )
    assert "idade" in str(exc.value).lower()


def test_funcionario_idade_120_valida():
    """UC15 - R1: Testa que idade 120 anos é aceita (limite superior)"""
    funcionario = NovoFuncionario(
        nome="João Silva",
        idade=120,
        funcao=FuncaoFuncionario.ADMINISTRATIVO,
        cpf="12345678901",
        email="joao@scb.com",
        senha="senha123",
        confirmacaoSenha="senha123"
    )
    assert funcionario.idade == 120


def test_funcionario_idade_maior_120_invalida():
    """UC15 - R1: Testa que idade maior que 120 anos falha"""
    with pytest.raises(ValidationError) as exc:
        NovoFuncionario(
            nome="João Silva",
            idade=121,
            funcao=FuncaoFuncionario.ADMINISTRATIVO,
            cpf="12345678901",
            email="joao@scb.com",
            senha="senha123",
            confirmacaoSenha="senha123"
        )
    assert "idade" in str(exc.value).lower()


def test_funcionario_cpf_11_digitos_valido():
    """UC15 - R2: Testa que CPF com 11 dígitos é aceito"""
    funcionario = NovoFuncionario(
        nome="João Silva",
        idade=30,
        funcao=FuncaoFuncionario.ADMINISTRATIVO,
        cpf="12345678901",
        email="joao@scb.com",
        senha="senha123",
        confirmacaoSenha="senha123"
    )
    assert funcionario.cpf == "12345678901"


def test_funcionario_cpf_menos_11_digitos_invalido():
    """UC15 - R2: Testa que CPF com menos de 11 dígitos falha"""
    with pytest.raises(ValidationError) as exc:
        NovoFuncionario(
            nome="João Silva",
            idade=30,
            funcao=FuncaoFuncionario.ADMINISTRATIVO,
            cpf="123456789",  # 9 dígitos
            email="joao@scb.com",
            senha="senha123",
            confirmacaoSenha="senha123"
        )
    assert "cpf" in str(exc.value).lower()


def test_funcionario_cpf_mais_11_digitos_invalido():
    """UC15 - R2: Testa que CPF com mais de 11 dígitos falha"""
    with pytest.raises(ValidationError) as exc:
        NovoFuncionario(
            nome="João Silva",
            idade=30,
            funcao=FuncaoFuncionario.ADMINISTRATIVO,
            cpf="123456789012",  # 12 dígitos
            email="joao@scb.com",
            senha="senha123",
            confirmacaoSenha="senha123"
        )
    assert "cpf" in str(exc.value).lower()


def test_funcionario_funcao_administrativo():
    """UC15 - R3: Testa que função ADMINISTRATIVO é aceita"""
    funcionario = NovoFuncionario(
        nome="Admin Sistema",
        idade=35,
        funcao=FuncaoFuncionario.ADMINISTRATIVO,
        cpf="12345678901",
        email="admin@scb.com",
        senha="senha123",
        confirmacaoSenha="senha123"
    )
    assert funcionario.funcao == FuncaoFuncionario.ADMINISTRATIVO


def test_funcionario_funcao_reparador():
    """UC15 - R3: Testa que função REPARADOR é aceita"""
    funcionario = NovoFuncionario(
        nome="João Reparador",
        idade=28,
        funcao=FuncaoFuncionario.REPARADOR,
        cpf="98765432100",
        email="joao@scb.com",
        senha="senha123",
        confirmacaoSenha="senha123"
    )
    assert funcionario.funcao == FuncaoFuncionario.REPARADOR


def test_funcionario_senhas_iguais():
    """UC15 - R4: Testa que senha e confirmação iguais passam"""
    funcionario = NovoFuncionario(
        nome="Carlos Silva",
        idade=40,
        funcao=FuncaoFuncionario.ADMINISTRATIVO,
        cpf="55566677788",
        email="carlos@scb.com",
        senha="minhasenha123",
        confirmacaoSenha="minhasenha123"
    )
    assert funcionario.senha == "minhasenha123"


def test_funcionario_senhas_diferentes_invalido():
    """UC15 - R4: Testa que senha e confirmação diferentes falham"""
    with pytest.raises(ValidationError) as exc:
        NovoFuncionario(
            nome="Carlos Silva",
            idade=40,
            funcao=FuncaoFuncionario.ADMINISTRATIVO,
            cpf="55566677788",
            email="carlos@scb.com",
            senha="senha123",
            confirmacaoSenha="senha456"  # Diferente
        )
    assert "senha" in str(exc.value).lower()


def test_funcionario_email_valido():
    """Testa que email válido é aceito"""
    funcionario = NovoFuncionario(
        nome="João Silva",
        idade=30,
        funcao=FuncaoFuncionario.ADMINISTRATIVO,
        cpf="12345678901",
        email="joao.silva@scb.com",
        senha="senha123",
        confirmacaoSenha="senha123"
    )
    assert funcionario.email == "joao.silva@scb.com"


def test_funcionario_email_invalido():
    """Testa que email inválido falha"""
    with pytest.raises(ValidationError) as exc:
        NovoFuncionario(
            nome="João Silva",
            idade=30,
            funcao=FuncaoFuncionario.ADMINISTRATIVO,
            cpf="12345678901",
            email="emailinvalido",  # Sem @
            senha="senha123",
            confirmacaoSenha="senha123"
        )
    assert "email" in str(exc.value).lower()


#   TESTES DE FUNCIONARIO COMPLETO

def test_funcionario_completo_com_matricula():
    """Testa criação de Funcionário completo (com matrícula gerada)"""
    funcionario = Funcionario(
        matricula="F001",
        nome="Admin Sistema",
        idade=35,
        funcao=FuncaoFuncionario.ADMINISTRATIVO,
        cpf="12345678901",
        email="admin@scb.com",
        senha="admin123"
    )
    assert funcionario.matricula == "F001"
    assert funcionario.funcao == FuncaoFuncionario.ADMINISTRATIVO


def test_funcionario_matricula_formato_correto():
    """Testa que matrícula no formato F001, F002, etc. é aceita"""
    funcionario = Funcionario(
        matricula="F042",
        nome="Funcionário 42",
        idade=30,
        funcao=FuncaoFuncionario.REPARADOR,
        cpf="11122233344",
        email="func42@scb.com",
        senha="senha123"
    )
    assert funcionario.matricula == "F042"
