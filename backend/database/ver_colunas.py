import sqlite3

conn = sqlite3.connect("publicacoes.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(publicacoes)")
for col in cursor.fetchall():
    print(col)

conn.close()

