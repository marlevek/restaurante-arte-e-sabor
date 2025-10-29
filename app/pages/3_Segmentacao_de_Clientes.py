import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, aplicar_filtros
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


st.title('👥 Segmentação de Clientes')


df = load_data()
df_f = aplicar_filtros(df)


# Aggregações por cliente
clientes_df = (
df_f.groupby('cliente')
.agg({
'valor_total': 'sum',
'quantidade': 'sum',
'data': ['min','max','count']
})
)
clientes_df.columns = ['total_gasto','total_itens','primeira_compra','ultima_compra','num_compras']
clientes_df['primeira_compra'] = pd.to_datetime(clientes_df['primeira_compra'])
clientes_df['ultima_compra'] = pd.to_datetime(clientes_df['ultima_compra'])
clientes_df['dias_entre'] = (clientes_df['ultima_compra'] - clientes_df['primeira_compra']).dt.days
clientes_df['dias_entre'] = clientes_df['dias_entre'].fillna(0)


# Seleção de k
k = st.sidebar.slider('Número de clusters (k)', min_value=2, max_value=6, value=3)


X = clientes_df[['total_gasto','num_compras','dias_entre']].fillna(0)
X_scaled = StandardScaler().fit_transform(X)


km = KMeans(n_clusters=k, random_state=42)
clientes_df['segmento'] = km.fit_predict(X_scaled)


st.subheader('Resumo por Cluster')
resumo = clientes_df.groupby('segmento')[['total_gasto','num_compras','dias_entre','total_itens']].mean().round(2)
st.dataframe(resumo)


st.subheader('Dispersão: Nº Compras x Total Gasto')
fig = px.scatter(clientes_df.reset_index(), x='num_compras', y='total_gasto', color=clientes_df['segmento'].astype(str), hover_name='cliente', title='Clusters de Clientes')
st.plotly_chart(fig, use_container_width=True)


# Download dos segmentos
csv = clientes_df.reset_index().to_csv(index=False).encode('utf-8')
st.download_button('⬇️ Baixar clientes segmentados (CSV)', data=csv, file_name='clientes_segmentados.csv', mime='text/csv')