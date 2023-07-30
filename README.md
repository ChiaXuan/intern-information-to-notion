# intern-information-to-notion
Collect information about job openings from job boards and integrate all the data into Notion. Users can select the type of openings based on their personal preferences before inserting them into Notion. This way, users can browse those openings anytime and anywhere through the Notion app.

## how it works
### collect data(intern_data.py)  
Use Selenium WebDriver to scrape data from job boards, like 104 and CakeResume. Exclude some openings that do not match the job you are searching for.
### insert data into the Notion database(data_to_notion.py)  
Insert data to Notion through Notion API. 

## Notion API
To connect to Notion, you will need to [obtain an API Key and database ID](https://developers.notion.com/docs/create-a-notion-integration) first.
Once you have these, you can use the API Key, database ID, URL(to send all API requests) ,and requests module to send data to the Notion database.
### personal data
1. API Key  
2. database ID  
3. Notion-Version  