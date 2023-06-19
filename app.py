from flask import Flask
from flask_cors import CORS
import os
import mysql.connector
import json as json
from flask import Flask, jsonify, request

app = Flask(__name__)

CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

port = int(os.environ.get("PORT", 5000))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)