import os
from database import Database
import sqlite3
import pytest
from typing import Any, Generator

@pytest.fixture
def setub_db() -> Generator[Any, Any, Any] :
    """Setup a temporary test database"""

    db_file: str = 'test_db.db' 

    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("CREATE TABLE exercises (exercise TEXT, weight INTEGER)")
    c.execute("CREATE TABLE books (book_name TEXT, author TEXT, page_number INTEGER)")
    conn.commit()
    conn.close()

    yield db_file #return the database name

    os.remove(db_file)


def test_create_record_exercises(setub_db):
    
    db = Database(setub_db) 
    db.create_record_exercises(('string' , 10))
    data = db.show_all('exercises')
    assert ('string' , 10) in data

def test_delete_record_exercises(setub_db):

    conn = sqlite3.connect(setub_db)
    c = conn.cursor()
    c.execute("INSERT INTO exercises (exercise, weight) VALUES (? , ?)" , ("string" , 1000))
    conn.commit()
    conn.close()

    db = Database(setub_db)
    db.delete_record_exercises("string")
    data = db.show_all("exercises")

    assert not data

def test_create_records_books(setub_db):

    db = Database(setub_db)
    db.create_record_books(("Think and grow rich" , "Napoleon hill" , 10))
    data = db.show_all("books")

    assert ("Think and grow rich" , "Napoleon hill" , 10) in data
    
def test_delete_record_books(setub_db):

    conn = sqlite3.connect(setub_db)
    c = conn.cursor()
    c.execute("INSERT INTO books (book_name, author, page_number) VALUES (?, ?, ?)", ("Think and grow rich" , "Napoleon hill" , 10) )
    conn.commit()
    conn.close()

    db = Database(setub_db)
    db.delete_record_books("Think and grow rich")
    data = db.show_all("books")

    assert not data

def test_create_record_book_invalid_data(setub_db):
    db = Database(setub_db)
    check_list = [("lkaf;dsjf", 1223, "lkdsajf"), (1223 , "Napoleon hill" , 10), ("hello"), (1223 , "Napoleon hill" , 10, 20)]
    for items in check_list:
        with pytest.raises(ValueError):
            db.create_record_books(items)

def test_invalid_record_exercise(setub_db):
    db = Database(setub_db)
    check_list = [("Hello" , "adslfkjl"), ("hello") , (1213 , "hello" , "hello"), (1312, "hello")]
    for items in check_list:
        with pytest.raises(ValueError):
            db.create_record_exercises(items)

def test_update_books(setub_db):
    conn = sqlite3.connect(setub_db)
    c = conn.cursor()
    c.execute("INSERT INTO books (book_name, author, page_number) VALUES (?, ?, ?)", ("Think and grow rich" , "Napoleon hill" , 10) )
    conn.commit()
    conn.close()

    db = Database(setub_db)
    db.update_books("Think and grow rich" , 100)
    data = db.show_all("books")
    assert ("Think and grow rich" , "Napoleon hill" , 100) in data      

def test_updata_exercise(setub_db):
    conn = sqlite3.connect(setub_db)
    c = conn.cursor()
    c.execute("INSERT INTO exercises (exercise, weight) VALUES (?, ?)" , ("push-ups" , 20))
    conn.commit()
    conn.close

    db = Database(setub_db)
    db.update_exercise("push-ups" , 45)
    data = db.show_all("exercises")
    assert ("push-ups" , 45) in data

def test_show_all(setub_db):
    conn = sqlite3.connect(setub_db)
    c = conn.cursor()
    c.execute("INSERT INTO exercises (exercise, weight) VALUES (?, ?)" , ("push-ups" , 20))
    conn.commit()
    conn.close

    db = Database(setub_db)
    data = db.show_all("exercises")
    assert ("push-ups" , 20) in data