JusCash - Gerenciador de Publicações Judiciais

Visão Geral do Projeto

O JusCash é um sistema web desenvolvido para centralizar, visualizar e gerenciar publicações judiciais extraídas automaticamente de Diários de Justiça Eletrônicos (DJEs). É composto por:

Um frontend React para visualização das publicações em formato Kanban.

Um backend FastAPI com banco de dados SQLite para armazenamento e manipulação das publicações.

Mecanismo de scraping para obtenção automatizada das publicações.

Estrutura do Projeto

JusCash/
├── backend/
│   ├── database/
│   ├── models.py
│   ├── api.py
├── frontend/
│   ├── public/
│   ├── src/
│   └── components/
├── README.md (visão geral)
├── backend/README.md
└── frontend/README.md
