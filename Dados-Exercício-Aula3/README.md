# Atividade Power BI – Vendas por Região

## Objetivo
Praticar o tratamento de dados no Power Query, a criação de uma coluna calculada e de medidas em DAX, incluindo o uso do `CALCULATE` com filtro.

## Arquivo
- **vendas.csv**: 10 pedidos de venda, com colunas separadas por ponto e vírgula (`;`).

| Coluna | Descrição |
|---|---|
| Pedido | Número do pedido |
| Data | Data da venda |
| Produto | Nome do produto ⚠️ *precisa de ajuste* |
| Regiao | Região da venda |
| Quantidade | Quantidade vendida |
| Preco_Unitario | Preço de cada unidade ⚠️ *precisa de ajuste* |

## Tarefas

### 1. Importar os dados
Importe o arquivo **vendas.csv** no Power BI e abra o Power Query (**Transformar dados**).

### 2. Ajustar a coluna Produto (texto)
- Remova os espaços extras.
- Padronize os nomes. Exemplo: `Notebook`, `Mouse`.

### 3. Ajustar a coluna Preco_Unitario (número)
- Remova o `R$`.
- Converta a coluna para **número decimal**.

> 💡 Dica: os valores usam vírgula como separador decimal (padrão brasileiro). Fique atento à localidade na hora de converter.

### 4. Criar a coluna calculada
Crie a coluna **Total**, que é a **Quantidade × Preco_Unitario**.

### 5. Criar as medidas
- **Faturamento Total**: soma do Total, sem filtro.
- **Faturamento Sul**: soma do Total usando `CALCULATE` com filtro na Região **"Sul"**.

### 6. Criar os visuais
Monte um visual para cada medida, por exemplo um cartão ou um gráfico por Produto.

## Checklist de entrega
- [ ] Coluna **Produto** com apenas 4 produtos distintos
- [ ] Coluna **Preco_Unitario** com tipo numérico
- [ ] Coluna calculada **Total** criada
- [ ] Medida **Faturamento Total** criada
- [ ] Medida **Faturamento Sul** criada com `CALCULATE`
- [ ] Um visual para cada medida

## Para pensar
Coloque as duas medidas em um gráfico por **Região**. Por que **Faturamento Sul** mostra o mesmo valor em todas as barras?
