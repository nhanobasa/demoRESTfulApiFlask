from dotenv import load_dotenv
from flask import request
from functools import wraps
import jwt
import os
from app.models.user import User

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


def access_token_required(fun_c):
    @wraps(fun_c)
    def decorated(*args, **kwargs):
        access_token = None

        if "Authorization" in request.headers:
            access_token = (
                str(request.headers["Authorization"]).replace("Bearer", "").strip()
            )
        if not access_token:
            return {"message": "No access_token provided!"}
        try:
            print(SECRET_KEY)
            data = jwt.decode(access_token, SECRET_KEY)
            current_user = User.query.filter_by(username=data["username"]).first()
        except:
            return {"message": "Token is invalid!"}, 401
        return fun_c(current_user, *args, **kwargs)

    return decorated
