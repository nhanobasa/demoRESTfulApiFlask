from app import db

# User model


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
