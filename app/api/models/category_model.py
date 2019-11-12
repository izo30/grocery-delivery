#  contain models for groceries categories. Include the following models:
#  1. create a new category
#  2. retrieve all categories
#  3. delete category

import psycopg2
import uuid
from datetime import datetime

from instance.db_config import DbSetup


class Category(DbSetup):

    #  create new category
    def create_category(self, name):
        category_exists_query = """SELECT *
            FROM categories
            WHERE
            name='{}'""".format(name)
        self.cursor.execute(category_exists_query)
        category = self.cursor.fetchone()

        if not category:

            id = str(uuid.uuid4())

            create_category_query = """INSERT INTO categories
            (id, name, created_on)
            VALUES('{}','{}','{}')
            """.format(id, name, datetime.now())

            self.cursor.execute(create_category_query)

            return dict(
                id=id,
                name=name
            )
        else:
            return False

    # retrieve all categories
    def retrieve_all_categories(self):

        retrieve_all_categories_query = """
            SELECT *
            FROM categories"""
        self.cursor.execute(retrieve_all_categories_query)

        rows = self.cursor.fetchall()

        if rows:
            categories = []

            for row in rows:
                category = dict(
                    id=row[0],
                    name=row[1],
                    created_on=row[2]
                )
                categories.append(category)

            return categories
        else:
            return False

    # delete a category
    def delete_category(self, id):

        delete_category_query = """
            DELETE
            FROM categories
            WHERE id = '{}'""".format(id)

        self.cursor.execute(delete_category_query)
        row_deleted = self.cursor.rowcount

        if row_deleted:
            return True
        else:
            return False
