# create blueprint

from flask import Blueprint
from flask_restplus import Api

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

version1 = Blueprint('api version 1', __name__, url_prefix='/api')
api = Api(version1, title='Grocery Delivery API', version='1.0', description='An application\
    that helps customers buy groceries online', authorizations=authorizations)
