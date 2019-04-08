# models for customer include:
#  1. add new customer
#  2. retrieve customer details
#  3. edit customer details
#  4. delete customer

import psycopg2
import uuid
import os
from datetime import datetime, timedelta

from instance.db_config import DbSetup
from app.api.utils.encryption import Encryption
from app.api.utils.auth import Authorization


class Customer(DbSetup):

    def __init__(self):
        super().__init__()

    #  add new customer to db
    def create_customer(self, first_name, last_name,
                        email, phone, location, password):

        customer_exists_query = """SELECT *
            FROM customers
            WHERE
            phone='{}'
            OR
            email='{}'""".format(phone, email)
        self.cursor.execute(customer_exists_query)
        customer = self.cursor.fetchone()

        if not customer:
            id = str(uuid.uuid4())

            create_customer_query = """INSERT INTO customers
                (id, first_name, last_name, email, phone, location,
                password, registered_on)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""

            self.cursor.execute(create_customer_query,
                                (id, first_name, last_name,
                                 email, phone, location, password,
                                 datetime.now()))

            return dict(
                id=id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                location=location
            )
        else:
            return False

    # retrieve customer details
    def retrieve_customer(self, email, password):

        customer_exists_query = """SELECT *
            FROM customers
            WHERE
            email='{}'""".format(email)
        self.cursor.execute(customer_exists_query)
        customer = self.cursor.fetchone()

        if customer:
            if Encryption().verify_hash(password, customer[6]):
                return dict(
                    id=customer[0],
                    first_name=customer[1],
                    last_name=customer[2],
                    email=customer[3],
                    phone=customer[4],
                    location=customer[5]
                )
        else:
            return False

    #  edit customer details
    def edit_customer(self, id, first_name, last_name,
                      email, phone, location, password):
        customer_exists_query = """SELECT *
            FROM customers
            WHERE
            id='{}'""".format(id)
        self.cursor.execute(customer_exists_query)
        customer = self.cursor.fetchone()

        if customer:
            id = str(uuid.uuid4())

            edit_customer_query = """UPDATE customers
                SET first_name='{}',
                last_name='{}',
                email='{}',
                phone='{}',
                location='{}',
                password='{}'
                WHERE
                id='{}'""".format(first_name, last_name,
                                  email, phone, location, password,
                                  id)

            self.cursor.execute(edit_customer_query)

            return dict(
                id=id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                location=location
            )
        else:
            return False

    #  delete customer
    def delete_customer(self, id):

        delete_customer_query = """DELETE
        FROM customers
        WHERE
        id='{}'""".format(id)
        self.cursor.execute(delete_customer_query)
        row_deleted = self.cursor.rowcount

        if row_deleted:
            return True
