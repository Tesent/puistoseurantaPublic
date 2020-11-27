from functools import wraps
from flask import request, jsonify

def check_auth(username, password):
    return username == "laite" and password == "VahvaSalausOnVahva"

def login_required(f):
    @wraps(f)
    def wrapped_view(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            message = {'error': 'Basic Authentication required.'}
            resp = jsonify(message)
            resp.status_code = 401
            return resp

        return f(*args, **kwargs)

    return wrapped_view
