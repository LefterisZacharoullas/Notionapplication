from fastapi import APIRouter, HTTPException, status
from models.user import User, UserInDB
from auth.auth_handler import get_user
from dao.user_dao import user_dao
from auth.my_security import get_password_hash

router = APIRouter()

@router.post("/registration")
def create_user(user_data: User, password: str):

    if get_user(user_data.username) is None:
        user_db = user_dao()

        hashed_password = get_password_hash(password)
        data = UserInDB(**user_data.model_dump(), hash_password= hashed_password)

        user_db.register_user_data(data)

        return { "User_successfully_registered": user_data}
    
    else:
        return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. User already exist",
        headers={"WWW-Authenticate": "Bearer"}
        )

        

    

