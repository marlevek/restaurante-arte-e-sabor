import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, aplicar_filtros, kpis

# --------------------------------------------------------
# 📊 Página: Visão Geral
# --------------------------------------------------------

st.title('📊 Visão Geral')

# 1️⃣ Carregar dados
df = load_data()

# 2️⃣ Traduzir dias da semana para português
traduz_dia = {
    'Monday': 'Segunda-feira',
    'Tuesday': 'Terça-feira',
    'Wednesday': 'Quarta-feira',
    'Thursday': 'Quinta-feira',
    'Friday': 'Sexta-feira',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}
if 'dia_semana' in df.columns:
    df['dia_semana'] = df['dia_semana'].map(traduz_dia).fillna(df['dia_semana'])

# 3️⃣ Aplicar filtros (menu lateral)
df_f = aplicar_filtros(df)

# 4️⃣ Garantir tradução também após filtros
if 'dia_semana' in df_f.columns:
    df_f['dia_semana'] = df_f['dia_semana'].map(traduz_dia).fillna(df_f['dia_semana'])

# 5️⃣ Ordenar dias da semana
ordem = [
    'Segunda-feira', 'Terça-feira', 'Quarta-feira',
    'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo'
]
if 'dia_semana' in df_f.columns:
    df_f['dia_semana'] = pd.Categorical(df_f['dia_semana'], categories=ordem, ordered=True)

# --------------------------------------------------------
# 📈 KPIs principais
# --------------------------------------------------------

m = kpis(df_f)
col1, col2, col3, col4 = st.columns(4)
col1.metric('Total de Vendas (R$)', f"{m['total_vendas']:.2f}")
col2.metric('Clientes Únicos', m['clientes_unicos'])
col3.metric('Ticket Médio (R$)', f"{m['ticket_medio']:.2f}")
col4.metric('Margem Total (R$)', f"{m['margem_total']:.2f}")

# --------------------------------------------------------
# 📅 Vendas por Dia da Semana
# --------------------------------------------------------

semana = (
    df_f.groupby('dia_semana')['valor_total']
    .sum()
    .reset_index()
    .sort_values('dia_semana', key=lambda x: pd.Categorical(x, categories=ordem, ordered=True))
)

fig_semana = px.bar(
    semana,
    x='dia_semana',
    y='valor_total',
    title='Vendas por Dia da Semana (R$)',
    text_auto='.2s'
)
fig_semana.update_layout(xaxis_title='', yaxis_title='Total de Vendas (R$)')
st.plotly_chart(fig_semana, use_container_width=True)

# --------------------------------------------------------
# ⏰ Heatmap: Dia da Semana x Hora
# --------------------------------------------------------

# Criar tabela dinâmica
pvt = df_f.pivot_table(
    index='dia_semana',
    columns='hora',
    values='valor_total',
    aggfunc='sum',
    fill_value=0
)

# Reordenar linhas (dias)
pvt = pvt.reindex(ordem)

fig_heatmap = px.imshow(
    pvt,
    aspect='auto',
    origin='upper',
    color_continuous_scale='Blues',
    title='Mapa de Calor — Dia da Semana x Hora (R$)'
)
fig_heatmap.update_xaxes(title='Hora do Dia')
fig_heatmap.update_yaxes(title='Dia da Semana')

st.plotly_chart(fig_heatmap, use_container_width=True)

# --------------------------------------------------------
# 🔎 Amostra de dados (para inspeção rápida)
# --------------------------------------------------------

st.markdown("### 📄 Amostra de Dados Filtrados")
st.dataframe(df_f.sample(min(10, len(df_f))))

st.caption("💬 Dica: use o menu lateral para ajustar período, categoria e hora. Os gráficos são atualizados automaticamente.")
