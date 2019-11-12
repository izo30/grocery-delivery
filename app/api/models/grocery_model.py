#  contain models for groceries. Include the follwoing:
#  1. create grocery item
#  2. retrieve all groceries
#  3. retrieve all groceries for specific category
#  4. edit grocery item
#  5. delete grocery item

import psycopg2
import uuid
from datetime import datetime

from instance.db_config import DbSetup


class Grocery(DbSetup):

    #  check if category id exists
    def category_exists(self, category_id):
        category_exists_query = """SELECT *
            FROM categories
            WHERE
            id='{}'""".format(category_id)
        self.cursor.execute(category_exists_query)
        category = self.cursor.fetchone()

        if category:
            return True
        else:
            return False

    #  create new grocery
    def create_grocery(self, category_id, name, price, quantity):
        grocery_exists_query = """SELECT *
            FROM groceries
            WHERE
            name='{}'""".format(name)
        self.cursor.execute(grocery_exists_query)
        grocery = self.cursor.fetchone()

        if not grocery:

            id = str(uuid.uuid4())

            create_grocery_query = """INSERT INTO groceries
            (id, category_id, name, price, quantity, created_on)
            VALUES('{}','{}','{}','{}','{}','{}')
            """.format(id, category_id, name, price, quantity, datetime.now())

            self.cursor.execute(create_grocery_query)

            return dict(
                id=id,
                category_id=category_id,
                name=name,
                price=price,
                quantity=quantity
            )
        else:
            return False

    # retrieve all groceries
    def retrieve_all_groceries(self):

        retrieve_all_groceries_query = """
            SELECT *
            FROM groceries"""
        self.cursor.execute(retrieve_all_groceries_query)

        rows = self.cursor.fetchall()

        if rows:
            groceries = []

            for row in rows:
                grocery = dict(
                    id=row[0],
                    category_id=row[1],
                    name=row[2],
                    price=row[3],
                    quantity=row[4],
                    created_on=row[5]
                )
                groceries.append(grocery)

            return groceries
        else:
            return False

    #  retrieve single grocery item
    def retrieve_single_grocery(self, grocery_id):
        retrieve_grocery_query = """SELECT *
            FROM groceries
            WHERE
            id='{}'""".format(grocery_id)
        self.cursor.execute(retrieve_grocery_query)
        grocery = self.cursor.fetchone()

        if grocery:
            return dict(
                id=grocery[0],
                category_id=grocery[1],
                name=grocery[2],
                price=grocery[3],
                quantity=grocery[4],
                created_on=grocery[5]
            )
        else:
            return False

    # retrieve category groceries
    def retrieve_category_groceries(self, category_id):

        retrieve_category_groceries_query = """
            SELECT *
            FROM groceries
            WHERE
            category_id='{}'""".format(category_id)
        self.cursor.execute(retrieve_category_groceries_query)

        rows = self.cursor.fetchall()

        if rows:
            groceries = []

            for row in rows:
                grocery = dict(
                    id=row[0],
                    category_id=row[1],
                    name=row[2],
                    price=row[3],
                    quantity=row[4],
                    created_on=row[5]
                )
                groceries.append(grocery)

            return groceries
        else:
            return False

    #  edit customer details
    def edit_grocery(self, id, category_id, name, price, quantity):
        grocery_exists_query = """SELECT *
            FROM groceries
            WHERE
            id='{}'""".format(id)
        self.cursor.execute(grocery_exists_query)
        grocery = self.cursor.fetchone()

        if grocery:
            edit_grocery_query = """UPDATE groceries
                SET category_id='{}',
                name='{}',
                price='{}',
                quantity='{}'
                WHERE
                id='{}'""".format(category_id, name, price, quantity, id)

            self.cursor.execute(edit_grocery_query)

            return dict(
                id=id,
                category_id=category_id,
                name=name,
                price=price,
                quantity=quantity
            )
        else:
            return False

    #  delete grocery
    def delete_grocery(self, id):

        delete_grocery_query = """DELETE
        FROM groceries
        WHERE
        id='{}'""".format(id)
        self.cursor.execute(delete_grocery_query)
        row_deleted = self.cursor.rowcount

        if row_deleted:
            return True
