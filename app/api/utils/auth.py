#  functionality for generating authentication tokens

import jwt
from flask import request, jsonify, make_response
from datetime import datetime, timedelta
from functools import wraps

from instance.config import secret_key


class Authorization():

    def __init__(self):
        pass

    #  generate authentication token
    def encode_auth_token(self, id, email, role):
        try:
            token = jwt.encode({'id': id, 'user': email, 'role': role,
                               'exp': datetime.utcnow() + timedelta(days=365)},
                               secret_key)

            return token
        except Exception as e:
            return e

    #  decode authentication token
    def decode_auth_token(self, auth_token):
        try:
            payload = jwt.decode(auth_token, secret_key, algorithms=['HS256'])
            return payload

        except jwt.ExpiredSignatureError:
            return jwt.ExpiredSignatureError

        except jwt.InvalidTokenError:
            return jwt.InvalidTokenError
