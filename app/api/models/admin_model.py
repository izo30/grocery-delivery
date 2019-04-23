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
