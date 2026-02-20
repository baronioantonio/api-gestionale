import db


# ---------- CLIENTI ----------

def get_clienti():
    conn = db.connect()
    c = conn.cursor()
    c.execute("SELECT * FROM clienti")
    rows = c.fetchall()
    conn.close()
    return rows


def add_cliente(nome, email, telefono):
    conn = db.connect()
    c = conn.cursor()
    c.execute(
        "INSERT INTO clienti (nome, email, telefono) VALUES (?, ?, ?)",
        (nome, email, telefono)
    )
    conn.commit()
    conn.close()


def update_cliente(cid, nome, email, telefono):
    conn = db.connect()
    c = conn.cursor()
    c.execute(
        "UPDATE clienti SET nome=?, email=?, telefono=? WHERE id=?",
        (nome, email, telefono, cid)
    )
    conn.commit()
    conn.close()


def delete_cliente(cid):
    conn = db.connect()
    c = conn.cursor()
    c.execute("DELETE FROM clienti WHERE id=?", (cid,))
    conn.commit()
    conn.close()


# ---------- ORDINI ----------

def get_ordini(cliente_id):
    conn = db.connect()
    c = conn.cursor()
    c.execute(
        "SELECT id, descrizione, importo FROM ordini WHERE cliente_id=?",
        (cliente_id,)
    )
    rows = c.fetchall()
    conn.close()
    return rows


def add_ordine(cliente_id, descrizione, importo):
    conn = db.connect()
    c = conn.cursor()
    c.execute(
        "INSERT INTO ordini (cliente_id, descrizione, importo) VALUES (?, ?, ?)",
        (cliente_id, descrizione, importo)
    )
    conn.commit()
    conn.close()