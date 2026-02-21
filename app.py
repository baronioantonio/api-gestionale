from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
import db
from routes import api

app = Flask(__name__)

# JWT
app.config["JWT_SECRET_KEY"] = "super-secret-key-cambia-questa"
JWTManager(app)

# Health check / root
@app.route("/")
def home():
    return jsonify({"status": "API online"})

# DB + API
db.init_db()
app.register_blueprint(api)

# ⚠️ NIENTE app.run()
# Gunicorn gestisce l'avvio

@app.route("/_routes")
def _routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            "rule": rule.rule,
            "methods": sorted(list(rule.methods))
        })
    return {"routes": routes}