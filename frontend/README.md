# JusCash Frontend

Este projeto é o frontend desenvolvido para o case JusCash, cuja proposta é gerenciar e processar publicações extraídas do Diário da Justiça Eletrônico (DJE). O sistema integra funcionalidades de autenticação (login e cadastro), além de uma interface de gerenciamento no formato Kanban, permitindo a movimentação de cards e a visualização detalhada de cada publicação.

## Funcionalidades

- **Login e Cadastro:** Validação de credenciais e criação de conta com requisitos de senha.
- **Kanban:** Interface para gerenciamento dos cards, com colunas para "Publicações Novas", "Publicações Lidas", "Enviado para ADV" e "Concluídas".
- **Drag and Drop:** Utilização do `react-beautiful-dnd` para permitir a movimentação dos cards entre as colunas, respeitando as regras de transição.
- **Busca e Filtros:** Barra de busca e filtro por data (usando `react-datepicker`).
- **Modal de Detalhes:** Ao clicar em um card, exibe os detalhes completos da publicação.

## Estrutura do Projeto

```plaintext
my-react-app/
├── node_modules/               # Dependências instaladas
├── public/                     # Arquivos estáticos (index.html, logo.png, etc.)
├── src/                        # Código fonte do aplicativo
│   ├── components/             # Componentes reutilizáveis (Navbar, Login, Register, KanbanBoard, etc.)
│   ├── App.js                  # Componente principal que gerencia as rotas
│   ├── index.js                # Ponto de entrada do React
│   └── index.css               # Estilos gerais do projeto
├── .gitignore                  # Arquivo para ignorar arquivos/pastas no Git
├── package.json                # Configurações e dependências do projeto
└── README.md                   # Documentação e instruções do projeto
