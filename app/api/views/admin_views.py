#  contain views for admin. Include the follwoing:
#  1. post admin account
#  2. get admin profile
#  3. put/patch admin profile
#  4. delete admin profile

from flask_restplus import Resource

from app.api.models.admin_model import Admin
from app.api.utils.validations import Validations
from app.api.utils.auth import Authorization
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
