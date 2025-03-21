from models.data import Book
from fastapi import APIRouter, HTTPException, Path
from dao.book_dao import book_dao

from fastapi import Depends
from typing import Annotated
from models.user import User
from auth.auth_handler import get_current_active_user

router = APIRouter() 

@router.put('/book/')
async def set_book_name(book: Book, current_user: Annotated[User, Depends(get_current_active_user)],):
    db = book_dao()
    data = db.show_all(current_user.username)

    existing_book = False

    for items_dict in data:
        if book.book_name in items_dict.values():
            existing_book = True
        
    if not existing_book:
        db.create_record_books(current_user.username, book)
    else:
        db.update_books(book, current_user.username)

    return {"book_data" : book}

@router.get('/book/')
async def get_book_name(current_user: Annotated[User, Depends(get_current_active_user)]):
    db = book_dao()
    data = db.show_all(current_user.username)
    return {"book_data" : data}

@router.delete('/book/{book_name}')
async def delete_book(book_name: str, current_user: Annotated[User, Depends(get_current_active_user)] ):
    db = book_dao()
    data = db.show_all(current_user.username)
    founded = False 
    for items_dict in data:
        if book_name in items_dict.values():                
            founded = True
            db.delete_record_books(book_name , current_user.username)
            return {"Success" : True}
    
    if not founded:
        raise HTTPException(404, detail= "The books dont exits")