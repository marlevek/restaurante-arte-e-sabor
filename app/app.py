import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, aplicar_filtros, kpis
import locale
import platform 

# --------------------------------------------------------
# 🌎 Configurar idioma e formatação PT-BR - CORRIGIDO
# --------------------------------------------------------
def configurar_locale_ptbr():
    """Configura locale para português brasileiro de forma robusta"""
    try:
        # Verifica o sistema operacional
        sistema = platform.system()
        
        if sistema == 'Windows':
            locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
        elif sistema == 'Darwin':  # macOS
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        else:  # Linux e outros
            locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
        
        return True
    except Exception as e:
        st.warning(f"⚠️ Locale PT-BR não disponível. Datas em inglês. Erro: {e}")
        return False

# Aplicar configuração
configurar_locale_ptbr()

# --------------------------------------------------------
# 🏠 Configuração da página principal
# --------------------------------------------------------
st.set_page_config(page_title='Restaurante Sabor & Arte', layout='wide')
st.title('🍽️ Restaurante Sabor & Arte — Inteligência Comercial')

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
# 📅 Vendas por Dia
# --------------------------------------------------------
vendas_dia = df_f.groupby(df_f['data'].dt.date)['valor_total'].sum().reset_index(name='valor_total')
fig = px.line(vendas_dia, x='data', y='valor_total', title='📆 Vendas Diárias (R$)')
fig.update_xaxes(title='Data', tickformat='%d/%m')
st.plotly_chart(fig, use_container_width=True)

st.caption('💬 Use o menu lateral para filtrar período, categoria e hora do dia.')
