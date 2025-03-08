from pydantic import BaseModel
from typing import Union

class Book(BaseModel):
    book_name: str
    author_name: str
    page_number: int 

class Exercise(BaseModel):
    exercise_name: str
    weight: Union[float , int] #Can be float or int