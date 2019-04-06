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
            email='{}'""".format(email)
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
                location=location
            )
        else:
            return False

    # retrieve customer details
    def retrieve_customer(self, email, password):

        print("SENT PASSWORD: {}" .format(password))

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
