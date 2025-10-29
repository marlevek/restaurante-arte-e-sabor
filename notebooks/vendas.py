import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker('pt_BR')
np.random.seed(42)

# Simulando dados
pratos = [
    {'nome': 'Feijoada', 'categoria': 'Prato Principal', 'preco': 35.0},
    {'nome': 'Strogonoff', 'categoria': 'Prato Principal', 'preco': 32.0},
    {'nome': 'Salada Caesar', 'categoria': 'Entrada', 'preco': 18.0},
    {'nome': 'Suco Natural', 'categoria': 'Bebida', 'preco': 10.0},
    {'nome': 'Refrigerante', 'categoria': 'Bebida', 'preco': 8.0},
    {'nome': 'Petit Gateau', 'categoria': 'Sobremesa', 'preco': 15.0},
]

clientes = [fake.name() for _ in range(200)]

dados = []
for _ in range(3000):
    p = random.choice(pratos)
    quantidade = np.random.randint(1, 4)
    dados.append({
        'data': fake.date_time_between(start_date='-90d', end_date='now'),
        'cliente': random.choice(clientes),
        'prato': p['nome'],
        'categoria': p['categoria'],
        'quantidade': quantidade,
        'valor_unitario': p['preco'],
        'valor_total': round(p['preco'] * quantidade, 2)
    })

df = pd.DataFrame(dados)
df['dia_semana'] = df['data'].dt.day_name()
df['hora'] = df['data'].dt.hour
df.to_csv('../data/vendas_restaurante.csv', index=False)
