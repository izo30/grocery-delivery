# create blueprint

from flask import Blueprint
from flask_restplus import Api

from app.api.views.customer_views import api as customers
from app.api.views.admin_views import api as admin
from app.api.views.category_views import api as categories
from app.api.views.grocery_views import api as groceries

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

version1 = Blueprint('api version 1', __name__, url_prefix='/api')
api = Api(version1, title='Grocery Delivery API', version='1.0', description='An application\
    that helps customers buy groceries online', authorizations=authorizations)

api.add_namespace(customers, path='/customers')
api.add_namespace(admin, path='/admin')
api.add_namespace(categories, path='/categories')
api.add_namespace(groceries, path='/groceries')
