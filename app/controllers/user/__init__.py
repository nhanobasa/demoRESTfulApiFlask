from flask import request, Blueprint, jsonify
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash

from app import db
from app.middlewares.auth import access_token_required
from app.models import User

api_user_blp = Blueprint("apiUser", __name__)
api = Api(api_user_blp)


class UserController(Resource):
    """
    Create new User

    Parameters: 
    username (str): 
    password (str):
    email (str):

    Returns:
    Create new User

    """
    def post(self):
        data = request.form

        if not data["username"] or not data["password"] or not data["email"]:
            return {"error": "No Email, username or password provided"}, 401

        exist_user = User.query.filter_by(username=data["username"]).first()
        exist_email = User.query.filter_by(email=data["email"]).first()
        if not exist_user and not exist_email:
            hashed_password = generate_password_hash(data["password"],
                                                     method="sha256")
            new_user = User(email=data["email"],
                            username=data["username"],
                            password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            return jsonify({"message": "New user created"})

        return {"error": "Email or Username already exists"}, 401

    """
    Get user details by public_id (query params)

    Parameters:
    public_id (str): public_id of user from query params

    Returns:
    User_data: Data of user
    """

    def get(self):
        public_id_from_qp = request.args.get('public_id')
        user = User.query.filter_by(public_id=public_id_from_qp).first()
        if not user:
            return {"error": "No users found"}

        user_data = {"email": user.email, "username": user.username, "posts": []}

        for post in user.posts:
            if post.private == False:
                post_data = {'id': post.id, 'title': post.title, 'body': post.body, 'pub_date': post.pub_date,
                             'private': post.private}
                user_data['posts'].append(post_data)

        return jsonify({"users": user_data})

    """
    Get user details by public_id (query params)

    Parameters:
    current_user : Sau khi kiểm tra access_token, nếu như hợp lệ, sẽ trả về thông tin của user tương ứng
    email : Email address muốn thay thế.
    Returns:
    User_data: Email được update.
    """

    @access_token_required
    def put(current_user, self):
        data = request.form

        user = User.query.filter_by(id=current_user.id).first()
        try:
            user.email = data["email"]
            db.session.commit()
        except:
            return {'error': 'Email already exists'}, 500
        return {'message': 'Update user successfully!'}

    @access_token_required
    def delete(current_user, self):
        user = User.query.filter_by(public_id=current_user.public_id).first()

        if not user:
            return jsonify({'message': 'No user found!'})

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'The user has been deleted!'})


api.add_resource(UserController, "/user")