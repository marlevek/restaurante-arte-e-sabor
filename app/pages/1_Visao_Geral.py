import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, aplicar_filtros, kpis


st.title('📊 Visão Geral')


df = load_data()
df_f = aplicar_filtros(df)


# Distribuição por dia da semana
semana = (
df_f.groupby('dia_semana')['valor_total']
.sum().reset_index()
.sort_values('valor_total', ascending=False)
)
fig = px.bar(semana, x='dia_semana', y='valor_total', title='Vendas por Dia da Semana (R$)')
st.plotly_chart(fig, use_container_width=True)


# Heatmap dia x hora
pvt = df_f.pivot_table(index='dia_semana', columns='hora', values='valor_total', aggfunc='sum', fill_value=0)
fig2 = px.imshow(pvt, aspect='auto', origin='lower', title='Mapa de Calor — Dia da Semana x Hora (R$)')
st.plotly_chart(fig2, use_container_width=True)


st.dataframe(df_f.sample(min(10, len(df_f))))