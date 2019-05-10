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
    def signup_args():
        parser = reqparse.RequestParser()
        Validations().add_arguments(parser, ['first_name', 'last_name',
                                             'email', 'phone', 'location',
                                             'password', 'role'])
        return parser.parse_args()

    signup_fields = customer_api.model('Signup Customer', {
        'first_name': fields.String,
        'last_name': fields.String,
        'email': fields.String,
        'phone': fields.String,
        'location': fields.String,
        'password': fields.String,
        'role': fields.String
    })

    @staticmethod
    def login_args():
        parser = reqparse.RequestParser()
        Validations().add_arguments(parser, ['email', 'password', 'role'])
        return parser.parse_args()

    login_fields = customer_api.model('Login Customer', {
        'email': fields.String,
        'password': fields.String,
        'role': fields.String
    })

    @staticmethod
    def edit_args():
        parser = reqparse.RequestParser()
        Validations().add_arguments(parser, ['id', 'first_name', 'last_name',
                                             'email', 'phone', 'location',
                                             'password', 'role'])
        return parser.parse_args()

    edit_account_fields = customer_api.model('Edit Customer Account', {
        'id': fields.String,
        'first_name': fields.String,
        'last_name': fields.String,
        'email': fields.String,
        'phone': fields.String,
        'location': fields.String,
        'password': fields.String,
        'role': fields.String
    })

    @staticmethod
    def delete_args():
        parser = reqparse.RequestParser()
        Validations().add_arguments(parser, ['id'])
        return parser.parse_args()

    delete_account_fields = customer_api.model('Delete Customer Account', {
        'id': fields.String
    })


admin_api = Namespace('Admin Endpoints', description='A collection of\
                          admin endpoints')


class AdminFields():
    @staticmethod
    def create_account_args():
        parser = reqparse.RequestParser()
        Validations().add_arguments(parser, ['first_name', 'last_name',
                                             'email', 'phone', 'password',
                                             'role'])
        return parser.parse_args()

    create_account_fields = admin_api.model('Create Admin Account', {
        'first_name': fields.String,
        'last_name': fields.String,
        'email': fields.String,
        'phone': fields.String,
        'password': fields.String,
        'role': fields.String
    })

    @staticmethod
    def login_args():
        parser = reqparse.RequestParser()
        Validations().add_arguments(parser, ['email', 'password', 'role'])
        return parser.parse_args()

    login_fields = admin_api.model('Login Admin', {
        'email': fields.String,
        'password': fields.String,
        'role': fields.String
    })

    @staticmethod
    def edit_args():
        parser = reqparse.RequestParser()
        Validations().add_arguments(parser, ['id', 'first_name', 'last_name',
                                             'email', 'phone',
                                             'password', 'role'])
        return parser.parse_args()

    edit_account_fields = admin_api.model('Edit Admin Account', {
        'id': fields.String,
        'first_name': fields.String,
        'last_name': fields.String,
        'email': fields.String,
        'phone': fields.String,
        'password': fields.String,
        'role': fields.String
    })

    @staticmethod
    def delete_args():
        parser = reqparse.RequestParser()
        Validations().add_arguments(parser, ['id'])
        return parser.parse_args()

    delete_account_fields = admin_api.model('Delete Admin Account', {
        'id': fields.String
    })
