# Guia de Deploy na Nuvem (Produção)

Este guia documenta o processo completo de implantação do **FrotaNext** em um ambiente de produção real, utilizando a **Oracle Cloud Infrastructure (OCI)** e **Docker**.

---

!!! info "Preparação do Código e Testes Locais"
    Este guia foca exclusivamente na configuração da infraestrutura de nuvem (servidor, rede e publicação). Se você deseja saber com mais detalhes como baixar os repositórios, configurar a estrutura de pastas e rodar o projeto localmente para testes antes do deploy, consulte o nosso **[Guia de Instalação e Setup](../dev/instalacao.md)**.

## 🎥 Demonstração em Produção

Antes de entrarmos nos detalhes técnicos, confira o vídeo abaixo demonstrando o sistema operando em nuvem, cobrindo o ciclo completo de reserva, gestão de frota e fluxos administrativos.

!!! tip "Assista ao Vídeo da Jornada Completa"
    <div style="text-align: center; margin-top: 15px;">
      <a href="https://youtu.be/W33DMWiJJQI" target="_blank">
        <img src="https://youtu.be/W33DMWiJJQI/maxresdefault.jpg" alt="Demonstração FrotaNext" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); max-width: 100%;">
      </a>
      <p><em>Clique na imagem para assistir no YouTube.</em></p>
    </div>

---

## ☁️ 1. Infraestrutura na Oracle Cloud

O projeto foi hospedado em uma instância **Always Free** da Oracle Cloud. 

### 1.1. Configuração da Rede (VCN)
Antes de criar a máquina, é necessário configurar a rede e liberar as portas de comunicação:
1. Criação de uma **Virtual Cloud Network (VCN)** com uma Sub-rede Pública.
2. Configuração da **Security List** (Firewall da Oracle) liberando as regras de entrada (Ingress) para:
    * Porta `3000` (Frontend)
    * Porta `8000` (Backend API)
    * Porta `8001` (Auth API)
    * Porta `22` (SSH - Padrão)

### 1.2. Criação da Máquina Virtual (VM)
* **Sistema Operacional:** Canonical Ubuntu 22.04 LTS.
* **Shape:** `VM.Standard.E2.1.Micro` (AMD com 1 OCPU e 1 GB de RAM).
* **IP Público:** Atribuído automaticamente.

---

## 🛠️ 2. Preparação do Servidor (Linux)

Após acessar o servidor via SSH, o ambiente precisa ser preparado. Como a instância possui apenas 1GB de RAM, a criação de uma **Memória Swap** é obrigatória para evitar travamentos durante o build do Docker.

### 2.1. Criando Memória Swap (4GB)
```bash
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
# Garantindo que o Swap inicie com o sistema
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 2.2. Instalação do Docker

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install docker.io docker-compose-v2 -y
sudo usermod -aG docker $USER
```

*(É necessário sair e reconectar no SSH para o grupo Docker aplicar).*

---

## 🚀 3. Transferência e Configuração do Projeto

Com o servidor pronto, o código-fonte foi compactado localmente e enviado para a nuvem via `scp`:

```bash
# Na máquina local:
tar -czvf frotanext.tar.gz .
scp -i chave.key frotanext.tar.gz ubuntu@SEU_IP_PUBLICO:~
```

No servidor, os arquivos foram extraídos e as configurações de IP foram ajustadas para o ambiente de produção.

### 3.1. Ajuste de Variáveis (Frontend)

No arquivo `docker-compose.yml`, o Frontend foi configurado para apontar para o IP público do servidor:

```yaml
environment:
  - VITE_API_URL=http://SEU_IP_PUBLICO:8000
  - VITE_AUTH_API_URL=http://SEU_IP_PUBLICO:8001
```

### 3.2. Configuração de CORS (Backend e Auth)

Para que o navegador do cliente consiga se comunicar com a API, o IP público do Frontend precisou ser adicionado à lista de origens permitidas (CORS) em ambos os serviços:

```python
# Em src/main.py (Backend e Auth)
origins = [
    "http://localhost:3000",
    "http://SEU_IP_PUBLICO:3000" # Adicionado para produção
]
```

## 🟢 4. Subindo o Sistema (Deploy Final)

Com tudo configurado, o sistema foi iniciado orquestrando todos os contêineres:

```bash
docker compose up -d --build

```

Após o build (que leva alguns minutos devido às limitações de hardware), o banco de dados foi populado com as informações iniciais:

```bash
docker compose exec backend python reset-popula.py
```

!!! success "Missão Cumprida"
O sistema está no ar! Agora ele pode ser acessado de qualquer lugar através do IP público na porta 3000 (`http://SEU_IP_PUBLICO:3000`).
