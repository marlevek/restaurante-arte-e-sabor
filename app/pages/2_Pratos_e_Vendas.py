import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, aplicar_filtros


st.title('🍝 Pratos e Vendas')


df = load_data()
df_f = aplicar_filtros(df)


# Top pratos por receita
top_pratos = (
df_f.groupby('prato')['valor_total']
.sum().reset_index()
.sort_values('valor_total', ascending=False)
)
st.subheader('Top 10 Pratos por Receita')
st.plotly_chart(px.bar(top_pratos.head(10), x='prato', y='valor_total', title='Receita por Prato'), use_container_width=True)


# Margem por categoria (se disponível)
if 'margem' in df_f.columns:
    cat = df_f.groupby('categoria')[['valor_total','margem']].sum().reset_index()
    cat['margem_%'] = (cat['margem'] / cat['valor_total']).replace([float('inf'), -float('inf')], 0).fillna(0) * 100
    st.subheader('Margem por Categoria')
    st.plotly_chart(px.bar(cat, x='categoria', y='margem_%', title='Margem % por Categoria'), use_container_width=True)


# Receita por hora (padrões de consumo)
por_hora = df_f.groupby('hora')['valor_total'].sum().reset_index()
st.subheader('Vendas por Hora do Dia')
st.plotly_chart(px.line(por_hora, x='hora', y='valor_total', markers=True, title='Receita por Hora'), use_container_width=True)