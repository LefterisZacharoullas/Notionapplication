import os
import sqlite3
from models.data import Book
from typing import Any, Generator

class book_dao():
    def __init__(self, db_name: str = "database.db"):
        if not os.path.exists(db_name):  
            raise TimeoutError("The database is not exitsting")
        
        self._conn = sqlite3.connect(db_name)


    def __del__(self) -> None:
        """Ensures the database connection is closed when the object is deleted."""
        if self._conn:
            self._conn.close()
            self._conn = None  # Prevent accidental reuse


    def show_all(self, username: str):
        """Display all records from a given table"""

        with self._conn as conn:
            conn.row_factory = lambda cursor, row: {col[0]: row[i] for i, col in enumerate(cursor.description)}
            c = conn.cursor()
            c.execute(f"""SELECT * FROM books WHERE username = ?""", (username, ))

            for items in c:
                yield items 
    

    def create_record_books(self, username: str, book: Book) -> None:
        """Insert new Book records."""
        data = []
        data.append(username)

        for item in book.model_dump().values():
            data.append(item)

        with self._conn as conn:
            c = conn.cursor()
            c.execute("INSERT INTO books VALUES (?,?,?,?)" , tuple(data) )
            self._conn.commit()

    
    def delete_record_books(self , book_name: str, username:str) -> None:
        """Delete an exercise record by name."""
        
        with self._conn as conn:
            c = conn.cursor()
            c.execute("DELETE FROM books WHERE book_name = ? AND username = ? " , (book_name, username))
            self._conn.commit()


    def update_books(self , book: Book, username:str) -> None:
        
        with self._conn as conn:
            c = conn.cursor()
            c.execute("UPDATE books SET page_number = ? WHERE book_name = ? and username = ?" , (book.page_number, book.book_name, username))
            self._conn.commit()