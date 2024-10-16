import psycopg2
import os

from dotenv import load_dotenv
from psycopg2 import Error

from services.sql_queries import SQLQueries

load_dotenv()

class PostgresService:
    def __init__(
        self,
        table_name: str,
    ):
        self.db_name = os.environ.get("DATABASE_NAME")
        self.db_user = os.environ.get("DATABASE_USER")
        self.db_password = os.environ.get("DATABASE_PASSWORD")
        self.db_host = os.getenv('DATABASE_HOST', 'postgres')
        self.db_port = os.getenv('DATABASE_PORT', '5432')
        self.table_name = table_name
        self.conn = None
        self.table_name = table_name
        print(self.db_port)
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=int(self.db_port),
            )
            self.cursor = self.conn.cursor()
            print(f"Connected to database {self.db_name}.")
        except Error as e:
            print(f"Error connecting to PostgreSQL database: {e}")
        self.get_table_or_create()

    def is_table_created(self):
        result = SQLQueries.get_table_by_name(table_name=self.table_name, cursor=self.cursor)
        if result[0]:
            return True
        return False
 
    def create_table(self):
        SQLQueries.create_table(table_name=self.table_name, cursor=self.cursor, conn=self.conn)
        print(f"Table '{self.table_name}' created successfully.")            

    def get_table_or_create(self):
        if not self.is_table_created():
            self.create_table()

    def insert_data(self, value):
        SQLQueries.insert_value(
            table_name=self.table_name,
            cursor=self.cursor,
            conn=self.conn,
            value=value,
        )
        print(f"Inserted value {value} into table '{self.table_name}'.")

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
