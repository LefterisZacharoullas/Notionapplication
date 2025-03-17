from controllers.exercises_controller import exercise_db
from models.data import Exercise
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
    c.execute("CREATE TABLE exercises (exercise TEXT, weight INTEGER)")
    conn.commit()
    conn.close()

    yield db_file #return the database name

    os.remove(db_file)

def test_show_all(setub_db: str) -> None:
    conn = sqlite3.connect(setub_db)
    c = conn.cursor()
    c.execute("INSERT INTO exercises (exercise, weight) VALUES (?, ?)" , ("push-ups" , 20))
    conn.commit()
    conn.close

    db = exercise_db(setub_db)
    data = db.show_all()
    assert ("push-ups" , 20) in data

def test_create_record_exercises(setub_db):
    exr = Exercise(exercise_name="hello" , weight=124)
    db = exercise_db(setub_db) 

    db.create_record_exercises((exr))
    data = db.show_all()

    assert (exr.exercise_name, exr.weight) in data

def test_delete_record_exercises(setub_db):

    conn = sqlite3.connect(setub_db)
    c = conn.cursor()
    c.execute("INSERT INTO exercises (exercise, weight) VALUES (? , ?)" , ("string" , 1000))
    conn.commit()
    conn.close()

    db = exercise_db(setub_db)
    db.delete_record_exercises("string")
    data = db.show_all()

    assert not data

def test_updata_exercise(setub_db):
    conn = sqlite3.connect(setub_db)
    c = conn.cursor()
    c.execute("INSERT INTO exercises (exercise, weight) VALUES (?, ?)" , ("push-ups" , 20))
    conn.commit()
    conn.close

    db = exercise_db(setub_db)
    exr = Exercise(exercise_name="push-ups" , weight=45)
    db.update_exercise(exr)
    data = db.show_all()
    
    assert ("push-ups" , 45) in data