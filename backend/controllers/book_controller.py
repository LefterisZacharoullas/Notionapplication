from models.data import Book
from fastapi import APIRouter, HTTPException, Path
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

    return {"book_data" : book}

@router.get('/book/')
async def get_book_name():
    db = book_dao()
    data = [{"book_name" : item[0] , "author_name" : item[1] , "page_number" : item[2]} for item in db.show_all()]

    return {"book_data" : data}

@router.delete('/book/{book_name}')
async def delete_book(book_name: str = Path(description= "Input the name of the book you want to delete")):
    db = book_dao()
    data = db.show_all()
    for items in data:
        if book_name in items:
            db.delete_record_books(book_name)
            return {"Success" : True}
    raise HTTPException(status_code= 404 , detail="book_name doesen't exits")