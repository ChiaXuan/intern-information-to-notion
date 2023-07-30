from intern_data import main
from data_to_notion import is_empty,patch_pg,insert_data
import secret_data as sd


database_id=sd.Database_id
api_key = sd.notion_api_key


scraped = main()

if not is_empty():      
    print("not empty")
    patch_pg(scraped) #if not empty, update data
else:
    print("empty")
    insert_data(scraped)   #if empty, insert data

