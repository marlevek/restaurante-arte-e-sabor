import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, aplicar_filtros, kpis

# --------------------------------------------------------
# 🏠 Configuração da página principal
# --------------------------------------------------------
st.set_page_config(page_title='Restaurante Sabor & Arte', layout='wide')
st.title('🍽️ Restaurante Sabor & Arte — Inteligência Comercial')

# --------------------------------------------------------
# ❌ Removido o uso de locale (não suportado no Streamlit Cloud)
# Em vez disso, formatamos datas manualmente para PT-BR
# --------------------------------------------------------

# --------------------------------------------------------
# 🔍 Carregar dados e aplicar filtros
# --------------------------------------------------------
df = load_data()
df_f = aplicar_filtros(df)

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
# 📅 Vendas por Dia (com datas formatadas no padrão BR)
# --------------------------------------------------------
vendas_dia = (
    df_f.groupby(df_f['data'].dt.date)['valor_total']
    .sum()
    .reset_index(name='valor_total')
)

# Formatando as datas manualmente (sem locale)
vendas_dia['data_formatada'] = pd.to_datetime(vendas_dia['data']).dt.strftime('%d/%m/%Y')

# Gráfico de linha
fig = px.line(
    vendas_dia,
    x='data_formatada',
    y='valor_total',
    title='📆 Vendas Diárias (R$)'
)
fig.update_xaxes(title='Data (DD/MM/AAAA)')
fig.update_yaxes(title='Total de Vendas (R$)')
st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------------
# 💬 Rodapé
# --------------------------------------------------------
st.caption('💬 Use o menu lateral para filtrar período, categoria e hora do dia.')
