import streamlit as st
import pandas as pd
from utils import load_data, aplicar_filtros

# --------------------------------------------------------
# 💡 Página: Insights & Recomendações
# --------------------------------------------------------

st.title('💡 Insights & Recomendações')

# 1) Carregar os dados
df = load_data()

# 2) Traduzir dia da semana para português
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

# 3) Aplicar filtros (período, categoria, hora)
df_f = aplicar_filtros(df)

# 4) Garantir tradução também após os filtros
if 'dia_semana' in df_f.columns:
    df_f['dia_semana'] = df_f['dia_semana'].map(traduz_dia).fillna(df_f['dia_semana'])

# 5) Ordenar os dias na sequência correta
ordem = [
    'Segunda-feira', 'Terça-feira', 'Quarta-feira', 
    'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo'
]
if 'dia_semana' in df_f.columns:
    df_f['dia_semana'] = pd.Categorical(df_f['dia_semana'], categories=ordem, ordered=True)

# --------------------------------------------------------
# 🔍 Análises e recomendações
# --------------------------------------------------------

# Agrupar por dia da semana
vendas_semana = (
    df_f.groupby('dia_semana')['valor_total']
    .sum()
    .sort_values()
)

# Agrupar por hora
por_hora = (
    df_f.groupby('hora')['valor_total']
    .sum()
    .sort_values()
)

# Top prato
prato_top = (
    df_f.groupby('prato')['valor_total']
    .sum()
    .sort_values(ascending=False)
)

# Identificar menores e maiores valores
menor_dia = vendas_semana.index[0] if len(vendas_semana) else '—'
menor_hora = int(por_hora.index[0]) if len(por_hora) else None
melhor_prato = prato_top.index[0] if len(prato_top) else '—'

# --------------------------------------------------------
# 🧠 Recomendações automáticas
# --------------------------------------------------------

st.markdown('### Recomendações Automáticas')

# Formatar hora em formato “10h”, “21h”, etc.
hora_txt = f"{menor_hora}h" if menor_hora is not None else '—'

st.write(
    f"- **Happy hour focado em baixas vendas:** "
    f"Considere promoções às **{hora_txt}** e no dia **{menor_dia}** para aumentar o fluxo."
)

# Analisar margem de lucro (se disponível)
if 'margem' in df_f.columns:
    cat = df_f.groupby('categoria')[['valor_total', 'margem']].sum()
    cat['margem_%'] = (cat['margem'] / cat['valor_total']).fillna(0) * 100
    low_margin = cat.sort_values('margem_%').head(1)

    if len(low_margin):
        st.write(
            f"- **Rever preços/custos:** "
            f"Categoria com menor margem: **{low_margin.index[0]}** "
            f"(≈ {low_margin['margem_%'].iloc[0]:.1f}%)."
        )

# Melhor prato
st.write(
    f"- **Aposte nos campeões de venda:** "
    f"Destaque **{melhor_prato}** em combos com bebida ou sobremesa."
)

st.info(
    "💬 Dica: personalize as regras de recomendação de acordo com o perfil do restaurante — "
    "considerando sazonalidade, eventos locais e metas de faturamento."
)
