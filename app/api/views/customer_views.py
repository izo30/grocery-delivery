# Views for customer. Contain the following endpoints:
#  1. CustomerAccount
#       - post
#       - patch
#       - delete
#  2. Login
#       - post

from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields

from app.api.models.customer_model import Customer
from app.api.utils.validations import Validations
from app.api.utils.auth import Authorization
from app.api.utils.encryption import Encryption
from app.api.utils.fields import customer_api as api, CustomerFields


# customer account endpoints
@api.route('/account')
class CustomerAccount(Resource):

    @api.expect(CustomerFields.signup_fields)
    def post(self):
        """signup new customer"""

        parser = CustomerFields.signup_parser()
        args = parser.parse_args()
        first_name = args['first_name']
        last_name = args['last_name']
        email = args['email']
        phone = args['phone']
        location = args['location']
        password = args['password']
        role = args['role']

        validate = Validations().validate_customer_data(first_name, last_name,
                                                        email, phone, location,
                                                        password, role)
        if validate:
            return {
                'status': 'Fail',
                'error': validate['error']
            }, 400

        created_customer = Customer().create_customer(first_name, last_name,
                                                      email, phone, location,
                                                      Encryption().generate_hash(password))
        if created_customer:
            token = Authorization().encode_auth_token(created_customer['id'],
                                                      email, role)
            return {
                'status': 'Success',
                'message': 'Signed up successfully',
                'auth_token': token.decode('UTF-8')
            }, 201
        else:
            return {
                'status': 'Fail',
                'error': 'User already exists, signup with another email'
            }, 403
