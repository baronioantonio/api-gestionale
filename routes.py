from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required
)
from werkzeug.security import generate_password_hash, check_password_hash

import db
import models

# Blueprint SENZA prefisso
api = Blueprint("api", __name__)

# =========================
# AUTH
# =========================

@api.route("/register", methods=["POST"], strict_slashes=False)
def register():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON mancante"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username e password obbligatori"}), 400

    if db.get_user(username):
        return jsonify({"error": "Utente già esistente"}), 409

    password_hash = generate_password_hash(password)
    db.add_user(username, password_hash)

    return jsonify({"status": "utente creato"}), 201


@api.route("/login", methods=["POST"], strict_slashes=False)
def login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON mancante"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Credenziali non valide"}), 401

    user = db.get_user(username)
    if not user:
        return jsonify({"error": "Credenziali non valide"}), 401

    if not check_password_hash(user[2], password):
        return jsonify({"error": "Credenziali non valide"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


# =========================
# CLIENTI
# =========================

@api.route("/clienti", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_clienti():
    return jsonify(models.get_clienti())


@api.route("/clienti", methods=["POST"], strict_slashes=False)
@jwt_required()
def add_cliente():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON mancante"}), 400

    nome = data.get("nome")
    email = data.get("email")
    telefono = data.get("telefono")

    if not nome:
        return jsonify({"error": "Nome obbligatorio"}), 400

    models.add_cliente(nome, email, telefono)
    return jsonify({"status": "cliente creato"}), 201


# =========================
# ORDINI
# =========================

@api.route("/clienti/<int:cliente_id>/ordini", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_ordini(cliente_id):
    return jsonify(models.get_ordini(cliente_id))


@api.route("/clienti/<int:cliente_id>/ordini", methods=["POST"], strict_slashes=False)
@jwt_required()
def add_ordine(cliente_id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON mancante"}), 400

    descrizione = data.get("descrizione")
    importo = data.get("importo")

    if not descrizione:
        return jsonify({"error": "Descrizione obbligatoria"}), 400

    try:
        importo = float(importo)
    except (TypeError, ValueError):
        return jsonify({"error": "Importo non valido"}), 400

    models.add_ordine(cliente_id, descrizione, importo)
    return jsonify({"status": "ordine creato"}), 201