from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "API online"})

@app.route("/ping")
def ping():
    return jsonify({"ping": "pong"})