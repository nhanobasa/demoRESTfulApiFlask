from dotenv import load_dotenv
from datetime import datetime, timedelta
from flask import request, Blueprint, jsonify
from flask_restful import Resource, Api
import jwt
import os
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

from app.models.user import User


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
REFRESH_KEY = os.getenv('REFRESH_KEY')

api_login_blp = Blueprint('apiLogin', __name__)
api = Api(api_login_blp)


class LoginController(Resource):
    def post(self):
        data = request.form
        if not data['username'] or not data['password']:
            return {'message': "No username or password provided"}, 401
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return {'message': 'Username not found'}, 401
        if check_password_hash(user.password, data['password']):
            # if true, return jwt token
            payload = {'user_id': user.id,
                       'username': user.username, 'exp': datetime.utcnow() + timedelta(minutes=30)}
            access_token = jwt.encode(payload, SECRET_KEY)

            payload['exp'] = datetime.utcnow(
            ) + timedelta(days=365)
            refresh_token = jwt.encode(payload, REFRESH_KEY)

            # return access_token and refresh_token
            return {'access_token': access_token.decode('utf-8'), 'refresh_token': refresh_token.decode('utf-8')}


api.add_resource(LoginController, '/login')
