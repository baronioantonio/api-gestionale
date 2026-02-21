from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flasgger import Swagger
import db
from routes import api

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret-key-cambia-questa"
JWTManager(app)

Swagger(app)

@app.route("/")
def home():
    return jsonify({"status": "API online"})

db.init_db()
app.register_blueprint(api)