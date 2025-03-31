import requests
import os
import json

class NotionAPI:
    def __init__(self , databaseID: str , headers: dict):
        self.db_id = databaseID
        self.head = headers

    # Response a Database
    def responseDatabase(self) -> None:
        """Displays The status code between notion and user also createing a file with representation"""
        readUrl=f"https://api.notion.com/v1/databases/{self.db_id}/query"
        res=requests.post(readUrl, headers=self.head)
        data = res.json()
        dir_path = os.path.dirname(os.path.abspath(__file__)) 
        
        with open(f"{dir_path}/db.json" , "w", encoding= "utf8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        if res.status_code != 200:
            raise Exception(f"Failed to fetch data: {res.status_code} - {res.text}")
        else:
            print("Response accessed successfully")
        
    # Create a Page
    def createPage(self, data: dict):
        createUrl = 'https://api.notion.com/v1/pages'

        newPageData = { "parent": { "database_id": self.db_id }, "properties": data }
    
        res = requests.post(createUrl, headers= self.head, json=newPageData)
        if res.status_code != 200:
            raise Exception(f"Error when creating database record {res.status_code} - {res.text}")

    # Update_page
    def update_page(self, page_id , data: dict):
        url = f"https://api.notion.com/v1/pages/{page_id}"
    
        payload = {"properties" : data}

        res = requests.patch(url , json=payload , headers=self.head)
        if res.status_code != 200:
            raise Exception(f"Error when updating database record {res.status_code} - {res.text}")
        