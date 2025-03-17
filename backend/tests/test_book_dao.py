from controllers.book_controller import book_dao
from models.data import Book
import sqlite3
import pytest
from typing import Generator, Any
import os

@pytest.fixture
def setub_db() -> Generator[Any, Any, Any] :
    """Setup a temporary test database"""

    db_file: str = 'test_db.db' 

    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("CREATE TABLE books (book_name TEXT, author TEXT, page_number INTEGER)")
    conn.commit()
    conn.close()

    yield db_file #return the database name

    os.remove(db_file)

def test_show_all(setub_db: str) -> None:
    conn = sqlite3.connect(setub_db)
    c = conn.cursor()
    c.execute("INSERT INTO books (book_name, author, page_number) VALUES (?, ?, ?)", ("Think and grow rich" , "Napoleon hill" , 10) )
    conn.commit()
    conn.close

    db = book_dao(setub_db)
    data = db.show_all()
    assert ("Think and grow rich" , "Napoleon hill" , 10) in data

def test_create_record_books(setub_db):
    book = Book(book_name="string" , author_name="test" , page_number=123)
    db = book_dao(setub_db) 

    db.create_record_books(book)
    data = db.show_all()

    assert (book.book_name, book.author_name, book.page_number) in data

def test_delete_record_books(setub_db):

    conn = sqlite3.connect(setub_db)
    c = conn.cursor()
    c.execute("INSERT INTO books (book_name, author, page_number) VALUES (?, ?, ?)", ("Think and grow rich" , "Napoleon hill" , 10) )
    conn.commit()
    conn.close()

    db = book_dao(setub_db)
    db.delete_record_books("Think and grow rich")
    data = db.show_all()

    assert not data

def test_updata_books(setub_db):
    conn = sqlite3.connect(setub_db)
    c = conn.cursor()
    c.execute("INSERT INTO books (book_name, author, page_number) VALUES (?, ?, ?)", ("Think and grow rich" , "Napoleon hill" , 10) )
    conn.commit()
    conn.close

    db = book_dao(setub_db)
    book = Book(book_name="Think and grow rich" , author_name="Napoleon hill" , page_number= 10)
    db.update_books(book)
    data = db.show_all()
    
    assert (book.book_name, book.author_name, book.page_number) in data