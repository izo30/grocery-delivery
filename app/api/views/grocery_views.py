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
        """create new grocery"""

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