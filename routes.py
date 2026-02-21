from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required
)
from werkzeug.security import generate_password_hash, check_password_hash
import db
import models
from errors import error

api = Blueprint("api", __name__)

# ================= AUTH =================

@api.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return error("JSON mancante")

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return error("Username e password obbligatori")

    if db.get_user(username):
        return error("Utente già esistente", 409)

    pwd_hash = generate_password_hash(password)
    db.add_user(username, pwd_hash)

    return jsonify({"status": "utente creato"}), 201


@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return error("JSON mancante")

    user = db.get_user(data.get("username"))
    if not user:
        return error("Credenziali non valide", 401)

    if not check_password_hash(user[2], data.get("password")):
        return error("Credenziali non valide", 401)

    token = create_access_token(identity=user[1])
    return jsonify(access_token=token)

# ================= CLIENTI =================

@api.route("/clienti", methods=["GET"])
@jwt_required()
def get_clienti():
    return jsonify(models.get_clienti())


@api.route("/clienti", methods=["POST"])
@jwt_required()
def add_cliente():
    data = request.get_json()
    if not data:
        return error("JSON mancante")

    nome = data.get("nome")
    if not nome:
        return error("Nome obbligatorio")

    models.add_cliente(
        nome,
        data.get("email"),
        data.get("telefono")
    )
    return jsonify({"status": "cliente creato"}), 201


# ================= ORDINI =================

@api.route("/clienti/<int:cid>/ordini", methods=["GET"])
@jwt_required()
def get_ordini(cid):
    return jsonify(models.get_ordini(cid))


@api.route("/clienti/<int:cid>/ordini", methods=["POST"])
@jwt_required()
def add_ordine(cid):
    data = request.get_json()
    if not data:
        return error("JSON mancante")

    descrizione = data.get("descrizione")
    importo = data.get("importo")

    if not descrizione:
        return error("Descrizione obbligatoria")

    try:
        importo = float(importo)
    except:
        return error("Importo non valido")

    models.add_ordine(cid, descrizione, importo)
    return jsonify({"status": "ordine creato"}), 201