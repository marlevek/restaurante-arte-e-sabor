# Restaurante Sabor & Arte — Dashboard (Streamlit)


Projeto de portfólio que demonstra o ciclo completo: **simulação/ingestão de dados → EDA → segmentação (K-Means) → dashboard Streamlit**.

# Contexto
O restaurante Sabor & Arte, localizado em uma região de grande movimento comercial, notou que as vendas variam muito entre dias e horários.
O gerente quer entender quais pratos mais lucram, quando há queda de movimento, e quais clientes são mais fiéis, para planejar promoções e cardápios mais estratégicos.


🎯 Objetivos do Projeto

* O projeto visa construir um Dashboard de Inteligência Comercial com:
* Análise de vendas e lucratividade por categoria e horário
* Identificação de padrões de consumo (dia da semana, hora, prato, cliente)
* Segmentação de clientes para programas de fidelidade
* Recomendações baseadas em dados (ex: promoções, ajustes no cardápio)


## Como rodar

```bash
# 1) Clone e vá para a pasta
# git clone <seu-repo>
cd restaurante_sabor_arte


# 2) (opcional) Crie venv
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate


# 3) Instale dependências
pip install -r requirements.txt


# 4) Gere dados de exemplo (opcional)
python generate_data.py


# 5) Rode o app
streamlit run app/app.py

