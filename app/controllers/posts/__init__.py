from flask import Blueprint, request, jsonify
from app.middlewares.auth import access_token_required

from app.models import User, Post
from app import db
api_post_blp = Blueprint("post", __name__)


@api_post_blp.route('/', methods=["POST"])
@access_token_required
def create_new_post(current_user):
    data = request.form
    new_post = Post(title=data['title'],
                    body=data['body'],
                    user_id=current_user.id,
                    private=bool(data['private']) or False)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({"message": "Post created."})


@api_post_blp.route('/', methods=["GET"])
@access_token_required
def get_all_post(current_user):
    posts = Post.query.filter_by(user_id=current_user.id).all()
    outputs = []
    for post in posts:
        post_data = {}
        post_data['id'] = post.id
        post_data['title'] = post.title
        post_data['body'] = post.body
        post_data['pub_date'] = post.pub_date
        post_data['private'] = post.private
        outputs.append(post_data)

    return jsonify({"list_posts": outputs})
