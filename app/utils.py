from __future__ import annotations
import pandas as pd
import streamlit as st
from pathlib import Path


# ======================================================
# 🔧 Funções auxiliares: carregar dados, filtros e KPIs
# ======================================================

@st.cache_data(show_spinner=False)
def load_data(path: str = 'data/vendas_restaurante.csv') -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=['data'])
     
    # Garantir colunas derivadas
    if 'dia_semana' not in df.columns:
        df['dia_semana'] = df['data'].dt.day_name()
    if 'hora' not in df.columns:
        df['hora'] = df['data'].dt.hour
    if 'margem' not in df.columns and {'valor_total', 'custo_total'}.issubset(df.columns):
        df['margem'] = df['valor_total'] - df['custo_total']
    
    return df


def kpis(df: pd.DataFrame) -> dict:
    total_vendas = float(df['valor_total'].sum()) if 'valor_total' in df else 0.0
    clientes_unicos = int(df['cliente'].nunique()) if 'cliente' in df else 0
    ticket_medio = float(df['valor_total'].mean()) if 'valor_total' in df else 0.0
    margem_total = float(df.get('margem', pd.Series(0)).sum())

    return {
        'total_vendas': total_vendas,
        'clientes_unicos': clientes_unicos,
        'ticket_medio': ticket_medio,
        'margem_total': margem_total,
    }


def aplicar_filtros(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.markdown('### 🔎 Filtros')

    # ===============================
    # 📅 Período — formato BR
    # ===============================
    st.sidebar.markdown("#### 📆 Selecione o Período")

    min_d, max_d = df['data'].min().date(), df['data'].max().date()

    # Força formato DD/MM/YYYY (visual)
    periodo = st.sidebar.date_input(
        "Período",
        value=(min_d, max_d),
        min_value=min_d,
        max_value=max_d,
        format="DD/MM/YYYY"
    )

    # Aplicar filtro
    if isinstance(periodo, tuple) and len(periodo) == 2:
        ini, fim = periodo
        df = df[(df['data'].dt.date >= ini) & (df['data'].dt.date <= fim)]

    # ===============================
    # 🥗 Categoria
    # ===============================
    if 'categoria' in df.columns:
        categorias = sorted(df['categoria'].dropna().unique().tolist())
        cat_sel = st.sidebar.multiselect('Categorias', categorias, default=categorias)
        df = df[df['categoria'].isin(cat_sel)] if cat_sel else df

    # ===============================
    # ⏰ Hora do Dia
    # ===============================
    if 'hora' in df.columns:
        hora_min, hora_max = int(df['hora'].min()), int(df['hora'].max())
        h_sel = st.sidebar.slider(
            "Hora do Dia",
            min_value=hora_min,
            max_value=hora_max,
            value=(hora_min, hora_max)
        )
        df = df[(df['hora'] >= h_sel[0]) & (df['hora'] <= h_sel[1])]

    return df

