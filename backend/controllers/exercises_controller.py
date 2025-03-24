from fastapi import APIRouter, HTTPException, Path, Depends
from models.data import Exercise
from dao.exercises_dao import exercise_db
from typing import Annotated
from models.user import User
from auth.auth_handler import get_current_active_user

router = APIRouter()

@router.put('/exercise/') 
async def set_exercise(exr: Exercise, current_user: Annotated[User, Depends(get_current_active_user)], ):
    db = exercise_db()
    data = db.show_all(current_user.username)

    Exercise_exeist = False

    for exercise in data:
        if exr.exercise_name in exercise.values():
            Exercise_exeist = True
    
    if Exercise_exeist:
        db.update_exercise(exr, current_user.username)
    else:
        db.create_record_exercises(exr, current_user.username)

    return {"Success" : exr}    
    
@router.get('/exercise/')
async def get_exercise(current_user: Annotated[User, Depends(get_current_active_user)],):
    db = exercise_db()
    data = db.show_all(current_user.username)
    return {"exercise_data" : data}

@router.delete('/exercise/{exercise_name}')
async def delete_exercise(exercise_name: str ,current_user: Annotated[User, Depends(get_current_active_user)] ):
    db = exercise_db()
    data = db.show_all(current_user.username)
    Exercise_exist = False    
    for items in data:
        if exercise_name in items.values():
            Exercise_exist = True
            db.delete_record_exercises(exercise_name, current_user.username)

    if Exercise_exist:
        return {"Success-exercises-deleted" : exercise_name}
    else:
        raise HTTPException(status_code= 404 , detail= f"The exercises {exercise_name} doesn't exist")