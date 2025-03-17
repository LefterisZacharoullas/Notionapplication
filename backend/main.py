from fastapi import FastAPI, Depends, HTTPException, status
from controllers.exercises_controller import router as exercises_router
from controllers.book_controller import router as books_router
from controllers.user_registration import router as registration_router
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from auth.auth_handler import authenticate_user, create_access_token, get_current_active_user
from models.user import User, Token
from datetime import timedelta

app = FastAPI()

@app.get("/")
def welcome():
    return {
        "Welcome": "Welcome to Notion Script",
        "/exercise": "Will give you all the information of exercises",
        "/book": "Will give you all the information of books"
    }

@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()] ) -> Token:
    # This working fine. I get the password and username correctly
    user = authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes = 30)

    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)],):
    return current_user

app.include_router(exercises_router)
app.include_router(books_router)
app.include_router(registration_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
