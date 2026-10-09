"""Tabela única (desnormalizada) para o Power BI."""
import pandas as pd

from config import NOMES_MES


def montar_powerbi(vendas_limpas) -> pd.DataFrame:
    """Tabela única para o Power BI: nomes amigáveis, sem dados pessoais."""
    df = vendas_limpas
    return pd.DataFrame({
        "ID Venda": df["id_venda"],
        "Data da Venda": df["data_venda"],
        "Ano": df["data_venda"].dt.year,
        "Mês Número": df["data_venda"].dt.month,
        "Mês": df["data_venda"].dt.month.map(lambda m: NOMES_MES[m - 1]),
        "Ano-Mês": df["data_venda"].dt.strftime("%Y-%m"),
        "Cliente": df["nome"],
        "Sexo": df["sexo"],
        "Faixa Etária": df["faixa_etaria"],
        "Cidade": df["cidade"],
        "Estado": df["estado"],
        "Região": df["regiao"],
        "Produto": df["nome_produto"],
        "Categoria": df["categoria"],
        "Marca": df["marca"],
        "Forma de Pagamento": df["forma_pagamento"],
        "Status Pagamento": df["status_pagamento"],
        "Canal de Venda": df["canal_venda"],
        "Quantidade": df["quantidade"],
        "Valor Unitário": df["valor_unitario"],
        "% Desconto": df["percentual_desconto"],
        "Valor Bruto": df["valor_bruto"],
        "Valor Desconto": df["valor_desconto"],
        "Valor Líquido": df["valor_liquido"],
        "Custo Total": df["custo_total"],
        "Lucro": df["lucro"],
    })
