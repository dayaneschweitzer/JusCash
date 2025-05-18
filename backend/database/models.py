import sqlite3
from typing import List, Dict, Any

DB_NAME = 'publicacoes.db'

# database/models.py
import sqlite3

DB_NAME = 'database/publicacoes.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS publicacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_processo TEXT,
            autores TEXT,
            reu TEXT DEFAULT 'Instituto Nacional do Seguro Social - INSS',
            advogados TEXT,
            valor_bruto TEXT,
            valor_juros TEXT,
            honorarios TEXT,
            conteudo TEXT,
            status TEXT DEFAULT 'novas',
            data_publicacao TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_publicacao(pub: Dict[str, str]) -> None:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO publicacoes (
            numero_processo,
            data_disponibilizacao,
            autores,
            advogados,
            conteudo,
            valor_bruto,
            valor_juros,
            honorarios
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        pub['numero_processo'],
        pub['data_disponibilizacao'],
        pub['autores'],
        pub['advogados'],
        pub['conteudo'],
        pub['valor_bruto'],
        pub['valor_juros'],
        pub['honorarios']
    ))
    conn.commit()
    conn.close()

import sqlite3

def listar_publicacoes(query="", fromDate="", toDate=""):
    conn = sqlite3.connect("database/publicacoes.db")
    cursor = conn.cursor()

    sql = "SELECT * FROM publicacoes WHERE 1=1"
    params = []

    if query:
        sql += " AND numero LIKE ?"
        params.append(f"%{query}%")

    if fromDate:
        sql += " AND data >= ?"
        params.append(fromDate)

    if toDate:
        sql += " AND data <= ?"
        params.append(toDate)

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row[0],
            "numero": row[1],
            "status": row[2],
            "data": row[3],
            "descricao": row[4],
        }
        for row in rows
    ]

def atualizar_status_publicacao(pub_id: int, novo_status: str) -> bool:
   
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE publicacoes SET status = ? WHERE id = ?
    ''', (novo_status, pub_id))
    conn.commit()
    atualizado = cursor.rowcount > 0
    conn.close()
    return atualizado
