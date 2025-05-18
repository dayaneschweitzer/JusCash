Backend

Tecnologias
* Python 3.10+
* FastAPI
* SQLite3

Requisitos
pip install -r requirements.txt

Inicialização
cd backend
uvicorn api:app --reload

Endpoints Disponíveis

GET /api/publicacoes - Listagem com filtros (query, fromDate, toDate)
PATCH /api/publicacoes/{id} - Atualiza o status da publicação
POST /api/register - Cadastro de novo usuário
POST /api/login - Login do administrador

Estrutura da Tabela
Tabela publicacoes:

id, numero_processo, autores, reu, advogados, valor_bruto, valor_juros, honorarios, conteudo, status, data_publicacao

Tabela usuarios:

id, nome, email (UNIQUE), senha

Scraping e Fluxo
* Publicações podem ser importadas via script externo com salvamento no banco via salvar_publicacao().