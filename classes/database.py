from os import getcwd, getenv
from os.path import join
from psycopg2 import connect
from dotenv import load_dotenv
from utils.sql_requests import *

dotenv_path = join(getcwd(), '.env')
load_dotenv(dotenv_path)

user = getenv('DB_USER')
password = getenv('DB_PASSWORD')
host = getenv('DB_HOST')
database = getenv('DATABASE')
port = getenv('DB_PORT')


class UsersDatabase():
    def __init__(self):
        self.__conn = connect(user=user,
                              password=password,
                              host=host,
                              database=database,
                              port=port)

    def create_tables(self):
        with self.__conn.cursor() as cur:
            cur.execute(DROP_USERS_TABLE)
            cur.execute(DROP_PHONES_TABLE)
            cur.execute(CREATE_USERS_TABLE)
            cur.execute(CREATE_PHONES_TABLE)
            self.__conn.commit()

    def add_user(self,
                 first_name: str,
                 last_name: str,
                 email: str,
                 phone: None | str = None):
        with self.__conn.cursor() as cur:
            cur.execute(INSERT_USERS_TABLE, (first_name, last_name, email))
            if phone:
                fetch_data = cur.fetchone()
                if fetch_data:
                    self.add_phone(phone, fetch_data[0])
        self.__conn.commit()

    def delete_user(self, user_id: int):
        with self.__conn.cursor() as cur:
            cur.execute(DELETE_USER_USERS, {'id': user_id})
        self.__conn.commit()

    def add_phone(self, phone: str, user_id: int):
        with self.__conn.cursor() as cur:
            cur.execute(INSERT_PHONES_TABLE, (phone, user_id))
        self.__conn.commit()

    def delete_phone(self, phone: str):
        with self.__conn.cursor() as cur:
            cur.execute(DELETE_PHONE_PHONES, (phone,))
        self.__conn.commit()

    def change_user(self,
                    user_id: int,
                    first_name: str | None = None,
                    last_name: str | None = None,
                    email: str | None = None,
                    phone: str | None = None):
        base_columns = {
            'first_name': {'data': first_name, 'request': UPDATE_FIRST_NAME_USERS},
            'last_name': {'data': last_name, 'request': UPDATE_LAST_NAME_USERS},
            'email': {'data': email, 'request': UPDATE_EMAIL_USERS}
        }
        for column in base_columns.values():
            if column['data']:
                with self.__conn.cursor() as cur:
                    cur.execute(column['request'], (column['data'], user_id))
        if phone:
            self.add_phone(phone, user_id)
        self.__conn.commit()

    def find_user(self,
                  first_name: str | None = None,
                  last_name: str | None = None,
                  email: str | None = None,
                  phone: str | None = None) -> list | None:
        base_colums = {
            'first_name': {'data': first_name, 'request': SELECT_USER_BY_FIRST_NAME},
            'last_name': {'data': last_name, 'request': SELECT_USER_BY_LAST_NAME},
            'email': {'data': email, 'request': SELECT_USER_BY_EMAIL},
            'phone': {'data': phone, 'request': SELECT_USER_BY_PHONE}
        }
        for column in base_colums.values():
            if column['data']:
                with self.__conn.cursor() as cur:
                    cur.execute(column['request'], (column['data'],))
                    data = cur.fetchall()
                    if len(data):
                        return data
        return None

    def close(self):
        self.__conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.close()
        return False
