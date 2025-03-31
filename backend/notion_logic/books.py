import os
from datetime import datetime 
from dotenv import load_dotenv
from .NotionAPI import NotionAPI  

load_dotenv()

NOTION_TOKEN = os.environ.get("NOTION_API")
DATABASE_ID = os.environ.get("DATABASE_ID_BOOKS")
BASE_URL = "http://127.0.0.1:8000"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def add_notion_book_page(book_name: str, author: str, page_number: int, ):

    conn = NotionAPI(DATABASE_ID, headers=  headers)
    published_data = datetime.now().strftime('%Y-%m-%d')

    data = {
        "Name" : {"title" : [{"text" : {"content" : book_name}}]},
        "Author" : {"rich_text" : [{"text" : {"content" : author}}]},
        "Page" : {"number" : page_number},
        "Publication Date": {"date": {"start": published_data, "end": None}}
    }
    
    conn.createPage(data= data)   

if __name__ == "__main__":
    pass