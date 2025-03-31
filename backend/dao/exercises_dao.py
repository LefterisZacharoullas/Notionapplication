import os
import sqlite3
from models.data import Exercise

class exercise_db():
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
        """Display all records from the exercise table"""

        with self._conn as conn:
            conn.row_factory = lambda cursor, row: {col[0]: row[i] for i, col in enumerate(cursor.description)}
            c = conn.cursor()
            c.execute("SELECT * FROM exercises WHERE username = ?", (username, ))

            for items in c: 
                yield items

    def create_record_exercises(self, exr: Exercise, username: str) -> None:
        """Insert new exercise records."""
        data = []
        data.append(username)

        for items in exr.model_dump().values():
            data.append(items)

      
        with self._conn as conn:
            c = conn.cursor()
            c.execute("INSERT INTO exercises VALUES (?,?,?)" ,tuple(data))
            self._conn.commit()
    

    def delete_record_exercises(self , exercise_name: str, username: str) -> None:
        """Delete an exercise record by name."""
        
        with self._conn as conn:
            c = conn.cursor()
            c.execute("DELETE FROM exercises WHERE exercise = ? and username = ? " , (exercise_name, username ))
            self._conn.commit()


    def update_exercise(self , exr: Exercise, username: str) -> None:
        """Update existing exercise. """
        
        with self._conn as conn:
            c = conn.cursor()
            c.execute("UPDATE exercises SET weight = ? WHERE exercise = ? and username =?" , (exr.weight, exr.exercise_name, username))
            self._conn.commit()