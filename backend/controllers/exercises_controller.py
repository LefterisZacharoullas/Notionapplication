from fastapi import APIRouter, HTTPException, Path
from models.data import Exercise
from dao.exercises_dao import exercise_db

router = APIRouter()

@router.put('/exercise/') 
async def set_exercise(exr: Exercise):
    db = exercise_db()
    data = db.show_all()

    existing_ex = next((item for item in data if item[0] == exr.exercise_name) , None)
    if not existing_ex:
        db.create_record_exercises(exr) 
    else:
        db.update_exercise(exr)

    return {"exercise_data" : exr}

@router.get('/exercise/')
async def get_exercise():
    db = exercise_db()
    #Converting the list of tuples to list of dictionaris
    data: list[dict] = [{"exercise_name" : item[0] , "weight" : item[1]} for item in db.show_all()]

    return {"exercise_data" : data}

@router.delete('/exercise/{exercise_name}')
async def delete_exercise(exercise_name: str = Path(description= "Input the name of exercise you want to delete")):
    db = exercise_db()
    data = db.show_all()
    
    for items in data:
        if exercise_name in items:
            db.delete_record_exercises(exercise_name)
            return {"Success" : True}
    else:  
        raise HTTPException(status_code=404 , detail= "exercise_doesn't_exist" )
