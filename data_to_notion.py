'''
The purpose of the file is to know whether the notion database is empty.If so, just insert data into it. 
Otherwise,update new pages and delete the rest of existing pages in the notion.
Since each job opening is one page, the first step is to query the parent page of all the pages to get the page id of each page.
Then updating/deleting can be finished by using each page id.
'''

import requests
import json
import secret_data as sd 

database_id = sd.Database_id
api_key = sd.notion_api_key

endpoint = f"https://api.notion.com/v1/databases/{database_id}/query"   #API endpoint for querying the parent page 
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

#, data=json.dumps(payload)
#send the API request with the prepared payload and headers 
response = requests.post(endpoint, headers=headers) 

if response.status_code == 200:
    data = response.json()  #type : dict
    existing_pages = data.get("results", [])

    #check if there are additional pages of data. If returnig true,it means there are more data
    while data.get("has_more", False):
        next_cursor = data.get("next_cursor")  # fetch additional pages
        response = requests.post(endpoint, headers=headers, json={"start_cursor": next_cursor})
        data = response.json()
        existing_pages.extend(data.get("results", []))
    
else:
    print("Failed to retrieve existing pages. Status code:", response.status_code)

#check if the notion database is empty or not
def is_empty():
    if len(existing_pages)==0:      
        return True
    else:
        return False

#return data that was scraped from 104 and CakeResume 
def all_data(sc: dict):
    if sc['date'] == "":  #openings in CakeResume doesn't comtain date information directly 
        #date_str = json.dumps(None)
        #print(date_str)
        dn = {
            "Date": {"date":None},
            "Job Title": {"title": [{"text": {"content": sc['title']}}]},
            "Company": {"rich_text": [{"text": {"content": sc['company']}}]},
            "Place": {"rich_text": [{"text": {"content": sc['place']}}]},
            "Salary": {"rich_text": [{"text": {"content": sc['salary']}}]},
            "URL":{"url": sc['url']}}
    else:
        dn = {
            "Date": {"date": {"start": sc['date'].isoformat(),"end": None}},
            "Job Title": {"title": [{"text": {"content": sc['title']}}]},
            "Company": {"rich_text": [{"text": {"content": sc['company']}}]},
            "Place": {"rich_text": [{"text": {"content": sc['place']}}]},
            "Salary": {"rich_text": [{"text": {"content": sc['salary']}}]},
            "URL":{"url": sc['url']}}
    
    # Check if the 'date' key has a value
    #if sc["date"]:
        # If it has a value, convert it to a proper date format before inserting
        #dn["date"] = 
    #else:
        #dn["Date"] = date_str
    #print(dn)
    return dn

#update page 
def update_page(url: str, new_data: dict):
    payload = {"properties": new_data}

    res = requests.patch(url, json=payload, headers=headers)

    if res.status_code == 200:
        print('Page updated successfully.')
    else:
        print('Failed to update the page.')
        print(res.json())
    


#delete the rest of pages  
def delete_page(url:str):
    payload = {"archived": True}

    res = requests.patch(url, json=payload, headers=headers)

    if res.status_code == 200:
        print('Page deleted successfully.')
    else:
        print('Failed to delete the page.')
        print(res.json())


#insert data into notion 
def insert_data(scraped:list):
    endpoint = "https://api.notion.com/v1/pages" 
    countinsert = 0
    for i in range (len(existing_pages),len(scraped)):
        data = {"parent": {"database_id": database_id},
                "properties": all_data(scraped[i])}
        
        #json.dumps() : Serialize obj to a JSON formatted str 序列化(以位元形式，電腦看得懂的方式)寫入JSON 格式的資料
        res = requests.post(endpoint, headers=headers, data=json.dumps(data)) 

        if res.status_code == 200:
            print("Row created successfully!")
            #page_id = res.json().get("id")
            countinsert+=1
        else:
            print("Failed to create row. Status code:", res.status_code)
            print(res.json())
    print("insert : ",countinsert)


def patch_pg(scraped:list):
    print("ep:",len(existing_pages))
    print("scr:",len(scraped))

    count_update=0
    count_delete =0

    #iterate each page id and update/delete it
    for i in range (len(existing_pages)):
        page_id = existing_pages[i].get("id")  #id of each child page
        url = f"https://api.notion.com/v1/pages/{page_id}"
        
        if(i<len(scraped)):
            new_data = all_data(scraped[i])
            update_page(url,new_data)  
            count_update+=1
        else:
            delete_page(url)
            count_delete+=1
    
    if(len(scraped)>len(existing_pages)):
        insert_data(scraped)


    print("update : ",count_update)
    print("delete : ",count_delete)    


if __name__ == '__main__':
    patch_pg(existing_pages)