# intern-information-to-notion
取得104與CakeResume這兩個求職網站的軟體類實習職缺的基本資料，依照個人偏好調整要蒐集的職缺類型，再利用Notion API將所有資料傳送至Notion資料庫中。將兩個求職網站上的職缺整合在一個平台上，如此一來便可以利用APP隨時隨地瀏覽，看到有興趣的職缺也可以利用網址直接了解職缺的詳細資訊與要求。

## how it works
1. collect data(intern_data.py)
Use Selenium WebDriver to scrape data from job boards,104 and CakeResume. Excluding some openings that are not the job you are searching for.
2. insert data into Notion Database
Insert data to Notion through Notion API. 

## Notion API
To connect to the Notion. You will need to [get API Key and database ID](https://developers.notion.com/docs/create-a-notion-integration) first.
Then you can use API Key, database ID, URL(send all API requests) ,and requests module to send all the data into Notion database.