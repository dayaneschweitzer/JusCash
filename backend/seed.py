import sqlite3
from datetime import datetime, timedelta
import random

conn = sqlite3.connect("./database/publicacoes.db")
cursor = conn.cursor()

# Criar a tabela (se não existir)
cursor.execute("""
CREATE TABLE IF NOT EXISTS publicacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    processNumber TEXT,
    status TEXT,
    publicationDate TEXT,
    lastUpdate TEXT,
    author TEXT,
    defendant TEXT,
    lawyer TEXT,
    valuePrincipal TEXT,
    valueInterest TEXT,
    valueFees TEXT,
    content TEXT
)
""")

# Limpar dados antigos
cursor.execute("DELETE FROM publicacoes")

# Dados de exemplo
nomes_autores = ["João da Silva", "Maria Oliveira", "Carlos Pereira", "Ana Souza"]
nomes_reus = ["INSS", "Banco do Brasil", "Caixa Econômica", "União Federal"]
nomes_adv = ["Dr. José", "Dra. Clara", "Dr. Marcos", "Dra. Beatriz"]
status_options = ["novas", "lidas", "enviados", "concluidas"]

# Função para gerar valores
def format_real(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Inserir 20 publicações
for i in range(20):
    process = f"{random.randint(1000000,9999999)}-21.2021.8.13.{random.randint(1000,9999)}"
    status = random.choice(status_options)
    pub_date = (datetime.now() - timedelta(days=random.randint(1, 120))).strftime('%Y-%m-%d')
    last_update = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
    author = random.choice(nomes_autores)
    defendant = random.choice(nomes_reus)
    lawyer = random.choice(nomes_adv)
    valuePrincipal = format_real(random.uniform(5000, 20000))
    valueInterest = format_real(random.uniform(100, 2000))
    valueFees = format_real(random.uniform(300, 1500))
    content = f"Conteúdo fictício da publicação {i+1}, referente ao processo judicial."

    cursor.execute("""
    INSERT INTO publicacoes (
        processNumber, status, publicationDate, lastUpdate,
        author, defendant, lawyer,
        valuePrincipal, valueInterest, valueFees, content
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        process, status, pub_date, last_update,
        author, defendant, lawyer,
        valuePrincipal, valueInterest, valueFees, content
    ))

conn.commit()
conn.close()
print("✅ Banco populado com 20 publicações completas.")