# Power BI: dashboard de vendas + DAX

Neste exemplo montamos no **Power BI Desktop** o mesmo dashboard do Streamlit (3 KPIs e 4 gráficos) e depois usamos **DAX** para criar tabelas separadas e 3 métricas customizadas.

| O quê | Onde |
|---|---|
| Arquivo de dados | `dados/powerbi/vendas_powerbi.csv` (gerado pelo ETL: `python etl/etl_vendas.py`) |
| Todo o código DAX (para copiar) | [`medidas.dax`](medidas.dax) |

O CSV já vem **limpo** e com **tudo junto** em uma tabela só (vendas + cliente + produto): uma linha por venda, separador **`;`**, **vírgula** decimal, datas **dd/mm/aaaa**, **UTF-8**.

### Fluxo

```
 Parte 1           Parte 2             Parte 3              Parte 4            Parte 5
 Importar CSV ──►  Tabela _Medidas ──► KPIs e gráficos ──►  Tabela Calendario ► 3 métricas DAX
 (Power Query)     (tabela separada)   (igual ao Streamlit) (tabela calculada)  + gráficos
```

> **Regra dos números:** como no Streamlit, os KPIs consideram só vendas com **Status Pagamento = "Pago"**. Cada medida abaixo traz o **valor esperado** para você conferir.

---

## Parte 1: Importar o CSV

| # | Onde | Ação |
|---|---|---|
| 1 | Página Inicial | **Obter Dados** > **Texto/CSV** > escolha `dados/powerbi/vendas_powerbi.csv` |
| 2 | Janela de visualização | **Origem do Arquivo**: `65001: Unicode (UTF-8)` · **Delimitador**: `Ponto e vírgula` |
| 3 | Janela de visualização | Clique em **Transformar Dados** (abre o Power Query) |
| 4 | Power Query > Consultas | Renomeie a consulta `vendas_powerbi` para **`Vendas`** (duplo clique no nome) |
| 5 | Power Query > Grade | Confira os tipos no cabeçalho: `Data da Venda` = **Data** 📅; `Valor Líquido`, `Custo Total`, `Lucro`, `Valor Unitário` = **Número decimal** (1.2); `Quantidade`, `Ano` = **Número inteiro** (123) |
| 6 | Página Inicial | **Fechar e Aplicar** |

> **Power BI em inglês?** Se as datas ou os decimais vierem errados (ex.: `129,9` virando `1299`), no Power Query clique com o botão direito na coluna > **Alterar Tipo** > **Usando Localidade…** > tipo `Número decimal` (ou `Data`) e localidade **Português (Brasil)**.

---

## Parte 2: Tabela separada para as medidas (`_Medidas`)

Medidas podem morar em qualquer tabela, mas o costume é criar uma **tabela só para elas**, que fica no topo do painel Dados.

| # | Onde | Ação |
|---|---|---|
| 1 | Página Inicial | **Inserir Dados** (Enter Data) |
| 2 | Janela "Criar Tabela" | **Nome**: `_Medidas` · não digite nada na grade · **Carregar** |
| 3 | Painel Dados | A tabela `_Medidas` aparece com uma coluna `Coluna1`. Ela será ocultada no passo 5 |
| 4 | Painel Dados | Clique em `_Medidas` > **Nova Medida** e crie as medidas da Parte 3 |
| 5 | Painel Dados | Depois da 1ª medida: botão direito em `Coluna1` > **Ocultar** (ou **Excluir**). O ícone da tabela vira uma calculadora 🖩 e ela sobe para o topo |

> O `_` no início do nome é só para ela aparecer primeiro na lista (ordem alfabética).

---

## Parte 3: KPIs e gráficos (o mesmo dashboard do Streamlit)

### 3.1 Medidas dos KPIs

Selecione a tabela `_Medidas` > **Nova Medida**, cole cada fórmula na barra de fórmulas e tecle **Enter**:

```dax
Faturamento =
CALCULATE (
    SUM ( Vendas[Valor Líquido] ),
    Vendas[Status Pagamento] = "Pago"
)
```

```dax
Vendas Pagas =
CALCULATE (
    COUNTROWS ( Vendas ),
    Vendas[Status Pagamento] = "Pago"
)
```

```dax
Ticket Médio =
DIVIDE ( [Faturamento], [Vendas Pagas] )
```

**Formatação** (selecione a medida > guia **Ferramentas de medida**):

| Medida | Formato | Esperado |
|---|---|---|
| Faturamento | Moeda (R$), 2 casas | **R$ 367.498,32** |
| Vendas Pagas | Número inteiro, separador de milhar | **2.385** |
| Ticket Médio | Moeda (R$), 2 casas | **R$ 154,09** |

> **Por que `CALCULATE`?** `SUM(Vendas[Valor Líquido])` somaria também as vendas canceladas e pendentes. O `CALCULATE` recalcula a soma com um filtro extra: só as linhas com status "Pago".
>
> **Por que `DIVIDE` e não `/`?** `DIVIDE` devolve vazio em vez de erro quando o denominador é zero.

### 3.2 Os 3 cartões de KPI

| # | Visual (painel Visualizações) | Campo |
|---|---|---|
| 1 | **Cartão** | `_Medidas[Faturamento]` |
| 2 | **Cartão** | `_Medidas[Vendas Pagas]` |
| 3 | **Cartão** | `_Medidas[Ticket Médio]` |

Coloque os três lado a lado no topo da página.

### 3.3 Os 4 gráficos

| # | Título | Visual | Eixo / Categoria | Valores |
|---|---|---|---|---|
| 1 | Faturamento por mês | **Gráfico de linhas** | `Vendas[Ano-Mês]` | `[Faturamento]` |
| 2 | Faturamento por categoria | **Gráfico de barras clusterizado** (horizontal) | `Vendas[Categoria]` | `[Faturamento]` |
| 3 | Faturamento por canal de venda | **Gráfico de colunas clusterizado** | `Vendas[Canal de Venda]` | `[Faturamento]` |
| 4 | Top 10 produtos por faturamento | **Gráfico de barras clusterizado** | `Vendas[Produto]` | `[Faturamento]` |

Ajustes:

- **Gráfico 1:** no eixo X, clique nos `...` do visual > **Classificar eixo** > `Ano-Mês` > **Crescente** (o formato `aaaa-mm` já ordena certo). Em **Formatar** > **Eixo X**, mude o **Tipo** para **Categórico** para mostrar todos os meses.
- **Gráficos 2, 3 e 4:** `...` > **Classificar eixo** > `Faturamento` > **Decrescente**.
- **Gráfico 4 (Top 10):** painel **Filtros** > arraste `Vendas[Produto]` para *Filtros neste visual* > **Tipo de filtro**: `N superior` > **Mostrar itens**: `Superior 10` > **Por valor**: `[Faturamento]` > **Aplicar filtro**.

Confira com o Streamlit: Suplementos é a maior categoria e "Whey Protein Isolado 900g" é o produto nº 1.

---

## Parte 4: Tabela calculada `Calendario` (DAX)

Para comparar **com o ano anterior** o DAX precisa de uma tabela de datas contínua: um dia por linha, sem buracos. Vamos criá-la **com DAX**, sem nenhum arquivo.

| # | Onde | Ação |
|---|---|---|
| 1 | Modelagem | **Nova Tabela** |
| 2 | Barra de fórmulas | Cole a fórmula abaixo e tecle **Enter** |

```dax
Calendario =
VAR PrimeiroAno = YEAR ( MIN ( Vendas[Data da Venda] ) )
VAR UltimoAno = YEAR ( MAX ( Vendas[Data da Venda] ) )
VAR Datas =
    CALENDAR ( DATE ( PrimeiroAno, 1, 1 ), DATE ( UltimoAno, 12, 31 ) )
RETURN
    ADDCOLUMNS (
        SELECTCOLUMNS ( Datas, "Data", [Date] ),
        "Ano", YEAR ( [Data] ),
        "Mês Número", MONTH ( [Data] ),
        "Mês", FORMAT ( [Data], "mmm" ),
        "Ano-Mês", FORMAT ( [Data], "yyyy-mm" ),
        "Trimestre", "T" & QUARTER ( [Data] )
    )
```

O que cada parte faz:

| Trecho | Função |
|---|---|
| `VAR ... RETURN` | Variáveis: guardam um valor para usar depois e deixam a fórmula legível |
| `CALENDAR(início, fim)` | Gera uma tabela com uma coluna `[Date]`, um dia por linha |
| `SELECTCOLUMNS(..., "Data", [Date])` | Renomeia a coluna `Date` para `Data` |
| `ADDCOLUMNS(...)` | Acrescenta colunas calculadas (ano, mês…) a partir da data |

Resultado: 730 linhas (01/01/2025 a 31/12/2026). Agora configure:

| # | Onde | Ação |
|---|---|---|
| 3 | Painel Dados | Botão direito em `Calendario` > **Marcar como tabela de datas** > coluna **Data** > **OK** |
| 4 | Exibição de tabela | Selecione a coluna `Calendario[Mês]` > **Ferramentas de coluna** > **Classificar por coluna** > `Mês Número` (senão os meses ficam em ordem alfabética: abr, ago, dez…) |
| 5 | Exibição de modelo | Arraste `Calendario[Data]` até `Vendas[Data da Venda]`. Confira: **Um para muitos (1:\*)**, direção do filtro **Única** |

> Se o mês aparecer como `Jan` em vez de `jan`, é só o idioma do modelo (Arquivo > Opções > Configurações regionais). Não muda nada nos cálculos.

### Bônus: outra tabela calculada, a `Resumo Categoria`

Uma tabela calculada também pode **resumir** dados usando medidas. Crie **depois** das medidas da Parte 5 (ela usa `[Margem %]`):

```dax
Resumo Categoria =
SUMMARIZECOLUMNS (
    Vendas[Categoria],
    "Faturamento", [Faturamento],
    "Vendas Pagas", [Vendas Pagas],
    "Margem %", [Margem %]
)
```

Ela tem 5 linhas (uma por categoria) e pode ser mostrada num visual **Tabela**. Diferença importante: tabelas calculadas são calculadas **uma vez**, ao atualizar os dados, e **não** reagem às segmentações. As medidas são recalculadas a cada clique.

---

## Parte 5: 3 métricas customizadas com DAX

Crie as três na tabela `_Medidas` (**Nova Medida**).

### Métrica 1: Margem % (função iteradora `SUMX`)

```dax
Margem % =
VAR Lucro =
    CALCULATE (
        SUMX ( Vendas, Vendas[Valor Líquido] - Vendas[Custo Total] ),
        Vendas[Status Pagamento] = "Pago"
    )
RETURN
    DIVIDE ( Lucro, [Faturamento] )
```

- **`SUMX`** percorre a tabela **linha a linha**, calcula `Valor Líquido - Custo Total` em cada venda e soma os resultados. `SUM` só soma uma coluna pronta; `SUMX` soma uma **expressão**.
- **Formato:** Porcentagem, 2 casas. **Esperado:** **47,83%**.

**Gráfico:** **Gráfico de barras clusterizado** · Eixo Y: `Vendas[Categoria]` · Eixo X: `[Margem %]` · classificar por `Margem %` decrescente.
Esperado: Acessórios **60,38%** (maior), Suplementos **39,53%** (menor). Repare que Suplementos é a categoria que **mais fatura** e a que tem a **menor margem**.

### Métrica 2: Crescimento YoY % (inteligência de tempo)

YoY = *year over year*: compara com o mesmo período do ano anterior. Precisa da tabela `Calendario` da Parte 4.

```dax
Crescimento YoY % =
VAR UltimaVenda =
    CALCULATE ( MAX ( Vendas[Data da Venda] ), REMOVEFILTERS () )
VAR Atual = [Faturamento]
VAR AnoAnterior =
    CALCULATE (
        [Faturamento],
        SAMEPERIODLASTYEAR ( Calendario[Data] ),
        Calendario[Data] <= EDATE ( UltimaVenda, -12 )
    )
RETURN
    IF (
        HASONEVALUE ( Calendario[Ano] ) && NOT ISBLANK ( Atual ),
        DIVIDE ( Atual - AnoAnterior, AnoAnterior )
    )
```

| Trecho | Função |
|---|---|
| `SAMEPERIODLASTYEAR(Calendario[Data])` | Troca as datas do filtro atual pelas mesmas datas um ano antes |
| `REMOVEFILTERS()` | Ignora todos os filtros: `UltimaVenda` é sempre a última venda do arquivo (31/08/2026) |
| `Calendario[Data] <= EDATE(UltimaVenda, -12)` | Corta o ano anterior em 31/08/2025. Os dados de 2026 vão só até agosto, então sem esse corte 2026 (8 meses) seria comparado com 2025 inteiro (12 meses) |
| `HASONEVALUE(Calendario[Ano])` | Só mostra o resultado quando há **um** ano no contexto. No total geral (2025 + 2026 juntos) a comparação não faz sentido |

- **Formato:** Porcentagem, 2 casas.

**Cartão + segmentação:**

| # | Visual | Campo |
|---|---|---|
| 1 | **Segmentação de dados** | `Calendario[Ano]` → selecione **2026** |
| 2 | **Cartão** | `[Crescimento YoY %]` → esperado **10,83%** (jan–ago/2026 contra jan–ago/2025) |

**Gráfico:** **Gráfico de colunas clusterizado** · Eixo X: `Calendario[Mês]` · Eixo Y: `[Crescimento YoY %]` · com a segmentação em 2026.
Esperado: fev **+82,65%** (maior alta), abr **−18,77%** (maior queda), ago **+28,89%**. Set a dez ficam vazios: ainda não há vendas.

> Dica: em **Formatar** > **Colunas** > **Cores** > **fx** (formatação condicional), use uma regra: valor < 0 em vermelho, ≥ 0 em verde.

### Métrica 3: Taxa de Cancelamento % (`CALCULATE` só no numerador)

```dax
Taxa de Cancelamento % =
DIVIDE (
    CALCULATE ( COUNTROWS ( Vendas ), Vendas[Status Pagamento] = "Cancelado" ),
    COUNTROWS ( Vendas )
)
```

- O numerador conta **só as canceladas** (`CALCULATE` muda o filtro). O denominador conta **todas** as vendas no contexto (pagas, pendentes, canceladas e "Não Informado").
- **Formato:** Porcentagem, 2 casas. **Esperado:** **7,20%**.

**Gráfico:** **Gráfico de colunas clusterizado** · Eixo X: `Vendas[Canal de Venda]` · Eixo Y: `[Taxa de Cancelamento %]` · classificar decrescente.
Esperado: Marketplace **8,43%** (maior), Aplicativo **6,66%** (menor).

---

## Resumo do que foi usado de DAX

| Conceito | Onde aparece |
|---|---|
| `CALCULATE` (mudar o contexto de filtro) | Faturamento, Vendas Pagas, Margem %, Crescimento YoY %, Taxa de Cancelamento % |
| `DIVIDE` (divisão segura) | Ticket Médio, Margem %, Crescimento YoY %, Taxa de Cancelamento % |
| Iteradora `SUMX` | Margem % |
| Variáveis `VAR … RETURN` | Calendario, Margem %, Crescimento YoY % |
| Inteligência de tempo `SAMEPERIODLASTYEAR` | Crescimento YoY % |
| `REMOVEFILTERS`, `HASONEVALUE`, `EDATE` | Crescimento YoY % |
| Tabela calculada `CALENDAR` + `ADDCOLUMNS` | Calendario |
| Tabela calculada `SUMMARIZECOLUMNS` | Resumo Categoria |
| Tabela só de medidas (`Inserir Dados`) | _Medidas |

### Sugestão de layout

```
+--------------------------------------------------------------------------+
| [Faturamento]          [Vendas Pagas]          [Ticket Médio]            |   Página 1
+------------------------------------+-------------------------------------+   "Visão Geral"
| Faturamento por mês (linha)        | Faturamento por categoria (barras)  |   (= Streamlit)
+------------------------------------+-------------------------------------+
| Faturamento por canal (colunas)    | Top 10 produtos (barras)            |
+------------------------------------+-------------------------------------+

+--------------------------------------------------------------------------+
| Segmentação: Ano [2026]     [Crescimento YoY %]    [Margem %]   [Taxa    |   Página 2
|                                                                 Cancel.] |   "DAX"
+------------------------------------+-------------------------------------+
| Crescimento YoY % por mês          | Margem % por categoria              |
+------------------------------------+-------------------------------------+
| Taxa de Cancelamento % por canal   | Tabela: Resumo Categoria            |
+------------------------------------+-------------------------------------+
```

> **Atenção à segmentação da página 2:** ela filtra o ano 2026 em todos os visuais da página, inclusive Margem % e Taxa de Cancelamento %, cujos valores esperados acima são do **total** (2025 + 2026). Para conferir os valores, limpe a segmentação ou, em **Formatar** > **Editar interações**, desligue o filtro dela nesses visuais.
