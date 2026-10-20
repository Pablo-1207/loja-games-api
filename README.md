Loja de Games API
Projeto acadêmico — Sistemas de Banco de Dados II

API para gerenciamento de jogos de uma loja, desenvolvida com Python, FastAPI e MongoDB. A aplicação implementa operações CRUD (Create, Read, Update e Delete), filtros de consulta e paginação.
1. Identificação acadêmica
- Curso: Engenharia de Software
- Período: 4º período
- Disciplina: Sistemas de Banco de Dados II
- Alunos responsáveis: Pablo Henrique e Amanda Borges
2. Objetivo
Aplicar os conceitos estudados na disciplina por meio do desenvolvimento de uma API integrada a um banco de dados NoSQL. O projeto permite cadastrar jogos, consultar registros, atualizar informações e remover jogos, além de demonstrar o uso de validação de dados, filtros e paginação.
3. Tecnologias utilizadas
- Python — linguagem de programação.
- FastAPI — desenvolvimento dos endpoints e documentação interativa.
- MongoDB — armazenamento dos documentos de jogos.
- PyMongo — comunicação entre a aplicação Python e o MongoDB; a API utiliza o cliente assíncrono.
- Docker Compose — execução local do MongoDB em um container.
- Swagger UI — interface para documentar e testar a API em /docs.
4. Pré-requisitos
- Python instalado.
- Docker Desktop instalado e em execução.
- Git (para versionar e publicar o projeto no GitHub).
Os comandos abaixo devem ser executados na raiz do repositório, isto é, na pasta que contém docker-compose.yml, requirements.txt e seed.py.

5. Como executar o projeto
5.1. Iniciar o MongoDB
Com o Docker Desktop em execução, inicie o container:
docker compose up -d
Verifique se o container está ativo:
docker ps
O arquivo docker-compose.yml publica a porta 27017 e mantém os dados no volume mongo_data.
5.2. Criar e ativar o ambiente virtual
Windows — PowerShell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
Se o PowerShell bloquear a execução do script de ativação, libere-a somente para a sessão atual e tente ativar novamente:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
Linux ou macOS
python3 -m venv .venv
source .venv/bin/activate
5.3. Instalar as dependências
Com o ambiente virtual ativado, execute:
python -m pip install -r requirements.txt
5.4. Configurar variáveis de ambiente
O arquivo .env.example apresenta os valores de configuração locais. Para criar o arquivo .env:

Windows — PowerShell
Copy-Item .env.example .env
Linux ou macOS
cp .env.example .env
Configuração padrão:
MONGO_URL=mongodb://localhost:27017
MONGO_DB=loja_games
A criação do .env é opcional quando os valores padrão são suficientes. Não publique arquivos .env que contenham senhas, tokens ou outros segredos.
5.5. Inserir jogos de exemplo
Com o MongoDB em execução e as dependências instaladas, execute:
python seed.py
O script insere os jogos de exemplo sem duplicar registros que já existam com o mesmo título e plataforma. Atualmente, seed.py utiliza os valores de conexão padrão definidos no próprio arquivo (mongodb://localhost:27017 e loja_games). Se esses valores forem alterados, atualize também o script.
5.6. Iniciar a API
Na raiz do projeto, com o ambiente virtual ativado, execute:
python -m uvicorn app.main:app --reload
Mantenha esse terminal aberto enquanto utilizar a API. A documentação interativa ficará disponível em:
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json
- Rota de status: http://127.0.0.1:8000/
6. Endpoints CRUD
Método HTTP	Rota	Operação	Descrição
POST	/jogos	Create	Cadastra um jogo.
GET	/jogos	Read	Lista jogos com filtros e paginação.
GET	/jogos/{jogo_id}	Read	Busca um jogo pelo identificador.
PUT	/jogos/{jogo_id}	Update	Substitui os dados do jogo. Envie todos os campos obrigatórios.
PATCH	/jogos/{jogo_id}	Update	Atualiza somente os campos enviados.
DELETE	/jogos/{jogo_id}	Delete	Remove um jogo.


Filtros do GET /jogos
- busca — pesquisa parcial no título.
- plataforma — filtra pela plataforma.
- genero — filtra pelo gênero.
- preco_min e preco_max — limitam a faixa de preço.
- em_estoque — true retorna jogos com estoque maior que zero; false retorna jogos sem estoque.
- skip — quantidade de registros a ignorar na paginação.
- limit — quantidade máxima de registros retornados (entre 1 e 100).
7. Exemplos de requisições
Os exemplos de curl abaixo são destinados a Bash, Linux/macOS ou Git Bash. Também é possível executar todas as operações em http://127.0.0.1:8000/docs.
7.1. Cadastrar um jogo — POST
curl -X POST "http://localhost:8000/jogos" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Elden Ring",
    "descricao": "RPG de ação em mundo aberto.",
    "plataforma": "PlayStation 5",
    "genero": "RPG",
    "preco": 249.90,
    "estoque": 15,
    "desenvolvedora": "FromSoftware",
    "classificacao_etaria": 16,
    "data_lancamento": "2022-02-25"
  }'
7.2. Listar RPGs de PlayStation 5 em estoque até R$ 300 — GET
curl "http://localhost:8000/jogos?plataforma=PlayStation%205&genero=RPG&preco_max=300&em_estoque=true"
7.3. Atualizar somente o estoque — PATCH
Substitua ID_DO_JOGO pelo id retornado pela API:
curl -X PATCH "http://localhost:8000/jogos/ID_DO_JOGO" \
  -H "Content-Type: application/json" \
  -d '{"estoque": 14}'
O PATCH preserva os campos omitidos na requisição. Envie apenas os campos que deseja alterar.
7.4. Substituir os dados — PUT
O PUT substitui os dados do jogo; envie todos os campos exigidos pelo modelo:
curl -X PUT "http://localhost:8000/jogos/ID_DO_JOGO" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Elden Ring",
    "descricao": "RPG de ação em mundo aberto.",
    "plataforma": "PlayStation 5",
    "genero": "RPG",
    "preco": 249.90,
    "estoque": 14,
    "desenvolvedora": "FromSoftware",
    "classificacao_etaria": 16,
    "data_lancamento": "2022-02-25"
  }'
7.5. Remover um jogo — DELETE
Substitua ID_DO_JOGO pelo identificador do registro que deseja remover:
curl -X DELETE "http://localhost:8000/jogos/ID_DO_JOGO"
Faça testes de exclusão com um registro descartável para evitar apagar dados que deseja manter.
8. Regras e observações sobre os dados
- As datas devem ser informadas como strings no formato YYYY-MM-DD, por exemplo, "2022-02-25".
- A plataforma deve corresponder exatamente a uma das opções aceitas pela aplicação, como "PlayStation 5", "PC" ou "Nintendo Switch".
- A classificação etária aceita os valores 0, 10, 12, 14, 16 e 18.
- O preço deve ser maior que zero e o estoque não pode ser negativo.
- A aplicação cria um índice único para a combinação de título e plataforma. Não cadastre a mesma combinação mais de uma vez. Caso existam duplicidades inseridas manualmente, será necessário corrigi-las antes que a API consiga criar esse índice.
9. Estrutura do projeto
loja-games/
├── app/
│   ├── routers/
│   │   └── jogos.py
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   └── schemas.py
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
├── requirements.txt
└── seed.py
- app/main.py — cria a aplicação FastAPI, configura o ciclo de vida e o índice único.
- app/config.py — carrega as configurações da aplicação.
- app/database.py — configura o cliente e o acesso à coleção MongoDB.
- app/schemas.py — define modelos e validações dos dados com Pydantic.
- app/routers/jogos.py — implementa os endpoints CRUD.
- docker-compose.yml — define o container MongoDB e o volume persistente.
- requirements.txt — lista as dependências Python.
- seed.py — insere os dados iniciais de exemplo.
- .env.example — modelo das variáveis de ambiente.
- .gitignore — impede que arquivos temporários, ambientes virtuais e configurações locais sejam enviados ao Git.
10. Considerações finais
O desenvolvimento deste projeto permitiu aplicar os conceitos de gerenciamento de dados e integração entre aplicações e bancos de dados, com foco nas operações CRUD em um banco NoSQL. A implementação também proporcionou prática com validação de dados, filtros, paginação, documentação de APIs e execução de serviços por meio do Docker.
Curso: Engenharia de Software
Período: 4º período
Disciplina: Sistemas de Banco de Dados II
Alunos: Pablo Henrique e Amanda Borges