import sqlite3

# Conectar ao banco de dados (se não existir, será criado)
conn = sqlite3.connect('banco_dados.db')

# Criar um cursor
cursor = conn.cursor()

# Executar o código SQL para criar as tabelas
cursor.executescript('''
CREATE TABLE IF NOT EXISTS Usuarios (
    ID_usuario INTEGER PRIMARY KEY,
    Primeiro_Nome VARCHAR(50) NOT NULL,
    Segundo_Nome VARCHAR(50) NOT NULL,
    Funcao_Estacionamento VARCHAR(50) NOT NULL,
    Login VARCHAR(50) UNIQUE NOT NULL,
    Senha VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Clientes (
    ID_cliente INTEGER PRIMARY KEY,
    Nome_cliente VARCHAR(100),
    Numero_telefone VARCHAR(20),
    Endereco VARCHAR(255),
    Email VARCHAR(100),
    CPF VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS Veiculos (
    ID_veiculo INTEGER PRIMARY KEY,
    ID_cliente INTEGER,
    Modelo_veiculo VARCHAR(50) NOT NULL,
    Placa_veiculo VARCHAR(20) NOT NULL,
    FOREIGN KEY (ID_cliente) REFERENCES Clientes(ID_cliente)
);

CREATE TABLE IF NOT EXISTS Registros_Uso_Vagas (
    ID_registro INTEGER PRIMARY KEY,
    ID_cliente INTEGER,
    ID_veiculo INTEGER,
    Data_Hora_Entrada DATETIME NOT NULL,
    Data_Hora_Saida DATETIME,
    Status_Vaga VARCHAR(20) NOT NULL,
    FOREIGN KEY (ID_cliente) REFERENCES Clientes(ID_cliente),
    FOREIGN KEY (ID_veiculo) REFERENCES Veiculos(ID_veiculo)
);

CREATE TABLE IF NOT EXISTS Registros_Pagamentos (
    ID_pagamento INTEGER PRIMARY KEY,
    ID_registro INTEGER,
    Valor_pagamento DECIMAL(10,2) NOT NULL,
    Data_Hora_Pagamento DATETIME NOT NULL,
    Tipo_Pagamento VARCHAR(20),
    FOREIGN KEY (ID_registro) REFERENCES Registros_Uso_Vagas(ID_registro)
);
                     
-- Tabela Configuracoes_Estabelecimento
CREATE TABLE IF NOT EXISTS Configuracoes_Estabelecimento (
    ID_estabelecimento INTEGER PRIMARY KEY,
    Nome_Estacionamento VARCHAR(100) NOT NULL,
    CNPJ_Estacionamento VARCHAR(20) NOT NULL,
    Email_Estacionamento VARCHAR(100) NOT NULL,
    Telefone_Estacionamento VARCHAR(20) NOT NULL,
    Endereco_Estacionamento VARCHAR(255) NOT NULL,
    Numero_Vagas INTEGER NOT NULL,
    Horario_Abertura VARCHAR(5) NOT NULL,  -- Exemplo: "08:00"
    Horario_Fechamento VARCHAR(5) NOT NULL, -- Exemplo: "18:00"
    Tarifa_Por_Hora DECIMAL(10,2) NOT NULL,
    Tarifa_Diaria DECIMAL(10,2) NOT NULL,
    Tarifa_Noturna DECIMAL(10,2) NOT NULL,
    Tarifa_Mensal DECIMAL(10,2) NOT NULL
);
''')

# Commit para salvar as alterações
conn.commit()

# Fechar a conexão
conn.close()
