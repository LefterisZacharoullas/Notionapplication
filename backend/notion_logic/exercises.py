import os
from datetime import datetime 
from dotenv import load_dotenv
from .NotionAPI import NotionAPI  

load_dotenv()

NOTION_TOKEN = os.environ.get("NOTION_API")
DATABASE_ID_EXR = os.environ.get("DATABASE_ID_EXERCISES")
BASE_URL = "http://127.0.0.1:8000"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def add_notion_exercise_page(exercise_name: str, weight: float | int ):

    conn = NotionAPI(DATABASE_ID_EXR, headers=  headers)
    published_data = datetime.now().strftime('%Y-%m-%d')

    data = {
        "Name" : {"title" : [{"text" : {"content" : exercise_name}}]},
        "Number" : {"number" : weight},
        "Workout-Date": {"date": {"start": published_data, "end": None}}
    }
    
    conn.createPage(data= data)   