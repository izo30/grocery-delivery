#  contain views for admin. Include the follwoing:
#  1. post admin account
#  2. get admin profile
#  3. put/patch admin profile
#  4. delete admin profile

from flask_restplus import Resource

from app.api.models.admin_model import Admin
from app.api.utils.validations import Validations
from app.api.utils.auth import Authorization, admin_required
from app.api.utils.validations import Validations
from app.api.utils.fields import admin_api as api, AdminFields
from app.api.utils.encryption import Encryption


# admin endpoints
@api.route('')
class AdminViews(Resource):

    @api.expect(AdminFields.create_account_fields)
    def post(self):
        """create new admin"""

        args = AdminFields.create_account_args()
        first_name = args['first_name']
        last_name = args['last_name']
        email = args['email']
        phone = args['phone']
        password = args['password']
        role = args['role']

        validate = Validations().validate_registration_data(first_name,
                                                            last_name,
                                                            email,
                                                            phone,
                                                            password,
                                                            role)

        if validate:
            return {
                'status': 'Fail',
                'error': validate['error']
            }, 400

        created_admin = Admin().create_admin(first_name, last_name,
                                             email, phone,
                                             Encryption()
                                             .generate_hash(password))

        if created_admin:
            token = Authorization().encode_auth_token(created_admin['id'],
                                                      email, role)
            return {
                'status': 'Success',
                'message': 'Signed up successfully',
                'customer': created_admin,
                'auth_token': token.decode('UTF-8')
            }, 201
        else:
            return {
                'status': 'Fail',
                'error': 'Email or phone already exists'
            }, 403

    @api.expect(AdminFields.edit_account_fields)
    @api.doc(security='apikey')
    @admin_required
    def patch(self):
        """edit existing customer  account details"""

        args = AdminFields.edit_args()
        id = args['id']
        first_name = args['first_name']
        last_name = args['last_name']
        email = args['email']
        phone = args['phone']
        password = args['password']
        role = args['role']

        validate = Validations().validate_registration_data(first_name,
                                                            last_name,
                                                            email, phone,
                                                            password, role)
        if validate:
            return {
                'status': 'Fail',
                'error': validate['error']
            }, 400

        edited_admin = Admin().edit_admin(id, first_name, last_name,
                                          email, phone,
                                          Encryption()
                                          .generate_hash(password))
        if edited_admin:
            return {
                'status': 'Success',
                'message': 'Edited successfully',
                'customer': edited_admin
            }, 201
        else:
            return {
                'status': 'Fail',
                'error': 'Admin cannot be edited or does not exist'
            }, 403

    @api.expect(AdminFields.delete_account_fields)
    @api.doc(security='apikey')
    @admin_required
    def delete(self):
        """delete an existing admin"""

        args = AdminFields.delete_args()
        id = args['id']

        if not id:
            return {
                'status': 'Fail',
                'error': 'ID should not be empty'
            }, 400

        if Admin().delete_admin(id):
            return {
                'status': 'Success',
                'message': 'Deleted successfully'
            }, 201
        else:
            return {
                'status': 'Fail',
                'error': 'Admin cannot be deleted or does not exist'
            }, 403


# admin Login endpoint
@api.route('/login')
class AdminLogin(Resource):
    @api.expect(AdminFields.login_fields)
    def post(self):
        """login admin"""

        args = AdminFields.login_args()
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

        admin = Admin().retrieve_admin_login(email, password)
        if admin:
            token = Authorization().encode_auth_token(admin['id'],
                                                      email, role)
            return {
                'status': 'Success',
                'message': 'Logged in successfully',
                'admin': admin,
                'auth_token': token.decode('UTF-8')
            }, 200
        else:
            return {
                'status': 'Fail',
                'message': 'Wrong email or password'
            }, 403
