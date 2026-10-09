"""Etapa 3: modelo dimensional (esquema estrela) e tabela do Power BI."""
from modelagem.dimensoes import (montar_dim_cliente, montar_dim_data,
                                 montar_dim_produto, montar_dim_simples)
from modelagem.fato import montar_fato_vendas
from modelagem.powerbi import montar_powerbi
