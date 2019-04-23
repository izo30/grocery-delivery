# setup tables and database connection

from flask import current_app
import os
from datetime import datetime
import uuid

import psycopg2
from passlib.hash import pbkdf2_sha256 as sha256


class DbSetup():

    def __init__(self, app=None):

        self.app = app

        current_context = self.context_switcher()

        self.db_name = current_context.config['DB_NAME']
        self.db_user = current_context.config['DB_USERNAME']
        self.db_password = current_context.config['DB_PASSWORD']
        self.db_host = current_context.config['DB_HOST']

        self.connection = psycopg2.connect(
            database=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.db_host
        )
        self.connection.autocommit = True

        try:
            self.cursor = self.connection.cursor()
            print("CONNECTION_SUCCESS!!")
        except:
            print("CONNECTION_ERROR!!")

    def context_switcher(self):
        """get current passed context to the dbModel"""
        if current_app:
            return current_app
        else:
            return self.app

    def create_customers_table(self):
        create_table_command = """CREATE TABLE IF NOT EXISTS customers(
            id VARCHAR(50) PRIMARY KEY,
            first_name VARCHAR(25) NOT NULL,
            last_name VARCHAR(25) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20) UNIQUE NOT NULL,
            location VARCHAR(50) NOT NULL,
            password VARCHAR(256) NOT NULL,
            registered_on VARCHAR(50));"""
        self.cursor.execute(create_table_command)

    def create_categories_table(self):
        create_table_command = """CREATE TABLE IF NOT EXISTS categories(
            id VARCHAR(50) PRIMARY KEY,
            category_id VARCHAR(50) REFERENCES categories(id),
            name VARCHAR(50) NOT NULL);"""
        self.cursor.execute(create_table_command)

    def create_groceries_table(self):
        create_table_command = """CREATE TABLE IF NOT EXISTS groceries(
            id VARCHAR(50) PRIMARY KEY,
            category_id VARCHAR(50) REFERENCES categories(id),
            name VARCHAR NOT NULL,
            price INTEGER,
            quantity INTEGER,
            created_on VARCHAR(50));"""
        self.cursor.execute(create_table_command)

    def create_admin_table(self):
        create_table_command = """CREATE TABLE IF NOT EXISTS admin(
            id VARCHAR(50) PRIMARY KEY,
            first_name VARCHAR(25) NOT NULL,
            last_name VARCHAR(25) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20) UNIQUE NOT NULL,
            password VARCHAR(256) NOT NULL,
            registered_on VARCHAR(50));"""
        self.cursor.execute(create_table_command)

    def create_default_admin(self):
        print("CREATING DEFAULT ADMIN")

        query = "SELECT * FROM admin WHERE email=%s"
        self.cursor.execute(query, ('isaacwangethi30@gmal.com',))
        admin = self.cursor.fetchone()

        if not admin:

            print("IF ADMIN NOT EXISTS")

            create_default_admin_query = """INSERT INTO admin
            (id, first_name, last_name, email, phone, password, registered_on)
            VALUES(
            '{}','isaac','wangethi','isaacwangethi30@gmal.com',
            '0706874327','{}','{}')
            """.format(uuid.uuid4(), sha256.hash("F31+25e9"), datetime.now())
            self.cursor.execute(create_default_admin_query)

    def drop_tables(self):
        drop_users_command = "DROP TABLE IF EXISTS customers CASCADE;"
        self.cursor.execute(drop_users_command)

        drop_categories_command = "DROP TABLE IF EXISTS categories CASCADE;"
        self.cursor.execute(drop_categories_command)

        drop_groceries_command = "DROP TABLE IF EXISTS groceries CASCADE;"
        self.cursor.execute(drop_groceries_command)

        drop_admin_command = "DROP TABLE IF EXISTS admin CASCADE;"
        self.cursor.execute(drop_admin_command)
