"""Carga dos CSVs de dados/dimensional no PostgreSQL (schema dw)."""
import os

from config import (ARQUIVO_ENV, ARQUIVO_SCHEMA, COLUNAS_DATA,
                    PASTA_DIMENSIONAL, SCHEMA_DW, TABELAS_DIMENSIONAL)
from utils.arquivos import ler_csv


def obter_engine():
    from dotenv import load_dotenv
    from sqlalchemy import create_engine
    from sqlalchemy.engine import URL

    load_dotenv(ARQUIVO_ENV)
    url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5435")),
        database=os.getenv("DB_NAME", "vendas_dw"),
    )
    return create_engine(url)


def carregar_postgres() -> None:
    """Recria o schema dw e carrega nele os CSVs de dados/dimensional."""
    from sqlalchemy import text

    engine = obter_engine()
    with engine.begin() as conexao:
        conexao.execute(text(ARQUIVO_SCHEMA.read_text(encoding="utf-8")))
        for tabela in TABELAS_DIMENSIONAL:
            df = ler_csv(PASTA_DIMENSIONAL / f"{tabela}.csv",
                         COLUNAS_DATA.get(tabela, ()))
            df.to_sql(tabela, conexao, schema=SCHEMA_DW, if_exists="append",
                      index=False, method="multi", chunksize=1000)
            print(f"  {SCHEMA_DW}.{tabela}: {len(df)} linha(s)")
