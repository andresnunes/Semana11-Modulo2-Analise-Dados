"""Limpeza das vendas."""
import pandas as pd

from utils.limpeza import aparar, capitalizar, para_data, para_numero


def transformar_vendas(df: pd.DataFrame, ids_clientes) -> pd.DataFrame:
    df = df.apply(aparar)
    antes = len(df)
    df = df.drop_duplicates().drop_duplicates(subset="id_venda", keep="first")
    print(f"  vendas: {antes - len(df)} duplicada(s) removida(s)")

    df["id_venda"] = df["id_venda"].astype(int)
    df["id_cliente"] = df["id_cliente"].astype(int)
    df["id_produto"] = df["id_produto"].astype(int)
    df["data_venda"] = para_data(df["data_venda"])
    df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce")
    df["valor_unitario"] = para_numero(df["valor_unitario"])
    df["percentual_desconto"] = pd.to_numeric(df["percentual_desconto"]).fillna(0)

    # Venda sem quantidade (vazia ou zero) não tem valor: é descartada
    invalidas = df["quantidade"].isna() | (df["quantidade"] <= 0)
    print(f"  vendas: {invalidas.sum()} sem quantidade válida removida(s)")
    df = df[~invalidas].copy()
    df["quantidade"] = df["quantidade"].astype(int)

    for coluna in ["forma_pagamento", "status_pagamento", "canal_venda"]:
        df[coluna] = df[coluna].map(capitalizar)
    df["status_pagamento"] = df["status_pagamento"].fillna("Não Informado")

    orfas = ~df["id_cliente"].isin(ids_clientes)
    print(f"  vendas: {orfas.sum()} com cliente fora do cadastro "
          f"(mantidas como 'Cliente Não Identificado')")
    return df
