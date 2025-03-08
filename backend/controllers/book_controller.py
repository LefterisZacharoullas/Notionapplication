from models.user import Book
from fastapi import APIRouter

from dao.book_dao import book_dao

router = APIRouter() 

@router.put('/book/')
async def set_book_name(book: Book):
    db = book_dao()
    data = db.show_all()
    
    existing_book = next((item for item in data if item[0] == book.book_name) , None)
    if not existing_book:
        db.create_record_books(book)
    else:
        db.update_books(book)

    return {"book_name": book.book_name, "author_name": book.author_name, "page_number": book.page_number}

@router.get('/book/')
async def get_book_name():
    db = book_dao()
    data = [{"book_name" : item[0] , "author_name" : item[1] , "page_number" : item[2]} for item in db.show_all()]
    return data

@router.delete('/book/{book_name}')
async def delete_book(book_name: str):
    db = book_dao()
    data = db.show_all()
    for items in data:
        if book_name in items[0]:
            db.delete_record_books(book_name)
            return {"Success" : True}
    return {"Book_doesn't_exist" : False}