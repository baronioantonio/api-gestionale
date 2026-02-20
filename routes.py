from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required
)
from werkzeug.security import generate_password_hash, check_password_hash
import models
import db
from errors import error

api = Blueprint("api", __name__)

# ==================================================
# AUTH
# ==================================================

@api.route("/register", methods=["POST"])
def register():
    """
    Registrazione utente
    ---
    tags:
      - Auth
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      201:
        description: Utente creato
      400:
        description: Dati non validi
      409:
        description: Utente già esistente
    """
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
    """
    Login utente
    ---
    tags:
      - Auth
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Token JWT
      401:
        description: Credenziali non valide
    """
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


# ==================================================
# CLIENTI (PROTETTI)
# ==================================================

@api.route("/clienti", methods=["GET"])
@jwt_required()
def list_clienti():
    """
    Lista clienti
    ---
    tags:
      - Clienti
    security:
      - BearerAuth: []
    responses:
      200:
        description: Lista clienti
    """
    return jsonify(models.get_clienti())


@api.route("/clienti", methods=["POST"])
@jwt_required()
def create_cliente():
    """
    Crea cliente
    ---
    tags:
      - Clienti
    security:
      - BearerAuth: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nome
          properties:
            nome:
              type: string
            email:
              type: string
            telefono:
              type: string
    responses:
      201:
        description: Cliente creato
      400:
        description: Dati non validi
    """
    data = request.get_json()
    if not data:
        return error("JSON mancante")

    nome = data.get("nome")
    if not nome or len(nome.strip()) < 2:
        return error("Nome non valido")

    models.add_cliente(
        nome,
        data.get("email"),
        data.get("telefono")
    )
    return jsonify({"status": "cliente creato"}), 201


@api.route("/clienti/<int:cid>", methods=["DELETE"])
@jwt_required()
def delete_cliente(cid):
    """
    Elimina cliente
    ---
    tags:
      - Clienti
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: cid
        required: true
        type: integer
    responses:
      200:
        description: Cliente eliminato
    """
    models.delete_cliente(cid)
    return jsonify({"status": "cliente eliminato"})


# ==================================================
# ORDINI (PROTETTI)
# ==================================================

@api.route("/clienti/<int:cid>/ordini", methods=["GET"])
@jwt_required()
def list_ordini(cid):
    """
    Lista ordini di un cliente
    ---
    tags:
      - Ordini
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: cid
        required: true
        type: integer
    responses:
      200:
        description: Lista ordini
    """
    return jsonify(models.get_ordini(cid))


@api.route("/clienti/<int:cid>/ordini", methods=["POST"])
@jwt_required()
def create_ordine(cid):
    """
    Crea ordine per cliente
    ---
    tags:
      - Ordini
    security:
      - BearerAuth: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - descrizione
            - importo
          properties:
            descrizione:
              type: string
            importo:
              type: number
    responses:
      201:
        description: Ordine creato
      400:
        description: Dati non validi
    """
    data = request.get_json()
    if not data:
        return error("JSON mancante")

    descrizione = data.get("descrizione")
    importo = data.get("importo")

    if not descrizione:
        return error("Descrizione obbligatoria")

    try:
        importo = float(importo)
    except (TypeError, ValueError):
        return error("Importo non valido")

    models.add_ordine(cid, descrizione, importo)
    return jsonify({"status": "ordine creato"}), 201