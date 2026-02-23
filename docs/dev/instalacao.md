# Guia de Instalação e Setup

Este guia descreve como configurar o ambiente de desenvolvimento do **FrotaNext** localmente.

Como utilizamos Docker e conteinerização em todo o projeto, você não precisa instalar Python, Node.js ou PostgreSQL na sua máquina local, apenas o Docker.

## 📋 Pré-requisitos

* **[Docker Desktop](https://www.docker.com/products/docker-desktop/)** (ou Engine + Compose no Linux).
* **[Git](https://git-scm.com/)**.

---

## 🚀 Passo a Passo

### 1. Clonar o Repositório Base (Orquestrador)

O projeto adota o padrão *Multi-repo*. Primeiro, você deve clonar este repositório principal, que contém a orquestração do Docker, scripts de banco de dados e a documentação.

Abra o terminal e execute:

```bash
git clone https://github.com/GG555-13/FrotaNext-Docs.git FrotaNext

cd FrotaNext
```

### 2. Baixar os Microsserviços

Agora, dentro da pasta `FrotaNext`, você precisará clonar os outros três repositórios que compõem o sistema.

⚠️ **Atenção:** É crucial que as pastas sejam criadas com os nomes exatos fornecidos nos comandos abaixo, pois o `docker-compose.yml` mapeia a construção das imagens através desses nomes.

```bash
# 1. Baixando o Backend Principal
git clone https://github.com/GG555-13/FrotaNext-Backend.git FrotaNext-Backend-main

# 2. Baixando o Auth Service
git clone https://github.com/GG555-13/FrotaNext-Auth.git FrotaNext-Auth-main

# 3. Baixando o Frontend React
git clone https://github.com/GG555-13/FrotaNext-Frontend.git FrotaNext-Frontend-main
```

!!! info "Estrutura Final Esperada"
Após clonar os 4 repositórios, sua pasta base deve ter a seguinte estrutura:
```text
    FrotaNext/
    │
    ├── docker-compose.yml           <-- Arquivo principal 
    ├── reset-popula.py              <-- Script de banco de dados
    │
    ├── FrotaNext-Backend-main/      <-- Pasta do Backend 
    ├── FrotaNext-Auth-main/         <-- Pasta do serviço de Autenticação
    └── FrotaNext-Frontend-main/     <-- Pasta do site em React
```

### 3. Subir a Aplicação

Com todas as peças no lugar, basta pedir para o Docker construir as imagens e rodar os contêineres simultaneamente:

```bash
docker compose up -d --build
```

O processo de build pode levar alguns minutos na primeira vez, pois o Docker baixará as dependências do Node e do Python.

!!! success "Acesso aos Serviços Locais"
Após o comando finalizar, os serviços estarão disponíveis em:

* **Frontend (Aplicação):** [http://localhost:3000](http://localhost:3000)
* **Backend Principal (Swagger API):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Auth Service (Swagger API):** [http://localhost:8001/docs](http://localhost:8001/docs)


## 🌱 População do Banco de Dados

Ao subir os contêineres pela primeira vez, o banco de dados PostgreSQL será criado, mas estará vazio.

Para facilitar os testes, criamos um script de automação (`reset-popula.py`) que cria o usuário administrador e cadastra veículos de teste.

Execute o comando abaixo no seu terminal (na raiz do projeto):


```bash
docker compose exec backend python reset-popula.py
```

O script executará as seguintes ações:

1. Limpeza e recriação das tabelas (para garantir um estado limpo).
2. Criação do usuário **Admin Root** (Email: `admin@frotanext.com` | Senha: `admin123`).
3. Cadastro de uma frota inicial de veículos prontos para reserva.

---

## 🛑 Comandos do Dia a Dia

Aqui estão os principais comandos do Docker Compose para gerenciar o projeto:

| Ação | Comando |
| --- | --- |
| **Parar todos os serviços** | `docker compose down` |
| **Ver logs em tempo real (todos)** | `docker compose logs -f` |
| **Ver logs de um serviço específico** | `docker compose logs -f frontend` |
| **Reiniciar serviços** | `docker compose restart backend auth-service` |
| **Resetar o banco (apagar os dados)** | `docker compose down -v` |

