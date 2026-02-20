import sqlite3

DB_NAME = "clienti.db"


def connect():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = connect()
    c = conn.cursor()

    # ---------- UTENTI (AUTH) ----------
    c.execute("""
        CREATE TABLE IF NOT EXISTS utenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # ---------- CLIENTI ----------
    c.execute("""
        CREATE TABLE IF NOT EXISTS clienti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT,
            telefono TEXT
        )
    """)

    # ---------- ORDINI ----------
    c.execute("""
        CREATE TABLE IF NOT EXISTS ordini (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            descrizione TEXT NOT NULL,
            importo REAL NOT NULL,
            FOREIGN KEY(cliente_id) REFERENCES clienti(id)
        )
    """)

    conn.commit()
    conn.close()


# ================== UTENTI ==================

def add_user(username, password_hash):
    conn = connect()
    c = conn.cursor()
    c.execute(
        "INSERT INTO utenti (username, password) VALUES (?, ?)",
        (username, password_hash)
    )
    conn.commit()
    conn.close()


def get_user(username):
    conn = connect()
    c = conn.cursor()
    c.execute(
        "SELECT id, username, password FROM utenti WHERE username=?",
        (username,)
    )
    row = c.fetchone()
    conn.close()
    return row


# ================== CLIENTI ==================

def get_clienti():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM clienti")
    rows = c.fetchall()
    conn.close()
    return rows


def add_cliente(nome, email, telefono):
    conn = connect()
    c = conn.cursor()
    c.execute(
        "INSERT INTO clienti (nome, email, telefono) VALUES (?, ?, ?)",
        (nome, email, telefono)
    )
    conn.commit()
    conn.close()


def update_cliente(cid, nome, email, telefono):
    conn = connect()
    c = conn.cursor()
    c.execute(
        "UPDATE clienti SET nome=?, email=?, telefono=? WHERE id=?",
        (nome, email, telefono, cid)
    )
    conn.commit()
    conn.close()


def delete_cliente(cid):
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM clienti WHERE id=?", (cid,))
    conn.commit()
    conn.close()


# ================== ORDINI ==================

def get_ordini(cliente_id):
    conn = connect()
    c = conn.cursor()
    c.execute(
        "SELECT id, descrizione, importo FROM ordini WHERE cliente_id=?",
        (cliente_id,)
    )
    rows = c.fetchall()
    conn.close()
    return rows


def add_ordine(cliente_id, descrizione, importo):
    conn = connect()
    c = conn.cursor()
    c.execute(
        "INSERT INTO ordini (cliente_id, descrizione, importo) VALUES (?, ?, ?)",
        (cliente_id, descrizione, importo)
    )
    conn.commit()
    conn.close()