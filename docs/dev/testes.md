# Guia de Testes Automatizados

O FrotaNext possui uma estratégia de testes em camadas para garantir a integridade dos microsserviços e a experiência do usuário.

!!! warning "Pré-requisito"
    Certifique-se de que os contêineres estão rodando antes de executar qualquer teste:
    ```bash
    docker compose up -d
    ```

---

## 🧪 Testes de Backend (Unitários e Integração)

Utilizamos o **Pytest** para testar as regras de negócio e endpoints das APIs. Como o ambiente é containerizado, os comandos devem ser executados via `docker compose exec`.

### Auth Service (Autenticação)
Testa fluxos de login, criação de usuários, JWT e proteção de rotas.

```bash
docker compose exec auth-service pytest -v
```

### Backend Principal (Regras de Negócio)

Testa o ciclo de vida das reservas, CRUD de veículos e cálculos financeiros.

```bash
docker compose exec backend pytest -v
```

!!! tip "Solução de Problemas (Cache)"
Se você fez alterações no código e os testes parecem estar rodando uma versão "antiga" ou falhando estranhamente, limpe o cache do Pytest:

````
```bash
docker compose exec backend pytest -v --cache-clear
docker compose exec auth-service pytest -v --cache-clear
```
````

-----

## 👁️ Testes E2E (Interface do Usuário)

Utilizamos um script em **Python + Selenium** (`teste_visual_completo.py`) que simula um usuário real navegando no sistema. Ele percorre o fluxo:

1.  **Admin:** Cadastra um veículo.
2.  **Cliente:** Faz cadastro e reserva.
3.  **Admin:** Aprova, entrega e recebe o veículo.

### 1. Preparação do Ambiente

O teste visual precisa que o usuário **Admin** já exista no banco de dados. Se você acabou de subir os containers, rode o script de população:

```bash
docker compose exec backend python reset-popula.py
```

### 2. Executando o Teste

Este teste roda na sua máquina host (fora do Docker), pois ele precisa abrir o navegador para você ver.

**Instale as dependências:**

```bash
pip install selenium
```

**Rode o script:**

```bash
python3 teste_visual_completo.py
```

**O que esperar:**

  * Uma janela do Firefox será aberta.
  * O sistema será testado automaticamente (você verá os formulários sendo preenchidos).
  * Ao final, o terminal exibirá: `✅ TESTE DE INTEGRAÇÃO TOTAL CONCLUÍDO COM SUCESSO!`.

-----

## 🐛 Solução de Erros Comuns

### Erro: "Connection Refused" no Selenium

Verifique se o Frontend está acessível em `http://localhost:3000`. Se o Docker ainda estiver subindo, aguarde alguns segundos e tente novamente.
