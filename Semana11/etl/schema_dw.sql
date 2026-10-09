-- Esquema estrela da Semana 11 (schema "dw").
-- Executado pelo etl/etl_vendas.py a cada carga: recria tudo do zero.

DROP SCHEMA IF EXISTS dw CASCADE;
CREATE SCHEMA dw;

CREATE TABLE dw.dim_data (
    sk_data          INTEGER PRIMARY KEY,      -- aaaammdd
    data             DATE NOT NULL UNIQUE,
    ano              SMALLINT NOT NULL,
    trimestre        SMALLINT NOT NULL,
    mes              SMALLINT NOT NULL,
    nome_mes         VARCHAR(20) NOT NULL,
    ano_mes          CHAR(7) NOT NULL,         -- aaaa-mm
    dia              SMALLINT NOT NULL,
    dia_semana       SMALLINT NOT NULL,        -- 1 = segunda
    nome_dia_semana  VARCHAR(20) NOT NULL,
    fim_de_semana    VARCHAR(3) NOT NULL
);

CREATE TABLE dw.dim_cliente (
    sk_cliente       INTEGER PRIMARY KEY,      -- 0 = cliente não identificado
    id_cliente       INTEGER NOT NULL,
    nome             VARCHAR(120) NOT NULL,
    sexo             VARCHAR(20),
    data_nascimento  DATE,
    idade            SMALLINT,
    faixa_etaria     VARCHAR(20),
    cidade           VARCHAR(80),
    estado           VARCHAR(20),
    regiao           VARCHAR(20),
    data_cadastro    DATE
);

CREATE TABLE dw.dim_produto (
    sk_produto       INTEGER PRIMARY KEY,
    id_produto       INTEGER NOT NULL,
    nome_produto     VARCHAR(120) NOT NULL,
    categoria        VARCHAR(60) NOT NULL,
    marca            VARCHAR(60) NOT NULL,
    preco_custo      NUMERIC(10, 2) NOT NULL,
    preco_venda      NUMERIC(10, 2) NOT NULL,
    ativo            VARCHAR(3) NOT NULL
);

CREATE TABLE dw.dim_pagamento (
    sk_pagamento     INTEGER PRIMARY KEY,
    forma_pagamento  VARCHAR(40) NOT NULL UNIQUE
);

CREATE TABLE dw.dim_canal (
    sk_canal         INTEGER PRIMARY KEY,
    canal_venda      VARCHAR(40) NOT NULL UNIQUE
);

CREATE TABLE dw.fato_vendas (
    id_venda             INTEGER PRIMARY KEY,  -- dimensão degenerada
    sk_data              INTEGER NOT NULL REFERENCES dw.dim_data (sk_data),
    sk_cliente           INTEGER NOT NULL REFERENCES dw.dim_cliente (sk_cliente),
    sk_produto           INTEGER NOT NULL REFERENCES dw.dim_produto (sk_produto),
    sk_pagamento         INTEGER NOT NULL REFERENCES dw.dim_pagamento (sk_pagamento),
    sk_canal             INTEGER NOT NULL REFERENCES dw.dim_canal (sk_canal),
    status_pagamento     VARCHAR(20) NOT NULL,
    quantidade           INTEGER NOT NULL,
    valor_unitario       NUMERIC(10, 2) NOT NULL,
    percentual_desconto  NUMERIC(5, 2) NOT NULL,
    valor_bruto          NUMERIC(12, 2) NOT NULL,
    valor_desconto       NUMERIC(12, 2) NOT NULL,
    valor_liquido        NUMERIC(12, 2) NOT NULL,
    custo_total          NUMERIC(12, 2) NOT NULL,
    lucro                NUMERIC(12, 2) NOT NULL
);

-- Fato + dimensões em uma visão só (usada pelo dashboard Streamlit)
CREATE VIEW dw.vw_vendas AS
SELECT
    f.id_venda,
    d.data              AS data_venda,
    d.ano_mes,
    c.nome              AS cliente,
    c.estado,
    c.regiao,
    p.nome_produto      AS produto,
    p.categoria,
    pg.forma_pagamento,
    cn.canal_venda,
    f.status_pagamento,
    f.quantidade,
    f.valor_liquido,
    f.custo_total,
    f.lucro
FROM dw.fato_vendas f
JOIN dw.dim_data      d  ON d.sk_data       = f.sk_data
JOIN dw.dim_cliente   c  ON c.sk_cliente    = f.sk_cliente
JOIN dw.dim_produto   p  ON p.sk_produto    = f.sk_produto
JOIN dw.dim_pagamento pg ON pg.sk_pagamento = f.sk_pagamento
JOIN dw.dim_canal     cn ON cn.sk_canal     = f.sk_canal;
