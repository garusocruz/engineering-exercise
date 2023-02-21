from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from settings import MYSQL_DB, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER

server = Flask(__name__)
server.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
server.config["DB"] = SQLAlchemy(server)
