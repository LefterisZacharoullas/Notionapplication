# Главный файл API
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
import database

app = FastAPI()

class Book(BaseModel):
    book_name: str
    author_name: str
    page_number: int 

class Exercise(BaseModel):
    exercise_name: str
    weight: Union[float , int] #Can be float or int

@app.get('/')
async def welcome():
    return {"Hello" : "Welcome to nostion API"}

@app.put('/book/')
async def set_book_name(book: Book):
    database.create_record_books((book.book_name, book.author_name, book.page_number))
    # Always better to return json
    return {"book_name": book.book_name, "author_name": book.author_name, "page_number": book.page_number} 


@app.get('/book/')
async def get_book_name():
    data = [{"book_name" : item[0] , "author_name" : item[1] , "page_number" : item[2]} for item in database.show_all("books")]
    return data


@app.put('/exercise/')
async def set_exercise(exr: Exercise):
    database.create_record_exercises((exr.exercise_name , exr.weight)) 
    return {"exercise_name" : exr.exercise_name , "weight" : exr.weight}

@app.get('/exercise/')
async def get_exercise():
    #Converting the list of tuples to list of dictionaris
    data = [{"exercise_name" : item[0] , "weight" : item[1]} for item in database.show_all("exercises")]
    return data