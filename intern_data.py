import datetime
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

dicts=[]
intern_info={}
companies=[]

driver = webdriver.Chrome("C:/Users/88691/Downloads/chromedriver-win64/chromedriver.exe")

#return total pages of 104
def total_page():
    class_element = driver.find_element(By.CLASS_NAME,"gtm-paging-top")
    option_elements = class_element.find_elements(By.CSS_SELECTOR,"option")

    for option_element in option_elements:
        pages = option_element.get_attribute("value")
    return int(pages)



'''
# Check if the given date is within 14 days from today
def within_14_days(date):
    today = datetime.date.today()
    range_start = today - datetime.timedelta(days=14)

    return range_start <= date <= today    # Check if the given date is within the range
'''

#click next page button in CakeResume
def next_page():
    class_element = driver.find_elements(By.CLASS_NAME,"Pagination_itemNavigation__Cv3M8")
    class_element[1].click()

#find the title name according to the company name
def FindTitle(dicts:dict,company:str):
    for job in dicts:
        if("股份有限公司" in job['company']):
            modi =job['company'].replace("有限公司","").strip() #cake resume
        else:
            modi = job["company"]
        if(modi==company):
            return job["title"]

#check the similarity of two company name        
def jaccard_similarity(word1, word2):
    set1 = set(word1)
    set2 = set(word2)
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    similarity_score = len(intersection) / len(union)
    return similarity_score


def main():
    #scrape data from yourator
    driver.get("https://www.yourator.co/jobs?category[]=%E5%89%8D%E7%AB%AF%E5%B7%A5%E7%A8%8B&category[]=%E5%BE%8C%E7%AB%AF%E5%B7%A5%E7%A8%8B&category[]=%E5%85%A8%E7%AB%AF%E5%B7%A5%E7%A8%8B&category[]=%E8%A1%8C%E5%8B%95%E8%A3%9D%E7%BD%AE%E9%96%8B%E7%99%BC&category[]=%E9%81%8A%E6%88%B2%E9%96%8B%E7%99%BC&category[]=%E6%B8%AC%E8%A9%A6%E5%B7%A5%E7%A8%8B&category[]=DevOps%20%2F%20SRE&category[]=%E8%B3%87%E6%96%99%E5%B7%A5%E7%A8%8B%20%2F%20%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92&category[]=MIS%20%2F%20%E7%B6%B2%E8%B7%AF%E7%AE%A1%E7%90%86&position[]=intern")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    cols = driver.find_elements(By.CLASS_NAME,"flex.overflow-hidden")

    for col in cols:
        
        inline = col.find_elements(By.CLASS_NAME,'flex.shrink')

        t = inline[1].find_element(By.TAG_NAME,"span")
        if "月" not in t.text:
            title = col.find_element(By.CLASS_NAME,'flex-initial.mb-1')
            
            company = col.find_element(By.CLASS_NAME,'flex-initial.text-sub')
            
            # find <a>
            a_element = col.find_element(By.XPATH,"..")
            href = a_element.get_attribute("href")
            
            place = inline[0].find_element(By.TAG_NAME,"span")
            salary = inline[2].find_element(By.TAG_NAME,"span")

            internCake_info = {'date':"",                               #last updated date 
                            'title':title.text.strip(),                 #title
                            'salary':salary.text.strip(),               #salary
                            'company':company.text.strip(),             #company name
                            'place':place.text.strip(),                 #place
                            'url':href}      
            
            if('股份有限公司' in (company.text)): 
                    companies.append(company.text.replace('股份有限公司','').strip()) #to increase similarity
            else:
                    companies.append(company.text.strip())

            dicts.append(internCake_info)
    

    

    #scrape 
    # data in 104
    driver.get("https://www.104.com.tw/jobs/search/?ro=2&jobcat=2007001000%2C2007002000&isnew=14&kwop=7&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=12&asc=0&page=1&mode=s&jobsource=student2020&langFlag=0&langStatus=0&recommendJob=1&hotJob=1")

    driver.implicitly_wait(10)

    search = driver.find_element(By.ID,"keyword")
    search.send_keys('intern 實習生')   #search "intern 實習生"

    button = driver.find_element(By.CLASS_NAME,"gtm-main-search") #click the search button
    button.click()


    for x in range (1,total_page()):        #n pages in total, need to scroll for n-1 time(s) (no need for first page)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")  #scroll the page
        time.sleep(3)

    dates = driver.find_elements(By.CLASS_NAME,"b-tit__date")
    dates_processed = dates[3:]


    titles_104 = driver.find_elements(By.CLASS_NAME,"js-job-link")

    salaries104 = driver.find_elements(By.CLASS_NAME,"b-tag--default")
    salaries104_processed = []
    for i in salaries104:
        if '元' in i.text or '待遇' in i.text:
            salaries104_processed.append(i.text)

    companies104 = driver.find_elements(By.CSS_SELECTOR,".b-list-inline a")  #all 'a' tags in class named b-list-inline

    places104 = driver.find_elements(By.CSS_SELECTOR,".job-list-intro li:first-child")  ## Find the first "li" element within the specified class
    places104_processed = places104[3:]


    hrefs104 = driver.find_elements(By.CLASS_NAME,"js-job-link")
    count104 = 0
    

    for i in range(len(titles_104)):
        if(dates_processed[i].text!=""):
            date_object = datetime.datetime.strptime(dates_processed[i].text, "%m/%d")   #the date format of 104 is m/d
                
            if(datetime.datetime.now().month<date_object.month):    #if the month now is smaller than the updated month of the job on 104, it means the job is updated last year
                date_object = date_object.replace(year=datetime.datetime.now().year-1)
            else:  
                date_object = date_object.replace(year=datetime.datetime.now().year)
            date_only = date_object.date() 
        

            if("股份有限公司" in companies104[i].text):
                com = companies104[i].text.replace("股份有限公司","").strip()
            else:
                com = companies104[i].text.strip() 

            simi = 0
            
            #check the similarity of two companies name, one from 104, the other from CakeResume
            for j in companies:
                if(simi<jaccard_similarity(com,j)):     
                    simi = jaccard_similarity(com,j)
                    name = j

            #the two companie names is similar and the title of these two openings are the same, so these two are regarded as the same opening -> skip this one in 104
            if(simi>0.4 and FindTitle(dicts,name) == titles_104[i].text):   
                print(FindTitle(dicts,name))
                continue
            
            if (('論件計酬' not in salaries104_processed[i]) and ('資安' not in titles_104[i].text) and ('韌體' not in titles_104[i].text)):
            
                intern104_info = {'date':date_only,                       #last updated date 
                                'title':titles_104[i].text,                #title
                                'salary':salaries104_processed[i],        #salary
                                'company':companies104[i].text,           #company name
                                'place':places104_processed[i].text,      #place
                                'url':hrefs104[i].get_attribute("href")}  #detail url
            
                count104+=1
                dicts.append(intern104_info)
                 
    print("count104 : ",count104)     
    driver.quit()
    return dicts

if __name__ == '__main__': #如果以主程式執行
   print(main())