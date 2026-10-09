"""Limpeza do cadastro de produtos."""
import pandas as pd

from utils.limpeza import aparar, capitalizar, para_numero


def transformar_produtos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.apply(aparar)
    df["id_produto"] = df["id_produto"].astype(int)
    df["nome_produto"] = df["nome_produto"].map(capitalizar)
    df["categoria"] = df["categoria"].map(capitalizar)
    df["marca"] = df["marca"].fillna("Sem Marca")
    df["preco_custo"] = para_numero(df["preco_custo"])
    df["preco_venda"] = para_numero(df["preco_venda"])
    df["ativo"] = df["ativo"].str.upper().map({"S": "Sim", "N": "Não"})
    return df
