
# streamlit run Ciclo07_ProjetoDoAluno/Dashboard.py 

import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# Configurações gerais
sns.set_theme()
plt.rcParams['figure.figsize'] = (6, 3)  # Tamanho da figura
plt.rcParams['axes.titlesize'] = 10  # Tamanho do título
plt.rcParams['axes.labelsize'] = 8  # Tamanho dos rótulos dos eixos
plt.rcParams['xtick.labelsize'] = 7  # Tamanho dos ticks eixo x
plt.rcParams['ytick.labelsize'] = 7  # Tamanho dos ticks eixo y
plt.rcParams['legend.fontsize'] = 8  # Tamanho da legenda
plt.rcParams['lines.markersize'] = 4  # Tamanho dos marcadores nas linhas

# Carregar dados
caminho = 'c:\\Users\\danmc\\OneDrive\\Carreira_DataScience\\Comunidade DS\\_Repos\\00_PosGraduacao\\01_Python\\datasets\\'
order_items_df = pd.read_csv(caminho + 'order_items_Consolidado.csv')

# Configuração da página
st.set_page_config(page_title='Análise de Vendas por Estado', layout='wide')
st.title('Dashboard de Análise de Vendas por Estado')

# Painel lateral para filtros
st.sidebar.title('Filtros')
filtro_estado = st.sidebar.multiselect('Selecione o(s) Estado(s)', options=order_items_df['customer_state'].unique())

# Filtro de data por mês e ano (multisseleção)
order_items_df['order_purchase_timestamp'] = pd.to_datetime(order_items_df['order_purchase_timestamp'])
order_items_df['order_purchase_year_month'] = order_items_df['order_purchase_timestamp'].dt.to_period('M').astype(str)
filtro_data = st.sidebar.multiselect(
    'Selecione o(s) Mês/Ano', 
    options=sorted(order_items_df['order_purchase_year_month'].unique().tolist()),
    default=sorted(order_items_df['order_purchase_year_month'].unique().tolist())  # Seleciona todos por padrão
)

# Aplicando filtros
if filtro_estado:
    order_items_df = order_items_df[order_items_df['customer_state'].isin(filtro_estado)]
if filtro_data:
    order_items_df = order_items_df[order_items_df['order_purchase_year_month'].isin(filtro_data)]

# Métricas gerais
total_vendas = order_items_df['price'].sum()
total_customers = order_items_df['customer_id'].nunique()
total_sellers = order_items_df['seller_id'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric('Vendas Totais', f"R${total_vendas:,.2f}")
col2.metric('Clientes Únicos', f"{total_customers:,.0f}")
col3.metric('Vendedores Únicos', f"{total_sellers:,.0f}")

# Abas para Visão Geral e Insights
tab1, tab2 = st.tabs(["Visão Geral", "Insights"])

with tab1:
    st.subheader('Visão Geral das Vendas por Estado')
    col1, col2, col3 = st.columns(3)

    # Gráfico de vendas por estado
    vendas_estados = order_items_df.groupby('customer_state')['price'].sum().reset_index()
    fig1, ax1 = plt.subplots()
    sns.barplot(data=vendas_estados, x='customer_state', y='price', ax=ax1)
    ax1.set_title('Vendas Totais por Estado')
    plt.xlabel('Estado')
    plt.ylabel('Vendas (R$)')
    col1.pyplot(fig1)

    # Gráfico de clientes únicos por estado
    clientes_estado = order_items_df.groupby('customer_state')['customer_unique_id'].nunique().reset_index()
    fig2, ax2 = plt.subplots()
    sns.barplot(data=clientes_estado, x='customer_state', y='customer_unique_id', ax=ax2)
    ax2.set_title('Clientes Únicos por Estado')
    plt.xlabel('Estado')
    plt.ylabel('Clientes Únicos')
    col2.pyplot(fig2)

    # Gráfico de vendedores únicos por estado
    vendedores_estado = order_items_df.groupby('seller_state')['seller_id'].nunique().reset_index()
    fig3, ax3 = plt.subplots()
    sns.barplot(data=vendedores_estado, x='seller_state', y='seller_id', ax=ax3)
    ax3.set_title('Vendedores Únicos por Estado')
    plt.xlabel('Estado')
    plt.ylabel('Vendedores Únicos')
    col3.pyplot(fig3)

    # Visão Temporal por Estado
    st.subheader('Visão Temporal por Estado')
    order_items_df['order_purchase_year_month'] = order_items_df['order_purchase_timestamp'].dt.to_period('M').astype(str)

    col1, col2, col3 = st.columns(3)
    vendas_temporal = order_items_df.groupby('order_purchase_year_month')['price'].sum().reset_index()
    fig1, ax1 = plt.subplots()
    sns.lineplot(data=vendas_temporal, x='order_purchase_year_month', y='price', ax=ax1)
    ax1.set_title(f'Vendas (R$) por mês')
    plt.xlabel('Ano-Mês')
    plt.ylabel('Vendas (R$)')
    plt.xticks(rotation=60)
    col1.pyplot(fig1)

    clientes_temporal = order_items_df.groupby('order_purchase_year_month')['customer_unique_id'].nunique().reset_index()
    fig2, ax2 = plt.subplots()
    sns.lineplot(data=clientes_temporal, x='order_purchase_year_month', y='customer_unique_id', ax=ax2)
    ax2.set_title(f'Clientes Únicos por mês')
    plt.xlabel('Ano-Mês')
    plt.ylabel('Clientes Únicos')
    plt.xticks(rotation=60)
    col2.pyplot(fig2)

    vendedores_temporal = order_items_df.groupby('order_purchase_year_month')['seller_id'].nunique().reset_index()
    fig3, ax3 = plt.subplots()
    sns.lineplot(data=vendedores_temporal, x='order_purchase_year_month', y='seller_id', ax=ax3)
    ax3.set_title(f'Vendedores Únicos por mês')
    plt.xlabel('Ano-Mês')
    plt.ylabel('Vendedores Únicos')
    plt.xticks(rotation=60)
    col3.pyplot(fig3)

with tab2:
    st.subheader('Insights')

    # Gráfico de Pareto para clientes únicos por estado
    clientes_por_estado = order_items_df.groupby('customer_state')['customer_unique_id'].nunique().reset_index()
    clientes_por_estado = clientes_por_estado.sort_values('customer_unique_id', ascending=False)
    clientes_por_estado['cumulative_percent'] = clientes_por_estado['customer_unique_id'].cumsum() / clientes_por_estado['customer_unique_id'].sum() * 100

    fig, ax = plt.subplots()
    ax.bar(clientes_por_estado['customer_state'], clientes_por_estado['customer_unique_id'], color='b', label='Clientes Únicos')
    ax2 = ax.twinx()
    ax2.plot(clientes_por_estado['customer_state'], clientes_por_estado['cumulative_percent'], color='r', marker='o', label='Percentual Acumulado')
    ax2.yaxis.set_major_formatter(PercentFormatter())
    ax.set_title('Pareto - Melhores Estados por Número de Clientes')
    ax.set_xlabel('Estado')
    ax.set_ylabel('Clientes Únicos')
    ax2.set_ylabel('Percentual Acumulado')
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    st.pyplot(fig)

    # Cálculo dos valores correspondentes ao threshold de 80% de Clientes únicos
    threshold = 85
    estados_acima_threshold = clientes_por_estado[clientes_por_estado['cumulative_percent'] <= threshold]

    # Filtrar os dados para os estados acima do threshold
    estados_selecionados = estados_acima_threshold['customer_state'].tolist()
    dados_threshold = order_items_df[order_items_df['customer_state'].isin(estados_selecionados)]

    # Calcular métricas para os estados acima do threshold
    vendas_threshold = dados_threshold['price'].sum()
    vendedores_threshold = dados_threshold['seller_id'].nunique()
    clientes_threshold = dados_threshold['customer_unique_id'].nunique()

    # Texto da recomendação
    st.write(f"**Recomendação:** Os **{len(estados_selecionados)}** principais estados concentram quantidade de Clientes únicos prioritários estabelecidos pelo Método de Pareto que equivalem a:")
    st.write(f"- **{clientes_threshold}** clientes únicos ({(clientes_threshold / total_customers) * 100:.1f}% do total de Clientes).")
    st.write(f"- **{vendedores_threshold}** vendedores únicos ({(vendedores_threshold / total_sellers) * 100:.1f}% do total de Vendedores).")
    st.write(f"- **R${vendas_threshold:,.2f}** em vendas ({(vendas_threshold / total_vendas) * 100:.1f}% do total de Vendas).")
    st.write("Recomendamos focar esforços de marketing e vendas em pelo menos nesses estados para maximizar o retorno. "
             "Considere expandir estratégias para os demais estados apenas após consolidar a presença nesses mercados prioritários.")