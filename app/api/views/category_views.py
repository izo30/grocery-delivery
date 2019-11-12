#  contain views for categories. Include the following:
#  1. post a category
#  2. get all categories
#  3. delete a category

from flask_restplus import Resource

from app.api.models.category_model import Category
from app.api.utils.validations import Validations
from app.api.utils.auth import Authorization, admin_required
from app.api.utils.fields import categories_api as api, CategoriesFields


# category endpoints
@api.route('')
class CategoryViews(Resource):

    @api.expect(CategoriesFields.create_category_fields)
    @api.doc(security='apikey')
    @admin_required
    def post(self):
        """Create new category"""

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

    def get(self):
        """Get all categories"""
        categories = Category().retrieve_all_categories()

        if categories:
            return {
                'status': 'Success',
                'categories': categories
            }, 200
        else:
            return {
                'status': 'Fail',
                'error': 'No category found'
            }, 404

    @api.expect(CategoriesFields.delete_category_fields)
    @api.doc(security='apikey')
    @admin_required
    def delete(self):
        """Delete an existing category"""

        args = CategoriesFields.delete_args()
        id = args['id']

        if not id:
            return {
                'status': 'Fail',
                'error': 'ID should not be empty'
            }, 400

        if Category().delete_category(id):
            return {
                'status': 'Success',
                'message': 'Deleted successfully'
            }, 201
        else:
            return {
                'status': 'Fail',
                'error': 'Category cannot be deleted or does not exist'
            }, 404
