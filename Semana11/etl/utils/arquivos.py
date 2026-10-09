"""Leitura e gravação dos CSVs gerados pelo ETL (padrão brasileiro)."""
from pathlib import Path

import pandas as pd

from config import CSV_DATA, CSV_DECIMAL, CSV_ENCODING, CSV_SEP, PASTA_BASE


def salvar_csv(df: pd.DataFrame, caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(caminho, sep=CSV_SEP, decimal=CSV_DECIMAL, date_format=CSV_DATA,
              float_format="%.2f", encoding=CSV_ENCODING, index=False)
    print(f"  {caminho.relative_to(PASTA_BASE)}: {len(df)} linha(s)")


def ler_csv(caminho: Path, colunas_data=()) -> pd.DataFrame:
    df = pd.read_csv(caminho, sep=CSV_SEP, decimal=CSV_DECIMAL,
                     encoding=CSV_ENCODING)
    for coluna in colunas_data:
        df[coluna] = pd.to_datetime(df[coluna], format=CSV_DATA)
    return df
