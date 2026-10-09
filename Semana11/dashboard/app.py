"""
Dashboard de Vendas - Semana 11
===============================

3 KPIs e 4 gráficos sobre o resultado do ETL. A fonte é escolhida na barra
lateral:

    PostgreSQL -> view dw.vw_vendas (carregada pelo etl/etl_vendas.py)
    CSV        -> arquivos de dados/dimensional (fato + dimensões)

As duas fontes têm os mesmos dados, então os números devem ser iguais.
Os KPIs consideram apenas vendas com status "Pago".

Execução (a partir da pasta Semana11):
    streamlit run dashboard/app.py
"""
import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

PASTA_BASE = Path(__file__).resolve().parent.parent
PASTA_DIMENSIONAL = PASTA_BASE / "dados" / "dimensional"
COR = "#2a78d6"

st.set_page_config(page_title="Dashboard de Vendas", layout="wide")


# ----------------------------------------------------------------------------
# Leitura dos dados (as duas funções devolvem as mesmas colunas)
# ----------------------------------------------------------------------------
@st.cache_data
def ler_postgres() -> pd.DataFrame:
    from dotenv import load_dotenv
    from sqlalchemy import create_engine
    from sqlalchemy.engine import URL

    load_dotenv(PASTA_BASE / ".env")
    url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5435")),
        database=os.getenv("DB_NAME", "vendas_dw"),
    )
    sql = """
        SELECT data_venda, ano_mes, produto, categoria, canal_venda,
               status_pagamento, valor_liquido
        FROM dw.vw_vendas
    """
    df = pd.read_sql(sql, create_engine(url), parse_dates=["data_venda"])
    df["valor_liquido"] = df["valor_liquido"].astype(float)  # NUMERIC -> float
    return df


@st.cache_data
def ler_csv() -> pd.DataFrame:
    def ler(nome):
        return pd.read_csv(PASTA_DIMENSIONAL / f"{nome}.csv", sep=";",
                           decimal=",", encoding="utf-8-sig")

    # Mesmo JOIN da view dw.vw_vendas, feito com pandas
    df = (ler("fato_vendas")
          .merge(ler("dim_data"), on="sk_data")
          .merge(ler("dim_produto"), on="sk_produto")
          .merge(ler("dim_canal"), on="sk_canal"))
    df["data_venda"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
    df = df.rename(columns={"nome_produto": "produto"})
    return df[["data_venda", "ano_mes", "produto", "categoria", "canal_venda",
               "status_pagamento", "valor_liquido"]]


def moeda(valor: float) -> str:
    """1234.5 -> 'R$ 1.234,50'"""
    return "R$ " + f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def grafico_barras(df, x, y, titulo, horizontal=False):
    if horizontal:
        fig = px.bar(df, x=y, y=x, orientation="h")
        fig.update_yaxes(title=None, categoryorder="total ascending")
        fig.update_xaxes(title=None, tickprefix="R$ ")
    else:
        fig = px.bar(df, x=x, y=y)
        fig.update_xaxes(title=None)
        fig.update_yaxes(title=None, tickprefix="R$ ")
    fig.update_traces(marker_color=COR,
                      hovertemplate="%{label}<br>R$ %{value:,.2f}<extra></extra>")
    return estilizar(fig, titulo)


def estilizar(fig, titulo):
    fig.update_layout(title=titulo, separators=",.", height=360,
                      margin=dict(l=10, r=10, t=50, b=10), bargap=0.3)
    return fig


# ----------------------------------------------------------------------------
# Barra lateral: fonte de dados
# ----------------------------------------------------------------------------
st.sidebar.header("Fonte de dados")
fonte = st.sidebar.radio("Ler os dados de:",
                         ["PostgreSQL (dw.vw_vendas)", "CSV (dados/dimensional)"])
if st.sidebar.button("Recarregar dados"):
    st.cache_data.clear()

try:
    dados = ler_postgres() if fonte.startswith("PostgreSQL") else ler_csv()
except Exception as erro:  # noqa: BLE001 - mensagem amigável para a aula
    st.error(f"Não foi possível ler os dados de **{fonte}**.\n\n"
             "Rode o ETL antes (`python etl/etl_vendas.py`) e, para o "
             "PostgreSQL, confira se o banco está no ar (`docker compose up -d`).")
    st.exception(erro)
    st.stop()

pagas = dados[dados["status_pagamento"] == "Pago"]

# ----------------------------------------------------------------------------
# KPIs
# ----------------------------------------------------------------------------
st.title("Dashboard de Vendas")
st.caption(f"Fonte: {fonte} · {len(dados):,} vendas no total · "
           f"KPIs e gráficos consideram apenas vendas pagas".replace(",", "."))

faturamento = pagas["valor_liquido"].sum()
qtd_vendas = len(pagas)
ticket_medio = faturamento / qtd_vendas if qtd_vendas else 0

k1, k2, k3 = st.columns(3)
k1.metric("Faturamento", moeda(faturamento), border=True)
k2.metric("Vendas pagas", f"{qtd_vendas:,}".replace(",", "."), border=True)
k3.metric("Ticket médio", moeda(ticket_medio), border=True)

# ----------------------------------------------------------------------------
# Gráficos
# ----------------------------------------------------------------------------
por_mes = pagas.groupby("ano_mes", as_index=False)["valor_liquido"].sum()
fig_mes = px.line(por_mes, x="ano_mes", y="valor_liquido", markers=True)
fig_mes.update_traces(line=dict(color=COR, width=2), marker=dict(size=8),
                      hovertemplate="%{x}<br>R$ %{y:,.2f}<extra></extra>")
fig_mes.update_xaxes(title=None, type="category")
fig_mes.update_yaxes(title=None, tickprefix="R$ ", rangemode="tozero")
estilizar(fig_mes, "Faturamento por mês")

por_categoria = pagas.groupby("categoria", as_index=False)["valor_liquido"].sum()
por_canal = (pagas.groupby("canal_venda", as_index=False)["valor_liquido"].sum()
             .sort_values("valor_liquido", ascending=False))
top_produtos = (pagas.groupby("produto", as_index=False)["valor_liquido"].sum()
                .nlargest(10, "valor_liquido"))

g1, g2 = st.columns(2)
g1.plotly_chart(fig_mes, width="stretch")
g2.plotly_chart(grafico_barras(por_categoria, "categoria", "valor_liquido",
                               "Faturamento por categoria", horizontal=True),
                width="stretch")

g3, g4 = st.columns(2)
g3.plotly_chart(grafico_barras(por_canal, "canal_venda", "valor_liquido",
                               "Faturamento por canal de venda"),
                width="stretch")
g4.plotly_chart(grafico_barras(top_produtos, "produto", "valor_liquido",
                               "Top 10 produtos por faturamento", horizontal=True),
                width="stretch")
