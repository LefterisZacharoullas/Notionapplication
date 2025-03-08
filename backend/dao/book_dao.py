import os
import sqlite3
from models.user import Book


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


    def show_all(self) -> list[tuple[Book]]:
        """Display all records from a given table"""

        with self._conn as conn:
            c = conn.cursor()
            c.execute(f"""SELECT * FROM books""")
            items = c.fetchall()
            return items 
    

    def create_record_books(self, book: Book) -> None:
        """Insert new Book records."""
        data = (book.book_name, book.author_name, book.page_number)
    
        with self._conn as conn:
            c = conn.cursor()
            c.execute("INSERT INTO books VALUES (?,?,?)" , data )
            self._conn.commit()

    
    def delete_record_books(self , book_name: str) -> None:
        """Delete an exercise record by name."""
        
        with self._conn as conn:
            c = conn.cursor()
            c.execute("DELETE FROM books WHERE book_name = ? " , (book_name, ))
            self._conn.commit()


    def update_books(self , book: Book) -> None:
        
        with self._conn as conn:
            c = conn.cursor()
            c.execute("UPDATE books SET page_number = ? WHERE book_name = ?" , (book.page_number, book.book_name))
            self._conn.commit()