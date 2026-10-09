# Semana 11: ETL em Python → PostgreSQL → Streamlit e Power BI

```
dados/origem/*.csv  ──►  etl/etl_vendas.py  ──┬──►  dados/dimensional/*.csv  ──►  PostgreSQL (schema dw)
 (clientes, produtos,     (extrai, limpa,     ├──►  dados/limpos/vendas_limpas.csv
  vendas: dados sujos)     modela, carrega)   └──►  dados/powerbi/vendas_powerbi.csv

PostgreSQL ou dados/dimensional  ──►  dashboard/app.py (Streamlit: 3 KPIs + 4 gráficos)
dados/powerbi/vendas_powerbi.csv ──►  Power BI (mesmos KPIs e gráficos + DAX)
```

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `dados/origem/` | CSVs brutos, com problemas de propósito |
| `etl/etl_vendas.py` | Ponto de entrada do ETL: orquestra as etapas abaixo |
| `etl/config.py` | Caminhos, padrão dos CSVs (`;`, vírgula decimal, dd/mm/aaaa) e tabelas de apoio (regiões, meses) |
| `etl/utils/` | Funções auxiliares: limpeza de texto/número/data (`limpeza.py`) e leitura/gravação de CSV (`arquivos.py`) |
| `etl/extracao/` | 1. Leitura dos CSVs brutos de `dados/origem` |
| `etl/transformacao/` | 2. Limpeza de `clientes`, `produtos`, `vendas` e junção em `vendas_limpas` |
| `etl/modelagem/` | 3. Dimensões, tabela fato e tabela única do Power BI |
| `etl/carga/` | 5. Carga do modelo dimensional no PostgreSQL |
| `etl/schema_dw.sql` | Tabelas do esquema estrela + view `dw.vw_vendas` (executado pelo ETL) |
| `dados/dimensional/` | **Saída**: `dim_data`, `dim_cliente`, `dim_produto`, `dim_pagamento`, `dim_canal`, `fato_vendas` |
| `dados/limpos/vendas_limpas.csv` | **Saída**: uma linha por venda com **todas** as colunas limpas das 3 origens (inclui CPF, e-mail e telefone) |
| `dados/powerbi/vendas_powerbi.csv` | **Saída**: tudo junto em uma tabela, nomes amigáveis e sem dados pessoais, para o Power BI |
| `dashboard/app.py` | Dashboard Streamlit que lê o PostgreSQL **ou** os CSVs do dimensional |
| `powerbi/passo_a_passo_power_bi.md` | Como montar o mesmo dashboard no Power BI + tabelas e métricas em DAX |
| `powerbi/medidas.dax` | Todo o código DAX para copiar |

Todos os CSVs gerados usam separador `;`, vírgula decimal, datas `dd/mm/aaaa` e UTF-8.

## Como executar

Todos os comandos são rodados **dentro da pasta `Semana11`**.

```powershell
# 1. Ambiente Python (uma vez só)
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# 2. Configuração e banco (precisa do Docker Desktop aberto)
copy .env.example .env
docker compose up -d

# 3. ETL: gera os CSVs e carrega no PostgreSQL
python etl/etl_vendas.py
#    (sem banco? python etl/etl_vendas.py --sem-banco gera só os CSVs)

# 4. Dashboard: abre em http://localhost:8501
streamlit run dashboard/app.py
```

O PostgreSQL fica na porta **5435** (banco `vendas_dw`, usuário/senha `postgres`), para não conflitar com a Semana 10 (5434) nem com um PostgreSQL instalado no Windows (5432). Para conectar pelo DBeaver/pgAdmin use esses mesmos dados.

## O que o ETL limpa

| Problema na origem | Tratamento |
|---|---|
| Espaços sobrando e maiúsculas/minúsculas misturadas (`" PIX "`, `"cartão de crédito"`, `"SP  "`) | `strip` + padronização (`Pix`, `Cartão de Crédito`, `SP`) |
| Pronomes de tratamento no nome (`DR. GUSTAVO`, `Sra. Ana`) | Removidos; nome em formato próprio (`Gustavo Henrique Rios`) |
| Clientes e vendas duplicados (6 e 12 linhas) | Removidos |
| Venda sem quantidade ou com quantidade 0 (56 linhas) | Descartadas |
| Desconto vazio | Vira 0% |
| Status de pagamento vazio | `Não Informado` |
| Produto sem marca | `Sem Marca` |
| Venda de cliente que não está no cadastro (8 linhas, ids 1100 a 1107) | Mantida, ligada ao membro `Cliente Não Identificado` (`sk_cliente = 0`) da `dim_cliente` |
| Números `129,90` e datas `dd/mm/aaaa` como texto | Convertidos para número e data |

Resultado: 3.012 vendas brutas viram **2.944 vendas limpas**.

## Modelo dimensional (schema `dw`)

```
                 dim_data            dim_cliente
                 (sk_data)           (sk_cliente)
                      \                 /
  dim_pagamento ── fato_vendas ── dim_produto
  (sk_pagamento)   (id_venda)      (sk_produto)
                       |
                   dim_canal
                   (sk_canal)
```

A fato guarda as chaves das dimensões, o `status_pagamento` e os valores: `quantidade`, `valor_unitario`, `percentual_desconto`, `valor_bruto`, `valor_desconto`, `valor_liquido`, `custo_total` e `lucro`. A view `dw.vw_vendas` junta a fato com as dimensões e é ela que o Streamlit lê.

## KPIs (iguais no Streamlit e no Power BI)

Considerando só vendas com status **Pago**:

| KPI | Valor |
|---|---|
| Faturamento (valor líquido) | R$ 367.498,32 |
| Vendas pagas | 2.385 |
| Ticket médio | R$ 154,09 |

Gráficos: faturamento por mês, por categoria, por canal de venda e top 10 produtos.
