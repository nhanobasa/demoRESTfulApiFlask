from flask import request, Blueprint, jsonify
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
import jwt

from app import db
from app.models.user import User
from app.middlewares.auth import access_token_required


api_user_blp = Blueprint("apiUser", __name__)
api = Api(api_user_blp)


class UserController(Resource):
    def post(self):
        data = request.form

        if not data["username"] or not data["password"] or not data["email"]:
            return {"message": "No Email, username or password provided"}, 401

        exist_user = User.query.filter_by(username=data["username"]).first()
        exist_email = User.query.filter_by(username=data["username"]).first()
        if not exist_user and not exist_email:
            hashed_password = generate_password_hash(data["password"], method="sha256")
            new_user = User(
                email=data["email"], username=data["username"], password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()

            return jsonify({"message": "New user created"})

        return {"message": "Email or Username already exists"}, 401

    @access_token_required
    def get(self):
        users = User.query.all()
        output = []

        for user in users:

            user_data = {}
            user_data["email"] = user.email
            user_data["username"] = user.username
            user_data["password"] = user.password
            output.append(user_data)

        return jsonify({"users": output})

    @access_token_required
    def put(self, current_user):
        pass


api.add_resource(UserController, "/user")
