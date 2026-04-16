from functools import wraps
from secrets import compare_digest
from flask import request

from parameters import WEBSERVER_PASSWORD

def check_auth(username, password):
    return WEBSERVER_PASSWORD == "" or (username == 'admin' and compare_digest(password, WEBSERVER_PASSWORD))

def login_required(f):
    @wraps(f)
    def wrapped_view(**kwargs):
        auth = request.authorization
        if WEBSERVER_PASSWORD != "" and not (auth and check_auth(auth.username, auth.password)):
            return ('Unauthorized', 401, {
                'WWW-Authenticate': 'Basic realm="Login Required"'
            })

        return f(**kwargs)

    return wrapped_view
