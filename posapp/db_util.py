import os
from flask import current_app
import psycopg2
from pprint import pprint


class DbUtil:
    def __init__(self):
        
        pprint("Initialized")

    def connect(self):
         try:
            self.connection = psycopg2.connect(current_app.config['DATABASE_URL'])
            #self.connection = psycopg2.connect(current_app.config['DATABASE_URL'],sslmode='require')
            return self.connection           
         except:
            pprint("Cannot connect to database")