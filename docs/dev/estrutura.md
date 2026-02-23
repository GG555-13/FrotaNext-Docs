# Estrutura do Projeto

O **FrotaNext** é organizado como um *monorepo* lógico, onde a raiz contém a infraestrutura (Docker) e subpastas contêm os microsserviços independentes.

Esta estrutura facilita a execução de todo o ambiente com um único comando, mantendo a separação de responsabilidades.

## 📂 Visão Geral da Raiz

```text
FrotaNext/
├── 🐳 docker-compose.yml       # Orquestrador de todos os serviços e banco
├── 📄 .env                     # Variáveis de ambiente (não comitado)
├── 🐍 reset-popula.py          # Script de automação para limpar e popular o banco
├── 🤖 teste_visual_completo.py # Script de teste E2E (Selenium)
│
├── 📁 backend/                 # Microsserviço de Regras de Negócio (Core)
├── 📁 auth-api/                # Microsserviço de Autenticação
├── 📁 frontend/                # Aplicação Web (React)
└── 📁 docs/                    # Esta documentação (MkDocs)
````

-----

## ⚙️ Backend Principal (`/backend`)

Responsável por toda a lógica de negócio de veículos, reservas e gerenciamento de frota. Segue uma arquitetura em camadas para organização.

```text
backend/
├── Dockerfile                  # Configuração da imagem Python
├── requirements.txt            # Dependências (FastAPI, SQLAlchemy, etc.)
├── alembic.ini                 # Configuração de Migrações (se utilizado)
│
├── src/                        # Código Fonte
│   ├── main.py                 # Ponto de entrada (App FastAPI e Configuração de CORS)
│   ├── database.py             # Conexão com PostgreSQL (SessionLocal)
│   │
│   ├── 🛣️ routers/             # Controllers (Rotas da API)
│   │   ├── veiculo_router.py
│   │   ├── reserva_router.py
│   │   └── ...
│   │
│   ├── 🧠 services/            # Regras de Negócio (Lógica Pura)
│   │   ├── reserva_service.py  # (Cálculo de multas, validação de datas)
│   │   └── veiculo_service.py
│   │
│   ├── 📦 models/              # Modelos do Banco (SQLAlchemy - ORM)
│   │   ├── veiculo.py          # (Tabelas: veiculos, veiculos_passeio...)
│   │   ├── reserva.py
│   │   └── pessoa.py           # (Modelos compartilhados de Pessoa)
│   │
│   └── 📑 schemas/             # Schemas de Validação (Pydantic)
│       ├── reserva_schema.py   # (Input/Output da API)
│       └── ...
│
└── tests/                      # Testes Automatizados
    ├── conftest.py             # Fixtures do Pytest (Setup do Banco)
    ├── test_unit_*.py          # Testes Unitários (Mockados)
    └── test_int_*.py           # Testes de Integração (Com banco real)
```

-----

## 🔐 Auth Service (`/auth-api`)

Serviço leve e isolado, focado exclusivamente em identidade e tokens JWT.

```text
auth-api/
├── Dockerfile
├── src/
│   ├── main.py                 # Inicialização do serviço
│   ├── seguranca.py            # Lógica de Hash (Argon2) e criação de JWT
│   │
│   ├── routers/                # Rotas de Login e Cadastro
│   │   ├── auth_router.py      # (Endpoint /token)
│   │   └── ...
│   │
│   └── services/               # Validações de usuário
└── tests/                      # Testes específicos de autenticação
```

-----

## 💻 Frontend (`/frontend`)

Aplicação SPA construída com **Vite** e **React**.

```text
frontend/
├── Dockerfile                  # Build do Node.js
├── index.html                  # Entry point do HTML
├── tailwind.config.js          # Configuração de Estilos
│
└── src/
    ├── main.tsx                # Renderização do React
    ├── App.tsx                 # Rotas principais (React Router)
    │
    ├── 🧱 components/          # Componentes Reutilizáveis
    │   ├── ui/                 # (Botões, Modais, Cards, Inputs)
    │   └── layout/             # (Navbar, Sidebar, Footer)
    │
    ├── 📄 pages/               # Telas da Aplicação
    │   ├── public/             # (Home, Login, Cadastro)
    │   ├── client/             # (Dashboard, Minhas Reservas)
    │   └── admin/              # (Gestão de Frota, Reservas)
    │
    ├── 🔌 services/            # Comunicação com Backend (Axios)
    │   ├── api.ts              # Instância do Axios com Interceptors
    │   └── authService.ts      # Chamadas para Auth API
    │
    └── 🎨 assets/              # Imagens e ícones
```

-----

## 🗄️ Banco de Dados

O banco **PostgreSQL** não possui pasta de código, pois roda a partir de uma imagem oficial Docker. Seus dados persistem no volume `frota_pg_data` (gerenciado pelo Docker).

As tabelas são criadas automaticamente pelo SQLAlchemy ao iniciar o Backend Principal (no arquivo `backend/src/main.py`).
