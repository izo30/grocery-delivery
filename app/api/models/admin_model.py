#  contain models for admin. Include the following models:
#  1. create a new account
#  2. retrieve profile details
#  3. edit profile details
#  4. delete profile

import psycopg2
import uuid
from datetime import datetime

from instance.db_config import DbSetup
from app.api.utils.encryption import Encryption


class Admin(DbSetup):

    def __init__(self):
        super().__init__()

    #  create admin account
    def create_admin(self, first_name, last_name,
                     email, phone, password):
        admin_exists_query = """SELECT *
            FROM admin
            WHERE
            email='{}'
            OR
            phone='{}'""".format(email, phone)
        self.cursor.execute(admin_exists_query)
        admin = self.cursor.fetchone()

        if not admin:

            id = str(uuid.uuid4())

            print("fname : {}\nlname : {}\nemail : {}\nphone : {}\npassword : {}".format(first_name, last_name, email, phone, password))

            create_admin_query = """INSERT INTO admin
            (id, first_name, last_name, email, phone, password, registered_on)
            VALUES('{}','{}','{}','{}','{}','{}','{}')
            """.format(id, first_name, last_name, email, phone, password, datetime.now())

            self.cursor.execute(create_admin_query)

            return dict(
                id=id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone
            )
        else:
            return False

    #  retrieve admin details for login
    def retrieve_admin_login(self, email, password):

        admin_exists_query = """SELECT *
            FROM admin
            WHERE
            email='{}'""".format(email)
        self.cursor.execute(admin_exists_query)
        admin = self.cursor.fetchone()

        if admin:
            if Encryption().verify_hash(password, admin[5]):
                return dict(
                    id=admin[0],
                    first_name=admin[1],
                    last_name=admin[2],
                    email=admin[3],
                    phone=admin[4]
                )
        else:
            return False

    #  edit admin details
    def edit_admin(self, id, first_name, last_name,
                      email, phone, password):
        admin_exists_query = """SELECT *
            FROM admin
            WHERE
            id='{}'""".format(id)
        self.cursor.execute(admin_exists_query)
        admin = self.cursor.fetchone()

        if admin:

            edit_admin_query = """UPDATE admin
                SET first_name='{}',
                last_name='{}',
                email='{}',
                phone='{}',
                password='{}'
                WHERE
                id='{}'""".format(first_name, last_name,
                                  email, phone, password,
                                  id)

            self.cursor.execute(edit_admin_query)

            return dict(
                id=id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone
            )
        else:
            return False