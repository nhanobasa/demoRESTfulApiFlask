from app import db
from datetime import datetime
import uuid
# User model


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    posts = db.relationship('Post', backref=db.backref('post', lazy=True))

    def __init__(self, email, username, password):
        self.public_id = str(uuid.uuid4())
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.String(50), db.ForeignKey('user.public_id'))

    def __repr__(self):
        return '<Post {}>'.format(self.title)
