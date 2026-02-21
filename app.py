import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flasgger import Swagger
import db
from routes import api

app = Flask(__name__)

# JWT
app.config["JWT_SECRET_KEY"] = "super-secret-key-cambia-questa"
jwt = JWTManager(app)

# Swagger (anche se online non lo useremo)
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API Gestionale",
        "version": "1.0.0"
    }
}
Swagger(app, template=swagger_template)

# Route di test
@app.route("/")
def home():
    return jsonify({"status": "API online"})

# DB + API
db.init_db()
app.register_blueprint(api)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)