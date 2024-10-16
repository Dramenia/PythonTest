import time
import uuid
from psycopg2 import sql


class SQLQueries():
    @staticmethod
    def get_table_by_name(table_name: str, cursor):
        try:
            cursor.execute(sql.SQL("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                );
            """), [table_name])
            result = cursor.fetchone()
            return result
        except Exception as e:
            print(f"Could not get table {table_name}. Reason: {e}")
    
    @staticmethod
    def create_table(table_name, cursor, conn):
        try:
            cursor.execute(sql.SQL(f"""
                    CREATE TABLE {table_name} (
                        value REAL,
                        timestamp TIMESTAMP
                    );
                """))
            conn.commit()
        except Exception as e:
            print(f"Could not create table {table_name}. Reason: {e}")
            
    @staticmethod
    def insert_value(table_name, cursor, conn, value):
        try:
            id = uuid.uuid4()
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            query = sql.SQL("""
                INSERT INTO {table} (id, value, created_at)
                VALUES (%s, %s, %s)
            """).format(table=sql.Identifier(table_name))
            cursor.execute(query, (str(id), value[0], timestamp))
            conn.commit()
        except Exception as e:
            print(f"Could not insert value {value} into table {table_name}. Reason: {e}")
