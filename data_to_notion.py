import requests
import json
from intern_data import main
from update_data import is_empty,patch_pg,all_data
import secret_data as sd


database_id=sd.Database_id
api_key = sd.notion_api_key

endpoint = "https://api.notion.com/v1/pages" #for insert

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

scraped = main()

#insert data into notion 
def insert_data():
    
    for i in range (len(scraped)):
        data = {
            "parent": {"database_id": database_id},
            "properties": all_data(scraped[i])
        }

        res = requests.post(endpoint, headers=headers, data=json.dumps(data))

        if res.status_code == 200:
            print("Row created successfully!")
            page_id = res.json().get("id")
            print(page_id)
        else:
            print("Failed to create row. Status code:", res.status_code)
            print(res.json())


if not is_empty():      
    print("not empty")
    patch_pg(scraped)
else:
    print("empty")
    insert_data()   #if empty, insert data

