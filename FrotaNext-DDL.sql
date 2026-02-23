/*﻿-- --------  << FrotaNext >>  ----------
--
--                    SCRIPT DE CRIACAO (DDL)
--
-- Data Criacao ...........: 30/10/2025
-- Autor(es) ..............: Guilherme de Oliveira Mendes
-- Banco de Dados .........: PostgreSQL
-- Base de Dados (nome) ...: frota_next_postgres_db
-- Ultimas Alteracoes
--
--
--
--
-- PROJETO => 01 Base de Dados
--         => 10 Tabelas
-- 		   => 02 Papeis
-- ---------------------------------------------------------*/

-- BASE DE DADOS
CREATE DATABASE IF NOT EXISTS frota_next_postgres_db;

USE frota_next_postgres_db;

-- -----------------------------------------------------
-- 1. CRIAÇÃO DOS TIPOS (ENUMS)
-- -----------------------------------------------------

CREATE TYPE status_conta_enum AS ENUM (
    'ativo', 
    'bloqueado', 
    'pendente_confirmacao'
);

CREATE TYPE tipo_perfil_enum AS ENUM (
    'cliente_pf', 
    'cliente_pj', 
    'admin'
);

CREATE TYPE status_veiculo_enum AS ENUM (
    'disponível', 
    'reservado', 
    'alugado', 
    'em manutenção', 
    'indisponível'
);

CREATE TYPE status_reserva_enum AS ENUM (
    'pendente', 
    'confirmada', 
    'em_andamento', 
    'finalizada', 
    'cancelada'
);

CREATE TYPE tipo_veiculo_enum AS ENUM (
    'passeio', 
    'utilitario', 
    'motocicleta'
);

CREATE TYPE cor_veiculo_enum AS ENUM (
    'Preto', 
    'Branco', 
    'Prata', 
    'Cinza', 
    'Vermelho', 
    'Azul', 
    'Verde', 
    'Amarelo', 
    'Outro'
);

-- -----------------------------------------------------
-- 2. TABELA DE FUNCIONÁRIOS
-- -----------------------------------------------------
CREATE TABLE funcionarios (
    id_funcionario SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    e_admin BOOLEAN DEFAULT FALSE NOT NULL,
    e_ativado BOOLEAN DEFAULT TRUE NOT NULL
);

-- -----------------------------------------------------
-- 3. TABELA BASE 'PESSOAS' (Polimorfismo)
-- -----------------------------------------------------
CREATE TABLE pessoas (
    id_pessoa SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    telefone VARCHAR(50) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo_pessoa VARCHAR(50) NOT NULL, 
    e_ativo BOOLEAN DEFAULT TRUE NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- -----------------------------------------------------
-- 4. TABELA 'PESSOAS_JURIDICAS'
-- -----------------------------------------------------
CREATE TABLE pessoas_juridicas (
    id_pessoa INTEGER PRIMARY KEY, 
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    cnpj VARCHAR(20) NOT NULL UNIQUE,
    FOREIGN KEY (id_pessoa) REFERENCES pessoas(id_pessoa) ON DELETE CASCADE
);

-- -----------------------------------------------------
-- 5. TABELA 'PESSOAS_FISICAS'
-- -----------------------------------------------------
CREATE TABLE pessoas_fisicas (
    id_pessoa INTEGER PRIMARY KEY, 
    nome_completo VARCHAR(255) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    cnh VARCHAR(20),
    empresa_id INTEGER,
    FOREIGN KEY (id_pessoa) REFERENCES pessoas(id_pessoa) ON DELETE CASCADE,
    FOREIGN KEY (empresa_id) REFERENCES pessoas_juridicas(id_pessoa) ON DELETE SET NULL
);

-- -----------------------------------------------------
-- 6. TABELA 'ENDERECOS'
-- -----------------------------------------------------
CREATE TABLE enderecos (
    id_endereco SERIAL PRIMARY KEY,
    rua VARCHAR(255) NOT NULL,
    numero VARCHAR(50) NOT NULL,
    complemento VARCHAR(255),
    bairro VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(2) NOT NULL,
    cep VARCHAR(20) NOT NULL,
    pessoa_id INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (pessoa_id) REFERENCES pessoas(id_pessoa) ON DELETE CASCADE
);

-- -----------------------------------------------------
-- 7. TABELA BASE 'VEICULOS'
-- -----------------------------------------------------
CREATE TABLE veiculos (
    id_veiculo SERIAL PRIMARY KEY,
    placa VARCHAR(20) NOT NULL UNIQUE,
    marca VARCHAR(100) NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    cor cor_veiculo_enum NOT NULL,
    valor_diaria DOUBLE PRECISION NOT NULL,
    ano_fabricacao INTEGER NOT NULL,
    ano_modelo INTEGER NOT NULL,
    chassi VARCHAR(100) NOT NULL UNIQUE,
    renavam VARCHAR(100),
    capacidade_tanque DOUBLE PRECISION NOT NULL,
    cambio_automatico BOOLEAN DEFAULT FALSE,
    ar_condicionado BOOLEAN DEFAULT FALSE,
    imagem_url VARCHAR(500),
    status status_veiculo_enum DEFAULT 'disponível' NOT NULL,
    tipo_veiculo tipo_veiculo_enum NOT NULL 
);

-- -----------------------------------------------------
-- 8. TABELA 'VEICULOS_PASSEIO'
-- -----------------------------------------------------
CREATE TABLE veiculos_passeio (
    id_veiculo INTEGER PRIMARY KEY,
    tipo_carroceria VARCHAR(50),
    qtde_portas INTEGER NOT NULL,
    qtde_passageiros INTEGER DEFAULT 5,
    FOREIGN KEY (id_veiculo) REFERENCES veiculos(id_veiculo) ON DELETE CASCADE
);

-- -----------------------------------------------------
-- 9. TABELA 'VEICULOS_UTILITARIO'
-- -----------------------------------------------------
CREATE TABLE veiculos_utilitario (
    id_veiculo INTEGER PRIMARY KEY,
    tipo_utilitario VARCHAR(50),
    capacidade_carga_kg DOUBLE PRECISION,
    capacidade_carga_m3 DOUBLE PRECISION,
    tipo_carga VARCHAR(100),
    qtde_eixos INTEGER,
    max_passageiros INTEGER,
    FOREIGN KEY (id_veiculo) REFERENCES veiculos(id_veiculo) ON DELETE CASCADE
);

-- -----------------------------------------------------
-- 10. TABELA 'VEICULOS_MOTOCICLETA'
-- -----------------------------------------------------
CREATE TABLE veiculos_motocicleta (
    id_veiculo INTEGER PRIMARY KEY,
    cilindrada INTEGER,
    tipo_tracao VARCHAR(50),
    abs BOOLEAN DEFAULT FALSE,
    partida_eletrica BOOLEAN DEFAULT TRUE,
    modos_pilotagem VARCHAR(100),
    FOREIGN KEY (id_veiculo) REFERENCES veiculos(id_veiculo) ON DELETE CASCADE
);

-- -----------------------------------------------------
-- 11. TABELA 'RESERVAS'
-- -----------------------------------------------------
CREATE TABLE reservas (
    id_reserva SERIAL PRIMARY KEY,
    data_retirada TIMESTAMP NOT NULL,
    data_devolucao TIMESTAMP NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    valor_diaria_no_momento DOUBLE PRECISION NOT NULL,
    valor_total_estimado DOUBLE PRECISION NOT NULL,

    seguro_pessoal BOOLEAN DEFAULT FALSE NOT NULL,
    seguro_terceiros BOOLEAN DEFAULT FALSE NOT NULL,
    
    status status_reserva_enum DEFAULT 'pendente' NOT NULL,

    cliente_id INTEGER NOT NULL,
    veiculo_id INTEGER NOT NULL,
    
    motorista_id INTEGER, 
    
    FOREIGN KEY (cliente_id) REFERENCES pessoas(id_pessoa),
    FOREIGN KEY (veiculo_id) REFERENCES veiculos(id_veiculo),
    FOREIGN KEY (motorista_id) REFERENCES pessoas(id_pessoa)
);

-- -----------------------------------------------------
-- 12. ÍNDICES
-- -----------------------------------------------------
CREATE INDEX idx_veiculos_status ON veiculos (status);
CREATE INDEX idx_reservas_status ON reservas (status);
CREATE INDEX idx_reservas_cliente ON reservas(cliente_id);
CREATE INDEX idx_reservas_veiculo ON reservas(veiculo_id);
CREATE INDEX idx_pessoas_fisicas_empresa ON pessoas_fisicas(empresa_id); 
CREATE INDEX idx_reservas_data_retirada ON reservas(data_retirada);
CREATE INDEX idx_reservas_data_devolucao ON reservas(data_devolucao);
CREATE INDEX idx_enderecos_cep ON enderecos (cep);
