from datetime import datetime , timezone
from dotenv import load_dotenv
import os
from NotionApi import NotionAPI

load_dotenv() # Load environment variables from .env file

def manage_book() -> str:
    filename = "current_book.txt"

    try:
        # Check if the file exists and read the book name
        with open(filename, "r") as file:
            book = file.read().strip() #just removes the whitespace 
        print(f"The current book is: {book}")
        still_reading = input("Are you still reading this book? (yes/no): ").strip().lower()

        if still_reading != "yes":
            new_book = input("Enter the name of the new book: ").strip()
            with open(filename, "w") as file:
                file.write(new_book)
            print(f"The new book '{new_book}' has been saved.")
            return new_book
        else:
            print("Continue enjoying your book!")
            return book
    except FileNotFoundError:
        # If the file doesn't exist, create it
        new_book = input("No book found. Enter the name of the book you are reading: ").strip()
        with open(filename, "w") as file:
            file.write(new_book)
        print(f"The book '{new_book}' has been saved.")
        return new_book

def reading_book(headers):
    Reading_database_id = os.getenv("READING_DATABASE_ID")
    bookreading = NotionAPI(Reading_database_id, headers)
    bookreading.responseDatabase()
    book_name = manage_book()
    while True:
        try:
            page_number = int(input("Enter the page number you finished reading: "))
            break
        except ValueError:
            print("You entered the wrong data. Please enter a number.")
    page_number = f"Молодец! Ты прочитал до {page_number} страницы."
    print(page_number)

    published_data = datetime.now().astimezone(timezone.utc).isoformat()

    data = {
        "Name of the Book": {"title": [{"text": {"content": book_name}}]},
        "Pages": {"rich_text": [{"text": {"content": page_number}}]},
        "Published": {"date": {"start": published_data, "end": None}}
    }

    bookreading.createPage(data)

def exercising(headers):
    gym_database_id = os.getenv("GYM_DATABASE_ID")
    gymexercise = NotionAPI(gym_database_id, headers)
    gymexercise.responseDatabase()
    exercises = ["push-ups" , "pull-ups" , "incline press", "lat pulldown" 
                , "butterfly" , "low row" , "triceps" , "biceps", "legs1" 
                , "legs2" , "legs3"]

    def get_motivation(value: float) -> str:
        motivational_phrases = {
            58: "Ты молодец!",
            60: "Продолжай в том же духе!",
            65: "Просто великолепно, так держать!",
            70: "Ты неостановим, вперед к цели!",
            75: "Сила и мощь, гордимся!",
            80: "Ты достигаешь великих вещей, не сдавайся!",
        }

        for key in motivational_phrases.keys():
            if value <= key:
                return f"{value}kg {motivational_phrases[key]}"
        else:
            last_value = list(motivational_phrases.values())[-1]
            return f"{value}kg {last_value}"    

    
    published_data = datetime.now().astimezone(timezone.utc).isoformat()

    for exercise in exercises:
        achive = input(f"Enter the weight in kilograms or the number of repetitions for the {exercise}: ")
        data = {
        "Exercise": {"title": [{"text": {"content": exercise.capitalize()}}]},
        "Kg": {"rich_text": [{"text": {"content": get_motivation(float(achive))}}]},
        "Published": {"date": {"start": published_data, "end": None}}
        }
        gymexercise.createPage(data)
    
def main():
    # Читаем переменные
    NOTION_TOKEN = os.getenv("NOTION_TOKEN")
    headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
    }

    if not os.path.exists('.env'):
        raise FileNotFoundError("The .env file is missing.")

    REQUIRED_ENV_VARS = ["NOTION_TOKEN", "READING_DATABASE_ID", "GYM_DATABASE_ID"]
    missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"Отсутствуют необходимые переменные окружения: {', '.join(missing)}")

    while True:
        goal = input("What goal you achive today Reading-1, Exercising-2, STOP-0: ")
        if goal == "1":
            reading_book(headers)
        elif goal == "2":
            exercising(headers)
        elif goal == "0":
            break
        else:
            print("You Enter wrong data please chose 1 or 2 (1-reading, 2-exercising)")
        
if __name__ == "__main__":
    main()