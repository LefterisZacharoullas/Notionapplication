import sqlite3
from models.user import UserInDB
import os

class user_dao():

    def __init__(self, db_name = "database.db"):
        if not os.path.exists(db_name):
            raise TimeoutError(f"The database with name {db_name} not exist")

        self._conn = sqlite3.Connection(db_name)

    def show_all(self):
        """Display all records from the users table"""

        with self._conn as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users")
            items = c.fetchall
            return items
        
    def register_user_data(self, user_data: UserInDB):
        """Adding the user data to the table users"""
        data = user_data.model_dump()
        user_data_values = tuple(data.values())

        with self._conn as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (username, full_name, email, disabled, hash_password) Values(?, ?, ?, ?, ?)", user_data_values)
            conn.commit()