# Contain required fields for API endpoints
# Have the following fields:
#  1. Customer fields
#  2. Groceries fields
#  3. Categories fields

from flask_restplus import reqparse, Api, Namespace, fields
from app.api.utils.validations import Validations

customer_api = Namespace('Customer Endpoints', description='A collection of\
                          customer endpoints')


class CustomerFields():
    @staticmethod
    def signup_parser():
        parser = reqparse.RequestParser()
        Validations().add_arguments(parser, ['first_name', 'last_name',
                                             'email', 'phone', 'location', 
                                             'password', 'role'])
        return parser

    signup_fields = customer_api.model('Signup', {
        'first_name': fields.String,
        'last_name': fields.String,
        'email': fields.String,
        'phone': fields.String,
        'location': fields.String,
        'password': fields.String,
        'role': fields.String
    })
