Sistema de Controle de Bicicletário
Visão Geral
Este projeto é um sistema de controle de bicicletário, desenvolvido como parte da disciplina de Engenharia de Software II. O objetivo é criar uma solução baseada em microsserviços, cada um responsável por um domínio específico do sistema, utilizando Python e FastAPI. A especificação da API segue o modelo fornecido pelo professor, disponível em SwaggerHub.

Estrutura do Repositório
O repositório está organizado em uma pasta para cada microsserviço, facilitando o desenvolvimento independente por cada integrante do grupo:

text
/
├── servico-aluguel/        # Microsserviço responsável por aluguel de bicicletas e gestão de ciclistas/funcionários
├── servico-equipamento/    # Microsserviço responsável por bicicletas, totens e trancas
├── servico-externo/        # Microsserviço responsável por integrações externas (e-mail, cobrança)
└── README.md               # Este arquivo
Cada pasta de microsserviço contém sua própria estrutura de código, testes e documentação.

Microsserviços
1. servico-aluguel
Gerencia ciclistas, funcionários e operações de aluguel/devolução de bicicletas.

Endpoints principais:

Cadastro e consulta de ciclistas e funcionários

Realização de aluguel e devolução

Verificação de permissão para aluguel

2. servico-equipamento
Gerencia bicicletas, totens e trancas.

Endpoints principais:

Cadastro, consulta e atualização de bicicletas, totens e trancas

Integração e retirada de equipamentos da rede

Alteração de status de equipamentos

3. servico-externo
Responsável por integrações externas, como envio de e-mails e cobranças.

Endpoints principais:

Notificação por e-mail

Processamento e consulta de cobranças

Validação de cartão de crédito

Tecnologias Utilizadas
Linguagem: Python 3.10+

Framework Web: FastAPI

Testes: pytest

Revisão Contínua de Código: SonarCloud ou Codacy

Deploy: Render, Heroku, Digital Ocean, AWS ou similar

Controle de Versão: GitHub

Como Executar Localmente
Cada microsserviço pode ser executado de forma independente. Exemplo para o servico-aluguel:

bash
cd servico-aluguel
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
Repita o processo para os outros microsserviços, ajustando o diretório.

Testes Automatizados
Cada microsserviço possui testes automatizados utilizando pytest. Para rodar os testes:

bash
pytest
Integração Contínua
O repositório está integrado ao SonarCloud/Codacy para análise contínua de código. A análise é executada a cada commit/pull request.

Deploy
O deploy é realizado em um servidor público, tornando pelo menos um endpoint acessível externamente. As instruções de deploy estão na documentação de cada microsserviço.

Especificação da API
A especificação completa da API está disponível em SwaggerHub. Os principais domínios e endpoints estão divididos entre os microsserviços conforme as tags:

Aluguel: operações de aluguel, ciclistas, funcionários

Equipamento: bicicletas, totens, trancas

Externo: e-mail, cobrança
