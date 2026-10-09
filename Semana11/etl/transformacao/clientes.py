"""Limpeza do cadastro de clientes."""
import re

import pandas as pd

from config import REGIOES
from utils.limpeza import aparar, capitalizar, faixa_etaria, para_data


def transformar_clientes(df: pd.DataFrame, data_referencia) -> pd.DataFrame:
    df = df.apply(aparar)
    antes = len(df)
    df = df.drop_duplicates().drop_duplicates(subset="id_cliente", keep="first")
    print(f"  clientes: {antes - len(df)} duplicado(s) removido(s)")

    df["id_cliente"] = df["id_cliente"].astype(int)
    # "Dr. Gustavo", "SRA. ANA" -> "Gustavo", "Ana"
    df["nome"] = (df["nome"]
                  .str.replace(r"^(dra?|sra?)\.?\s+", "", regex=True, flags=re.I)
                  .map(capitalizar))
    df["email"] = df["email"].str.lower()
    df["telefone"] = df["telefone"].str.replace(r"\D", "", regex=True)
    df["cidade"] = df["cidade"].map(capitalizar)
    df["estado"] = df["estado"].str.upper()
    df["regiao"] = df["estado"].map(REGIOES)
    df["sexo"] = df["sexo"].str.upper()
    df["data_nascimento"] = para_data(df["data_nascimento"])
    df["data_cadastro"] = para_data(df["data_cadastro"])
    # Idade na data da última venda, para o resultado não mudar a cada dia
    df["idade"] = ((data_referencia - df["data_nascimento"]).dt.days // 365.25).astype("Int64")
    df["faixa_etaria"] = df["idade"].map(faixa_etaria)
    return df
