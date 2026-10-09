"""Junção das 3 origens limpas em uma tabela única de vendas."""
import pandas as pd


def montar_vendas_limpas(vendas, clientes, produtos) -> pd.DataFrame:
    """Uma linha por venda, com todas as colunas limpas das 3 origens e os
    valores calculados."""
    df = (vendas
          .merge(clientes, on="id_cliente", how="left")
          .merge(produtos, on="id_produto", how="left"))
    df["nome"] = df["nome"].fillna("Cliente Não Identificado")
    for coluna in ["cidade", "estado", "regiao", "sexo"]:
        df[coluna] = df[coluna].fillna("Não Informado")
    df["faixa_etaria"] = df["faixa_etaria"].fillna("Não informado")

    df["valor_bruto"] = (df["quantidade"] * df["valor_unitario"]).round(2)
    df["valor_desconto"] = (df["valor_bruto"] * df["percentual_desconto"] / 100).round(2)
    df["valor_liquido"] = (df["valor_bruto"] - df["valor_desconto"]).round(2)
    df["custo_total"] = (df["quantidade"] * df["preco_custo"]).round(2)
    df["lucro"] = (df["valor_liquido"] - df["custo_total"]).round(2)
    return df.sort_values("id_venda").reset_index(drop=True)
