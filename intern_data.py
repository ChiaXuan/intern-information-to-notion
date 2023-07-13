import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

dicts=[]
intern_info={}



driver = webdriver.Chrome("C:/Users/88691/Downloads/chromedriver_win32/chromedriver.exe")

driver.get("https://www.104.com.tw/jobs/search/?ro=2&jobcat=2007001000%2C2007002000&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=12&asc=0&page=1&mode=s&jobsource=student2020&langFlag=0&langStatus=0&recommendJob=1&hotJob=1")

driver.implicitly_wait(10)

search = driver.find_element(By.ID,"keyword")
search.send_keys('intern 實習生')   #search "intern 實習生"

button = driver.find_element(By.CLASS_NAME,"gtm-main-search") #click the search button
button.click()


#取得總頁數
def total_page():
    class_element = driver.find_element(By.CLASS_NAME,"gtm-paging-top")
    option_elements = class_element.find_elements(By.CSS_SELECTOR,"option")

    for option_element in option_elements:
        pages = option_element.get_attribute("value")
    return int(pages)

# Check if the given date is within 14 days from today
def within_14_days(date):
    today = datetime.date.today()
    range_start = today - datetime.timedelta(days=14)

    return range_start <= date <= today    # Check if the given date is within the range


def main():
    for x in range (1,2):        #n pages in total, need to scroll for n-1 time(s) (no need for first page)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")  #滾動卷軸
        time.sleep(3)

    dates = driver.find_elements(By.CLASS_NAME,"b-tit__date")
    dates_processed = dates[3:]


    titles = driver.find_elements(By.CLASS_NAME,"js-job-link")

    salaries = driver.find_elements(By.CLASS_NAME,"b-tag--default")
    salaries_processed = []
    for i in salaries:
        if '元' in i.text or '待遇' in i.text:
            salaries_processed.append(i.text)

    companies = driver.find_elements(By.CSS_SELECTOR,".b-list-inline a")  #all a tags in class named b-list-inline

    places = driver.find_elements(By.CSS_SELECTOR,".job-list-intro li:first-child")  ## Find the first "li" element within the specified class
    places_processed = places[3:]


    hrefs = driver.find_elements(By.CLASS_NAME,"js-job-link")



    for i in range(len(titles)):
        if(dates_processed[i].text!=""):
            date_object = datetime.datetime.strptime(dates_processed[i].text, "%m/%d")   #the date format of 104 is m/d
                
            if(datetime.datetime.now().month<date_object.month):    #if the month now is smaller than the updated month of the job on 104, it means the job is updated last year
                date_object = date_object.replace(year=datetime.datetime.now().year-1)
            else:  
                date_object = date_object.replace(year=datetime.datetime.now().year)
            date_only = date_object.date() 
        

            if (within_14_days(date_only)) and ('實習' in titles[i].text or 'intern' in titles[i].text) and ('論件計酬' not in salaries_processed[i]) and ('資安' not in titles[i].text):
            
                intern_info = {'date':date_only,                       #last updated date 
                                'title':titles[i].text,                #title
                                'salary':salaries_processed[i],        #salary
                                'company':companies[i].text,           #company name
                                'place':places_processed[i].text,      #place
                                'url':hrefs[i].get_attribute("href")}  #detail url
            
                
                dicts.append(intern_info)



    driver.quit()
    return dicts

if __name__ == '__main__': #如果以主程式執行
    main()

'''

    #intern_info['title'] = titles[i].text   #職稱
  
    if '元' in salaries_processed[i].text:
        intern_info['salary'] = salaries_processed[i].text   #薪水
    if "待遇" in salaries_processed[i].text:
        intern_info['salary'] = salaries_processed[i].text   #待遇面議

    intern_info['company'] = companies[i].text   #公司名
    
    #intern_info['place'] = places_processed[i].text   #地點
    #intern_info['url'] = hrefs[i].get_attribute("href") #網址
    
    
    #print(dicts)


#print(dicts)
#data.to_excel('sample_data.xlsx', sheet_name='sheet1', index=False)  #export data to excel
'''