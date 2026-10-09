"""Configurações do ETL: caminhos, padrão dos CSVs e tabelas de apoio."""
from pathlib import Path

# ----------------------------------------------------------------------------
# Caminhos
# ----------------------------------------------------------------------------
PASTA_ETL = Path(__file__).resolve().parent
PASTA_BASE = PASTA_ETL.parent
PASTA_ORIGEM = PASTA_BASE / "dados" / "origem"
PASTA_DIMENSIONAL = PASTA_BASE / "dados" / "dimensional"
PASTA_LIMPOS = PASTA_BASE / "dados" / "limpos"
PASTA_POWERBI = PASTA_BASE / "dados" / "powerbi"
ARQUIVO_SCHEMA = PASTA_ETL / "schema_dw.sql"
ARQUIVO_ENV = PASTA_BASE / ".env"

# ----------------------------------------------------------------------------
# Padrão dos CSVs gerados (brasileiro)
# ----------------------------------------------------------------------------
CSV_SEP = ";"
CSV_DECIMAL = ","
CSV_DATA = "%d/%m/%Y"
CSV_ENCODING = "utf-8-sig"

# ----------------------------------------------------------------------------
# Banco de dados
# ----------------------------------------------------------------------------
SCHEMA_DW = "dw"

# Ordem de carga: dimensões antes da fato (por causa das chaves estrangeiras)
TABELAS_DIMENSIONAL = [
    "dim_data", "dim_cliente", "dim_produto", "dim_pagamento", "dim_canal",
    "fato_vendas",
]
# Colunas de data de cada tabela (para ler o CSV de volta com o tipo certo)
COLUNAS_DATA = {
    "dim_data": ["data"],
    "dim_cliente": ["data_nascimento", "data_cadastro"],
}

# Membro "desconhecido" da dim_cliente: vendas cujo cliente não existe no
# cadastro apontam para ele em vez de serem descartadas.
SK_CLIENTE_DESCONHECIDO = 0

# ----------------------------------------------------------------------------
# Tabelas de apoio
# ----------------------------------------------------------------------------
REGIOES = {
    "AC": "Norte", "AP": "Norte", "AM": "Norte", "PA": "Norte", "RO": "Norte",
    "RR": "Norte", "TO": "Norte",
    "AL": "Nordeste", "BA": "Nordeste", "CE": "Nordeste", "MA": "Nordeste",
    "PB": "Nordeste", "PE": "Nordeste", "PI": "Nordeste", "RN": "Nordeste",
    "SE": "Nordeste",
    "DF": "Centro-Oeste", "GO": "Centro-Oeste", "MT": "Centro-Oeste",
    "MS": "Centro-Oeste",
    "ES": "Sudeste", "MG": "Sudeste", "RJ": "Sudeste", "SP": "Sudeste",
    "PR": "Sul", "RS": "Sul", "SC": "Sul",
}
NOMES_MES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho",
             "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
NOMES_DIA_SEMANA = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado",
                    "Domingo"]

# Palavras que ficam minúsculas no meio de um nome ("Rio de Janeiro")
PARTICULAS = {"da", "das", "de", "do", "dos", "e", "em", "sem", "com"}
SIGLAS = {"bcaa": "BCAA"}
