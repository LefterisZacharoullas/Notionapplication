# Работа с базой данных (например, Notion API)
import sqlite3
import os
from typing import Any

def show_all(table_name: str) -> list[tuple[Any, ...]]:
    """Display all records from a given table"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(f'{dir_path}/database.db')
    c = conn.cursor()

    c.execute(f"""SELECT * FROM {table_name}""")

    items = c.fetchall()
    return items

def create_record_exercises(data: tuple[str, int]):
    """Insert new exercise records."""
    if not (isinstance(data, tuple) and isinstance(data[0] , str) and isinstance(data[1], int) and len(data) == 2):
        raise ValueError("Each entry must be a tuple with (str, int). Example: ('Push-ups', 20) ")

    dir_path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(f'{dir_path}/database.db')
    c = conn.cursor()

    c.execute("INSERT INTO exercises VALUES (?,?)" , data )

    conn.commit() # Only for modifying
    conn.close()

def delete_record_exercises(exercise_name: str):
    """Delete an exercise record by name."""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(f'{dir_path}/database.db')
    c = conn.cursor()

    c.execute("DELETE FROM exercises WHERE exercise = ? " , (exercise_name, ))

    conn.commit()
    conn.close()

def delete_record_books(book_name: str):
    """Delete a book record by name."""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(f'{dir_path}/database.db')
    c = conn.cursor()

    c.execute("DELETE FROM books WHERE book_name = ?" , (book_name, ))

    conn.commit()
    conn.close()

def create_record_books(data: tuple[str, str, int]):
    """Insert a new book record into the database.

    Args:
        data (tuple[str, str, int]): A tuple containing:
            - str: The book's name
            - str: The author's name
            - int: The number of pages read

    Raises:
        ValueError: If the input is not a tuple with the correct types.

    Example:
        create_record_books(("Think and Grow Rich", "Napoleon Hill", 25))
    """

    if not (isinstance(data, tuple) and isinstance(data[0], str) and isinstance(data[1], str) and isinstance(data[2], int) and len(data) == 3):
        raise ValueError("Each entry must be a tuple with (str, str, int). Example: [('Think and grow rich' , 'Napoleon Hill' , 25)]")

    dir_path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(f'{dir_path}/database.db')
    c = conn.cursor()

    c.execute("INSERT INTO books VALUES (?,?,?)" , data)

    conn.commit()
    conn.close()

def execute_sql_command(command: str):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(f'{dir_path}/database.db')
    c = conn.cursor()

    c.execute(command)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    #delete_record_exercises("test")
    #delete_record_books("test")
    pass