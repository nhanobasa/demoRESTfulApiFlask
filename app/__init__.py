from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Config
app.config.from_object("config.DevelopmentClass")

# Init db
db = SQLAlchemy(app)

from app.controllers.login import api_login_blp
from app.controllers.user import api_user_blp

app.register_blueprint(api_user_blp, url_prefix="/api")
app.register_blueprint(api_login_blp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
