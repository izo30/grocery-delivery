#  contain views for categories. Include the follwoing:
#  1. post a category
#  2. get all categories
#  3. delete a category

from flask_restplus import Resource

from app.api.models.category_model import Category
from app.api.utils.validations import Validations
from app.api.utils.auth import Authorization, admin_required
from app.api.utils.validations import Validations
from app.api.utils.fields import categories_api as api, CategoriesFields


# category endpoints
@api.route('')
class CategoryViews(Resource):

    @api.expect(CategoriesFields.create_category_fields)
    @api.doc(security='apikey')
    @admin_required
    def post(self):
        """create new category"""

        args = CategoriesFields.create_category_args()
        name = args['name']

        validate = Validations().validate_category(name)

        if validate:
            return {
                'status': 'Fail',
                'error': validate['error']
            }, 400

        created_category = Category().create_category(name)

        if created_category:

            return {
                'status': 'Success',
                'message': 'Created category successfully',
                'category': created_category
            }, 201
        else:
            return {
                'status': 'Fail',
                'error': 'Category already exists'
            }, 403
