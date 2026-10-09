"""Leitura dos CSVs brutos de dados/origem."""
import pandas as pd

from config import PASTA_ORIGEM


def extrair(nome: str) -> pd.DataFrame:
    """Lê tudo como texto: a tipagem é responsabilidade da transformação."""
    return pd.read_csv(PASTA_ORIGEM / f"{nome}.csv", sep=";", dtype=str,
                       encoding="utf-8-sig", keep_default_na=False)
