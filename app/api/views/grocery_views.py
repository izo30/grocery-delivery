#  contain views for groceries. Include the following:
#  1. post a grocery
#  2. get all groceries
#  3. get all groceries for a specific category
#  4. patch a grocery item
#  3. delete a grocery item

from flask_restplus import Resource

from app.api.models.grocery_model import Grocery
from app.api.utils.validations import Validations
from app.api.utils.auth import Authorization, admin_required
from app.api.utils.fields import groceries_api as api, GroceriesFields


# grocery endpoints
@api.route('')
class GroceryViews(Resource):

    @api.expect(GroceriesFields.create_grocery_fields)
    @api.doc(security='apikey')
    @admin_required
    def post(self):
        """Create new grocery"""

        args = GroceriesFields.create_grocery_args()
        category_id = args['category_id']
        name = args['name']
        price = args['price']
        quantity = args['quantity']

        validate = Validations().validate_grocery_data(category_id,
                                                       name,
                                                       price,
                                                       quantity)

        if validate:
            return {
                'status': 'Fail',
                'error': validate['error']
            }, 400

        if not Grocery().category_exists(category_id):
            return {
                'status': 'Fail',
                'error': 'Grocery category does not exist'
            }, 404

        created_grocery = Grocery().create_grocery(category_id,
                                                   name,
                                                   price,
                                                   quantity)

        if created_grocery:
            return {
                'status': 'Success',
                'message': 'Created grocery successfully',
                'category': created_grocery
            }, 201
        else:
            return {
                'status': 'Fail',
                'error': 'Grocery already exists'
            }, 403

    def get(self):
        """Get all groceries"""
        groceries = Grocery().retrieve_all_groceries()

        if groceries:
            return {
                'status': 'Success',
                'groceries': groceries
            }, 200
        else:
            return {
                'status': 'Fail',
                'error': 'No grocery found'
            }, 404

    @api.expect(GroceriesFields.edit_grocery_fields)
    @api.doc(security='apikey')
    @admin_required
    def patch(self):
        """Edit existing grocery item details"""

        args = GroceriesFields.edit_grocery_args()
        id = args['id']
        category_id = args['category_id']
        name = args['name']
        price = args['price']
        quantity = args['quantity']

        if not id:
            return {
                'status': 'Fail',
                'error': 'ID cannot be empty'
            }, 400

        validate = Validations().validate_grocery_data(category_id,
                                                       name,
                                                       price,
                                                       quantity)

        if validate:
            return {
                'status': 'Fail',
                'error': validate['error']
            }, 400

        edited_grocery = Grocery().edit_grocery(id,
                                                category_id,
                                                name,
                                                price,
                                                quantity)
        if edited_grocery:
            return {
                'status': 'Success',
                'message': 'Edited successfully',
                'customer': edited_grocery
            }, 201
        else:
            return {
                'status': 'Fail',
                'error': 'Grocery cannot be edited or does not exist'
            }, 403

# single grocery endpoints
@api.route('/<string:grocery_id>')
class SingleGroceryViews(Resource):

    def get(self, grocery_id):
        """Fetch a single grocery item"""

        if not grocery_id:
            return {
                'status': 'Fail',
                'error': 'Grocery id cannot be empty'
            }, 400

        grocery = Grocery().retrieve_single_grocery(grocery_id)

        if grocery:
            return {
                'status': 'Success',
                'grocery': grocery
            }, 200
        else:
            return {
                'status': 'Fail',
                'error': 'Category cannot be deleted or does not exist'
            }, 404

    @api.doc(security='apikey')
    @admin_required
    def delete(self, grocery_id):
        """Delete an existing grocery"""

        if not grocery_id:
            return {
                'status': 'Fail',
                'error': 'Grocery id should not be empty'
            }, 400

        if Grocery().delete_grocery(grocery_id):
            return {
                'status': 'Success',
                'message': 'Deleted successfully'
            }, 201
        else:
            return {
                'status': 'Fail',
                'error': 'Grocery cannot be deleted or does not exist'
            }, 404

# category groceries endpoints
@api.route('/category/<string:category_id>')
class CategoryViews(Resource):

    def get(self, category_id):
        """Fetch groceries for a specific category"""

        if not category_id:
            return {
                'status': 'Fail',
                'error': 'Category id cannot be empty'
            }, 400

        groceries = Grocery().retrieve_category_groceries(category_id)

        if groceries:
            return {
                'status': 'Success',
                'groceries': groceries
            }, 200
        else:
            return {
                'status': 'Fail',
                'error': 'No grocery found'
            }, 404
