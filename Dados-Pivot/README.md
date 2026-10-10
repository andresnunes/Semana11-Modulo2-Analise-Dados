# Atividade Power BI – Transformar Colunas em Linhas (Unpivot)

## Objetivo
Praticar a **Transformação de Colunas em Linhas** (*Unpivot*) no Power Query.

## Arquivo
- **vendas_mensais.csv**: quantidade vendida de 8 produtos em cada mês do ano (Jan a Dez), separada por ponto e vírgula (`;`).

| Produto | Jan | Fev | Mar | ... | Dez |
|---|---|---|---|---|---|
| Notebook | 12 | 15 | 9 | ... | 35 |
| Mouse | 40 | 35 | 50 | ... | 70 |
| Teclado | 25 | 30 | 22 | ... | 45 |
| ... | ... | ... | ... | ... | ... |

## O problema
Cada mês está em uma **coluna separada**. Assim fica difícil criar um gráfico por mês ou somar as vendas, porque o Power BI trabalha melhor quando cada informação está em **uma única coluna**.

## Tarefas

### 1. Importar os dados
Importe o arquivo **vendas_mensais.csv** e abra o Power Query (**Transformar dados**).

### 2. Fazer o Unpivot
- Selecione a coluna **Produto**.
- Clique com o botão direito → **Transformar outras colunas em linhas** (*Unpivot Other Columns*).

### 3. Renomear as colunas
- `Atributo` → **Mes**
- `Valor` → **Quantidade** (tipo **Número inteiro**)

### 4. Resultado esperado (96 linhas = 8 produtos × 12 meses)

| Produto | Mes | Quantidade |
|---|---|---|
| Notebook | Jan | 12 |
| Notebook | Fev | 15 |
| Notebook | Mar | 9 |
| Notebook | Abr | 18 |
| Mouse | Jan | 40 |
| ... | ... | ... |

### 5. Criar um visual
Crie um **gráfico de colunas** com **Mes** no eixo X e **Quantidade** nos valores. Use **Produto** na legenda.

## Desafio (opcional)
Faça o caminho inverso: selecione a coluna **Mes** → **Transformar → Coluna Dinâmica** (*Pivot Column*), usando **Quantidade** como valores. A tabela deve voltar ao formato original.
