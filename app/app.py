import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, aplicar_filtros, kpis


st.set_page_config(page_title='Restaurante Sabor & Arte', layout='wide')
st.title('🍽️ Restaurante Sabor & Arte — Inteligência Comercial')


# Carregar e filtrar
df = load_data()
df_f = aplicar_filtros(df)

# KPIs
m = kpis(df_f)
col1, col2, col3, col4 = st.columns(4)
col1.metric('Total de Vendas (R$)', f"{m['total_vendas']:.2f}")
col2.metric('Clientes Únicos', m['clientes_unicos'])
col3.metric('Ticket Médio (R$)', f"{m['ticket_medio']:.2f}")
col4.metric('Margem Total (R$)', f"{m['margem_total']:.2f}")

# Vendas por dia
vendas_dia = df_f.groupby(df_f['data'].dt.date)['valor_total'].sum().reset_index(name='valor_total')
fig = px.line(vendas_dia, x='data', y='valor_total', title='Vendas Diárias (R$)')
st.plotly_chart(fig, use_container_width=True)


st.caption('Dica: use o menu lateral para filtrar período, categoria e hora do dia.')