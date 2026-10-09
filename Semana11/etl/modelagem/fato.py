"""Tabela fato do esquema estrela."""
import pandas as pd

from config import SK_CLIENTE_DESCONHECIDO


def montar_fato_vendas(vendas_limpas, dim_cliente, dim_produto,
                       dim_pagamento, dim_canal) -> pd.DataFrame:
    fato = (vendas_limpas
            .merge(dim_cliente[["sk_cliente", "id_cliente"]], on="id_cliente", how="left")
            .merge(dim_produto[["sk_produto", "id_produto"]], on="id_produto", how="left")
            .merge(dim_pagamento, on="forma_pagamento", how="left")
            .merge(dim_canal, on="canal_venda", how="left"))
    fato["sk_cliente"] = fato["sk_cliente"].fillna(SK_CLIENTE_DESCONHECIDO).astype(int)
    fato["sk_data"] = fato["data_venda"].dt.strftime("%Y%m%d").astype(int)
    return fato[[
        "id_venda", "sk_data", "sk_cliente", "sk_produto", "sk_pagamento",
        "sk_canal", "status_pagamento", "quantidade", "valor_unitario",
        "percentual_desconto", "valor_bruto", "valor_desconto",
        "valor_liquido", "custo_total", "lucro",
    ]]
