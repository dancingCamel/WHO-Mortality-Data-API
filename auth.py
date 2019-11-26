from models.user import UserModel
from functools import wraps
from flask import request, abort
from flask_login import current_user


def requireApiKey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('api_key')
        user = UserModel.find_by_key(api_key)
        # api_key = api_key.replace('Basic ', '', 1)
        if api_key and user:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function
