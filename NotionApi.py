class NotionAPI:
    def __init__(self , databaseID: str , headers: dict):
        self.Reading_database_id = databaseID
        self.head = headers

    # Response a Database
    def responseDatabase(self, databasename: str) -> list:
        readUrl=f"https://api.notion.com/v1/databases/{self.Reading_database_id}/query"
        res=requests.request("POST", readUrl, headers= self.head)
        print(res.status_code)

        data = res.json()
        with open(f"{databasename}.json" , "w", encoding='utf8') as f:
            json.dump(data , f , ensure_ascii=False , indent=4)
        return data["results"]

    # Create a Page
    def createPage(self, data: dict):
        createUrl = 'https://api.notion.com/v1/pages'

        newPageData = { "parent": { "database_id": self.Reading_database_id }, "properties": data }
    
        res = requests.post(createUrl, headers= self.head, json=newPageData)
        print(res.status_code)

    # Update_page
    def update_page(self, page_id , data: dict):
        url = f"https://api.notion.com/v1/pages/{page_id}"
    
        payload = {"properties" : data}

        res = requests.patch(url , json=payload , headers=self.head)
        print(res.status_code)