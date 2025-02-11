import requests

data = {"book_name" : "test" , "author_name" : "test" , "page_number" : 14}

res = requests.get("http://127.0.0.1:8000/book", json=data)

print(res.json())


