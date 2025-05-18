import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = 'database/publicacoes.db'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

status_options = ['novas', 'lidas', 'enviados', 'concluidas']

for _ in range(20):
    numero_processo = f"{random.randint(1000000, 9999999)}-21.2021.8.13.{random.randint(1000, 9999)}"
    autores = random.choice(['Maria Silva', 'João Souza', 'Ana Paula', 'Carlos Andrade'])
    advogados = random.choice(['Dr. Marcos - OAB 12345', 'Dra. Luana - OAB 54321'])
    valor_bruto = f"R$ {random.randint(5000, 20000)}"
    valor_juros = f"R$ {random.randint(500, 3000)}"
    honorarios = f"R$ {random.randint(1000, 5000)}"
    conteudo = "Exemplo de conteúdo da publicação jurídica."
    status = random.choice(status_options)
    data_publicacao = (datetime.now() - timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d')

    cursor.execute("""
        INSERT INTO publicacoes (
            numero_processo,
            autores,
            advogados,
            valor_bruto,
            valor_juros,
            honorarios,
            conteudo,
            status,
            data_publicacao
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        numero_processo,
        autores,
        advogados,
        valor_bruto,
        valor_juros,
        honorarios,
        conteudo,
        status,
        data_publicacao
    ))

conn.commit()
conn.close()
print("✅ Banco populado com 20 publicações de teste.")
