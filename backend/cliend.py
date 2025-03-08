import requests

data = {"book_name" : "test" , "author_name" : "test" , "page_number" : 56}
data2 = {"book_name" : "test22" , "author_name" : "test" , "page_number" : 14}

res = requests.put("http://127.0.0.1:8000/book", json=data2)
res = requests.get("http://127.0.0.1:8000/books", json=data)
#res1 = requests.delete("http://127.0.0.1:8000/book/test")
#print(res.json())
# dataex = {"exercise" : "test" , "weight" : 10}
# resexercise = requests.put("http://127.0.0.1:8000/exercise" , json=dataex)
# resget = requests.get("http://127.0.0.1:8000/exercise/")
# print(resget.json())

print(res.json())