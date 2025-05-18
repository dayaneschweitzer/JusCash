import sqlite3
from typing import List, Dict

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
            autores,
            reu,
            advogados,
            valor_bruto,
            valor_juros,
            honorarios,
            conteudo,
            status,
            data_publicacao
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        pub['numero_processo'],
        pub['autores'],
        pub.get('reu', 'Instituto Nacional do Seguro Social - INSS'),
        pub['advogados'],
        pub['valor_bruto'],
        pub['valor_juros'],
        pub['honorarios'],
        pub['conteudo'],
        pub.get('status', 'novas'),
        pub['data_publicacao']
    ))
    conn.commit()
    conn.close()

def listar_publicacoes(query: str = '', fromDate: str = '', toDate: str = '') -> List[Dict]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    sql = "SELECT * FROM publicacoes WHERE 1=1"
    params = []

    if query:
        sql += " AND numero_processo LIKE ?"
        params.append(f"%{query}%")

    if fromDate:
        sql += " AND data_publicacao >= ?"
        params.append(fromDate)

    if toDate:
        sql += " AND data_publicacao <= ?"
        params.append(toDate)

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()

    publicacoes = []
    for row in rows:
        publicacoes.append({
            "id": row[0],
            "numero_processo": row[1],
            "autores": row[2],
            "reu": row[3],
            "advogados": row[4],
            "valor_bruto": row[5],
            "valor_juros": row[6],
            "honorarios": row[7],
            "conteudo": row[8],
            "status": row[9],
            "data_publicacao": row[10]
        })

    return publicacoes

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
def registrar_usuario(nome: str, email: str, senha: str) -> Dict[str, str]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, senha)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("E-mail já está registrado")
    finally:
        conn.close()

    return {
        "nome": nome,
        "email": email
    }
