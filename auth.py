from flask import request, abort
from flask_login import current_user
from functools import wraps
from werkzeug.security import check_password_hash
from models.user import UserModel
from models.superuser import SuperuserModel
from blacklist import BLACKLIST


def requireApiKey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('api_key')
        user = UserModel.find_by_key(api_key)

        if api_key and user:
            # check to see if user is denied access
            if api_key in BLACKLIST:
                return abort(401)
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function


def requireAdmin(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        username = request.headers.get('username')
        password = request.headers.get('password')

        user = UserModel.find_by_username(username)

        if user:
            superuser = SuperuserModel.find_by_username(user.username)

            if superuser:
                if check_password_hash(user.password, password):
                    return view_function(*args, **kwargs)

        abort(401)

    return decorated_function
