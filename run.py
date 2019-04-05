# initializing the app

from app import create_app
from instance.db_config import DbSetup

app = create_app('development')

db_setup = DbSetup(app)
db_setup.create_customers_table()
db_setup.create_categories_table()
db_setup.create_groceries_table()

if __name__ == '__main__':
    app.run()
