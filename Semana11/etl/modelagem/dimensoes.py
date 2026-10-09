"""Dimensões do esquema estrela."""
import pandas as pd

from config import NOMES_DIA_SEMANA, NOMES_MES, SK_CLIENTE_DESCONHECIDO


def montar_dim_data(inicio, fim) -> pd.DataFrame:
    datas = pd.date_range(inicio, fim, freq="D")
    return pd.DataFrame({
        "sk_data": datas.strftime("%Y%m%d").astype(int),
        "data": datas,
        "ano": datas.year,
        "trimestre": datas.quarter,
        "mes": datas.month,
        "nome_mes": [NOMES_MES[m - 1] for m in datas.month],
        "ano_mes": datas.strftime("%Y-%m"),
        "dia": datas.day,
        "dia_semana": datas.dayofweek + 1,
        "nome_dia_semana": [NOMES_DIA_SEMANA[d] for d in datas.dayofweek],
        "fim_de_semana": ["Sim" if d >= 5 else "Não" for d in datas.dayofweek],
    })


def montar_dim_cliente(clientes) -> pd.DataFrame:
    # CPF, e-mail e telefone ficam fora do DW (LGPD: o BI não precisa deles)
    colunas = ["id_cliente", "nome", "sexo", "data_nascimento", "idade",
               "faixa_etaria", "cidade", "estado", "regiao", "data_cadastro"]
    dim = clientes[colunas].sort_values("id_cliente").reset_index(drop=True)
    dim.insert(0, "sk_cliente", range(1, len(dim) + 1))
    desconhecido = pd.DataFrame([{
        "sk_cliente": SK_CLIENTE_DESCONHECIDO, "id_cliente": -1,
        "nome": "Cliente Não Identificado", "sexo": "Não Informado",
        "faixa_etaria": "Não informado", "cidade": "Não Informado",
        "estado": "Não Informado", "regiao": "Não Informado",
    }])
    return pd.concat([desconhecido, dim], ignore_index=True)[["sk_cliente", *colunas]]


def montar_dim_produto(produtos) -> pd.DataFrame:
    dim = produtos.sort_values("id_produto").reset_index(drop=True)
    dim.insert(0, "sk_produto", range(1, len(dim) + 1))
    return dim


def montar_dim_simples(valores: pd.Series, nome_coluna: str, nome_sk: str) -> pd.DataFrame:
    """Dimensão de uma coluna só (forma de pagamento, canal)."""
    dim = pd.DataFrame({nome_coluna: sorted(valores.dropna().unique())})
    dim.insert(0, nome_sk, range(1, len(dim) + 1))
    return dim
