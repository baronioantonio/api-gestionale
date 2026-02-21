import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flasgger import Swagger
import db
from routes import api

app = Flask(__name__)

# ---------- JWT ----------
app.config["JWT_SECRET_KEY"] = "super-secret-key-cambia-questa"
jwt = JWTManager(app)

# ---------- SWAGGER ----------
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API Gestionale",
        "description": "Backend Flask con JWT, Clienti e Ordini",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Inserisci: Bearer <JWT>"
        }
    }
}

Swagger(app, template=swagger_template)

# ---------- DB + ROUTES ----------
db.init_db()
app.register_blueprint(api)

# ---------- AVVIO COMPATIBILE RAILWAY ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)