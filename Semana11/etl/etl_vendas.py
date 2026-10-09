"""
ETL de Vendas - Semana 11
=========================

Lê os CSVs brutos de "dados/origem" (clientes, produtos e vendas), limpa,
monta o modelo dimensional (esquema estrela) e gera:

    dados/dimensional/  -> dim_data, dim_cliente, dim_produto, dim_pagamento,
                           dim_canal e fato_vendas (CSV)
    PostgreSQL (dw)     -> os mesmos CSVs do dimensional carregados no banco,
                           mais a view dw.vw_vendas (fato + dimensões)
    dados/limpos/       -> vendas_limpas.csv: uma linha por venda com TODAS as
                           colunas limpas das 3 origens
    dados/powerbi/      -> vendas_powerbi.csv: tudo junto em uma tabela única,
                           com nomes amigáveis, pronta para o Power BI

Todos os CSVs gerados usam o padrão brasileiro: separador ";", vírgula
decimal, datas dd/mm/aaaa e UTF-8 (com BOM, para o Excel abrir acentuado).

Organização do código (este arquivo só orquestra as etapas):

    etl/
    ├── etl_vendas.py      -> pipeline (ponto de entrada)
    ├── config.py          -> caminhos, padrão dos CSVs e tabelas de apoio
    ├── schema_dw.sql      -> tabelas do esquema estrela + view
    ├── utils/             -> limpeza (texto, número, data) e leitura/gravação de CSV
    ├── extracao/          -> 1. leitura dos CSVs brutos
    ├── transformacao/     -> 2. limpeza de clientes, produtos e vendas
    ├── modelagem/         -> 3. dimensões, fato e tabela do Power BI
    └── carga/             -> 5. carga no PostgreSQL

Execução (a partir da pasta Semana11):
    python etl/etl_vendas.py              # gera os CSVs e carrega no Postgres
    python etl/etl_vendas.py --sem-banco  # só gera os CSVs
"""
import argparse
import sys

from carga import carregar_postgres
from config import PASTA_DIMENSIONAL, PASTA_LIMPOS, PASTA_POWERBI, SCHEMA_DW
from extracao import extrair
from modelagem import (montar_dim_cliente, montar_dim_data, montar_dim_produto,
                       montar_dim_simples, montar_fato_vendas, montar_powerbi)
from transformacao import (montar_vendas_limpas, transformar_clientes,
                           transformar_produtos, transformar_vendas)
from utils.arquivos import salvar_csv
from utils.limpeza import para_data


def main():
    parser = argparse.ArgumentParser(description="ETL de vendas - Semana 11")
    parser.add_argument("--sem-banco", action="store_true",
                        help="gera apenas os CSVs, sem carregar no PostgreSQL")
    args = parser.parse_args()

    print("=== 1. Extração (dados/origem) ===")
    clientes_bruto = extrair("clientes")
    produtos_bruto = extrair("produtos")
    vendas_bruto = extrair("vendas")
    print(f"  clientes: {len(clientes_bruto)} | produtos: {len(produtos_bruto)} "
          f"| vendas: {len(vendas_bruto)} linha(s)")

    print("\n=== 2. Transformação ===")
    data_referencia = para_data(vendas_bruto["data_venda"].str.strip()).max()
    clientes = transformar_clientes(clientes_bruto, data_referencia)
    produtos = transformar_produtos(produtos_bruto)
    vendas = transformar_vendas(vendas_bruto, set(clientes["id_cliente"]))
    vendas_limpas = montar_vendas_limpas(vendas, clientes, produtos)

    print("\n=== 3. Modelo dimensional ===")
    dim_data = montar_dim_data(vendas_limpas["data_venda"].min(),
                               vendas_limpas["data_venda"].max())
    dim_cliente = montar_dim_cliente(clientes)
    dim_produto = montar_dim_produto(produtos)
    dim_pagamento = montar_dim_simples(vendas_limpas["forma_pagamento"],
                                       "forma_pagamento", "sk_pagamento")
    dim_canal = montar_dim_simples(vendas_limpas["canal_venda"],
                                   "canal_venda", "sk_canal")
    fato_vendas = montar_fato_vendas(vendas_limpas, dim_cliente, dim_produto,
                                     dim_pagamento, dim_canal)

    print("\n=== 4. Gravação dos CSVs ===")
    for nome, df in [("dim_data", dim_data), ("dim_cliente", dim_cliente),
                     ("dim_produto", dim_produto), ("dim_pagamento", dim_pagamento),
                     ("dim_canal", dim_canal), ("fato_vendas", fato_vendas)]:
        salvar_csv(df, PASTA_DIMENSIONAL / f"{nome}.csv")
    salvar_csv(vendas_limpas, PASTA_LIMPOS / "vendas_limpas.csv")
    salvar_csv(montar_powerbi(vendas_limpas), PASTA_POWERBI / "vendas_powerbi.csv")

    if args.sem_banco:
        print("\n=== 5. Carga no PostgreSQL: ignorada (--sem-banco) ===")
    else:
        print(f"\n=== 5. Carga no PostgreSQL (schema {SCHEMA_DW}) ===")
        try:
            carregar_postgres()
        except Exception as erro:  # noqa: BLE001 - mensagem amigável para a aula
            print(f"\nERRO ao carregar no PostgreSQL: {erro}\n"
                  "Verifique se o banco está no ar (docker compose up -d) e o "
                  "arquivo .env. Os CSVs já foram gerados.", file=sys.stderr)
            sys.exit(1)

    print("\nETL concluído.")


if __name__ == "__main__":
    main()
