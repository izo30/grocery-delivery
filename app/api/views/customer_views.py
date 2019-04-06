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

        args = CustomerFields.signup_args()
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
                                                      Encryption()
                                                      .generate_hash(password))
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

# customer login
@api.route('/login')
class Login(Resource):

    @api.expect(CustomerFields.login_fields)
    def post(self):
        """login an existing customer"""

        args = CustomerFields.login_args()
        email = args['email']
        password = args['password']
        role = args['role']

        is_empty = Validations().check_if_empty(dict(email=email,
                                                     password=password,
                                                     role=role))
        if is_empty:
            return {
                'status': 'Fail',
                'error': is_empty
            }, 400

        if not Validations().validate_email(email):
            return {
                'status': 'Fail',
                'error': 'Invalid email'
            }, 400

        if not Validations().check_if_role(role):
            return {
                'status': 'Fail',
                'error': 'Invalid role'
            }, 400

        customer = Customer().retrieve_customer(email, password)
        if customer:
            token = Authorization().encode_auth_token(customer['id'],
                                                      email, role)
            return {
                'status': 'Success',
                'message': 'Logged in successfully',
                'customer': customer,
                'auth_token': token.decode('UTF-8')
            }, 200
        else:
            return {
                'status': 'Fail',
                'message': 'Wrong email or password'
            }, 403
