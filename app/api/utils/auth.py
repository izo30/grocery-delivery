#  functionality for generating authentication tokens

import jwt
from flask import request, jsonify, make_response
from datetime import datetime, timedelta
from functools import wraps

from instance.config import secret_key
from app.api.utils.validations import Validations


class Authorization():

    def __init__(self):
        pass

    #  generate authentication token
    def encode_auth_token(self, id, email, role):
        try:
            print("TOKEN id : {}\n TOKEN email : {}\nTOKEN role : {}" .format(id, email, role))
            token = jwt.encode({'id': id, 'user': email, 'role': role,
                               'exp': datetime.utcnow() + timedelta(days=365)},
                               secret_key)

            return token
        except Exception as e:
            print("TOKEN ERROR : {}" .format(e))
            return e

    #  decode authentication token
    def decode_auth_token(self, auth_token):
        try:
            payload = jwt.decode(auth_token, secret_key, algorithms=['HS256'])
            return payload

        except jwt.ExpiredSignatureError:
            return "ExpiredSignatureError"

        except jwt.InvalidTokenError:
            return "InvalidTokenError"


#  decorater to check for an authorised customer
def customer_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        message = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            message = Authorization().decode_auth_token(token)

        if not Validations().token_present(token):
            return {'message': 'Token is missing.'}, 401

        if Validations().check_token_error(message):
            return {'message': message}, 401

        if not Validations().check_if_customer(message['role']):
            return {'message': "You are not a customer"}, 401

        return f(*args, **kwargs)
    return decorated


#  decorater to check for an authorised admin
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        message = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            message = Authorization().decode_auth_token(token)

        if not Validations().token_present(token):
            return {'message': 'Token is missing.'}, 401

        if Validations().check_token_error(message):
            return {'message': message}, 401

        if not Validations().check_if_admin(message['role']):
            return {'message': "You are not an admin"}, 401

        return f(*args, **kwargs)
    return decorated
