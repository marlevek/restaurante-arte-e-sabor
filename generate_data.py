import pandas as pd
import numpy as np
import random
from faker import Faker
from pathlib import Path


fake = Faker('pt_BR')
np.random.seed(42)


pratos = [
{'nome': 'Feijoada', 'categoria': 'Prato Principal', 'preco': 35.0, 'custo': 18.0},
{'nome': 'Strogonoff', 'categoria': 'Prato Principal', 'preco': 32.0, 'custo': 16.0},
{'nome': 'Salada Caesar', 'categoria': 'Entrada', 'preco': 18.0, 'custo': 8.0},
{'nome': 'Suco Natural', 'categoria': 'Bebida', 'preco': 10.0, 'custo': 3.0},
{'nome': 'Refrigerante', 'categoria': 'Bebida', 'preco': 8.0, 'custo': 2.5},
{'nome': 'Petit Gateau', 'categoria': 'Sobremesa', 'preco': 15.0, 'custo': 6.0},
]


clientes = [fake.name() for _ in range(250)]


rows = []
for _ in range(3500):
    p = random.choice(pratos)
    q = np.random.randint(1, 4)
    dt = fake.date_time_between(start_date='-120d', end_date='now')
    rows.append({
    'data': dt,
    'cliente': random.choice(clientes),
    'prato': p['nome'],
    'categoria': p['categoria'],
    'quantidade': q,
    'valor_unitario': p['preco'],
    'custo_unitario': p['custo'],
    'valor_total': round(p['preco'] * q, 2),
    'custo_total': round(p['custo'] * q, 2)
    })


df = pd.DataFrame(rows)
df['margem'] = df['valor_total'] - df['custo_total']
df['dia_semana'] = df['data'].dt.day_name()
df['hora'] = df['data'].dt.hour


Path('data').mkdir(exist_ok=True)
df.to_csv('data/vendas_restaurante.csv', index=False)
print('Arquivo gerado em data/vendas_restaurante.csv com', len(df), 'linhas')