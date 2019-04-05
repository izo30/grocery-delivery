
# contains configuration for tests
from app import create_app

from unittest import TestCase
import os
import json

from instance.db_config import DbSetup


class BaseTest(TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()

        DbSetup().create_categories_table()
        DbSetup().create_customers_table()
        DbSetup().create_groceries_table()

    def tearDown(self):
        DbSetup().drop_tables()
        self.app_context.pop()
