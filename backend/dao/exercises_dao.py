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


    def show_all(self) -> list[tuple[Exercise]]:
        """Display all records from the exercise table"""

        with self._conn as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM exercises")
            items = c.fetchall()
            return items 


    def create_record_exercises(self, exr: Exercise) -> None:
        """Insert new exercise records."""
        data = (exr.exercise_name, exr.weight)
    
        with self._conn as conn:
            c = conn.cursor()
            c.execute("INSERT INTO exercises VALUES (?,?)" , data )
            self._conn.commit()
    

    def delete_record_exercises(self , exercise_name: str) -> None:
        """Delete an exercise record by name."""
        
        with self._conn as conn:
            c = conn.cursor()
            c.execute("DELETE FROM exercises WHERE exercise = ? " , (exercise_name, ))
            self._conn.commit()


    def update_exercise(self , exr: Exercise) -> None:
        """Update existing exercise. """
        with self._conn as conn:
            c = conn.cursor()
            c.execute("UPDATE exercises SET weight = ? WHERE exercise = ?" , (exr.weight, exr.exercise_name))
            self._conn.commit()