from fastapi import APIRouter
from models.user import Exercise
from dao.exercises_dao import exercise_db
from typing import Any

router = APIRouter()

@router.put('/exercise/')
async def set_exercise(exr: Exercise) -> dict[str, int]:
    db = exercise_db()
    data = db.show_all()

    existing_ex = next((item for item in data if item[0] == exr.exercise_name) , None)
    if not existing_ex:
        db.create_record_exercises(exr) 
    else:
        db.update_exercise(exr)

    return {"exercise_name" : exr.exercise_name , "weight" : exr.weight}

@router.get('/exercise/')
async def get_exercise() -> list[dict]:
    db = exercise_db()
    #Converting the list of tuples to list of dictionaris
    data: list[dict] = [{"exercise_name" : item[0] , "weight" : item[1]} for item in db.show_all()]
    return data

@router.delete('/exercise/{exercise_name}')
async def delete_exercise(exercise_name: str) -> dict[str, bool]:
    db = exercise_db()
    data: list[tuple[Any]] = db.show_all()
    for items in data:
        if exercise_name in items[0]:
            db.delete_record_exercises(exercise_name)
            return {"Success" : True}
    return {"exercise_doesn't_exist" : False}