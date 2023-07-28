# intern-information-to-notion
Collect information about job openings from job boards and integrate all the data into Notion. The type of openings can be selected before inserting into Notion based on personal preference. This way, users can browse those openings everywhere and at all times through Notion APP.

## how it works
1. collect data(intern_data.py)  
Use Selenium WebDriver to scrape data from job boards,104 and CakeResume. Excluding some openings that are not the job you are searching for.
2. insert data into Notion Database(data_to_notion.py)  
Insert data to Notion through Notion API. 

## Notion API
To connect to the Notion. You will need to [get API Key and database ID](https://developers.notion.com/docs/create-a-notion-integration) first.
Then you can use API Key, database ID, URL(send all API requests) ,and requests module to send all the data into Notion database.