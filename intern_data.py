import datetime
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

dicts=[]
intern_info={}

driver = webdriver.Chrome("C:/Users/88691/Downloads/chromedriver_win32/chromedriver.exe")

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
    class_element = driver.find_elements(By.CLASS_NAME,"Pagination_itemNavigation__wHk0M")
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
    #scrape data from CakeResume
    driver.get("https://www.cakeresume.com/jobs?profession%5B0%5D=it&job_type%5B0%5D=internship&order=latest")
    time.sleep(5)

    #click the button which lets the updated time be sorted from new to old
    bar = driver.find_elements(By.CLASS_NAME,'DropdownButton_button__lWImA')
    bar[12].click()
    newest = driver.find_elements(By.CLASS_NAME,'InstantSearchSortBy_name__tTVDl')
    newest[1].click()
    time.sleep(5)

    sum=10
    companies=[] #store companies in CakeResume to skip the same openings in 104 later
    while(sum==10):
        upload_cake = driver.find_elements(By.CLASS_NAME,"fa-clock") 
        sum = 0
        
        for i in upload_cake:
            time_cake = i.find_element(By.XPATH,"..").find_element(By.XPATH,"..")
            if "天" in time_cake.text:
                s = [int(s) for s in re.findall(r'\d+', time_cake.text)]  #regular expression, \d means number, and '\d+' means a set of number
                if(s[0]<=14):
                    sum+=1
            else:
                sum+=1
            
        if(sum!=0):
        
            wrapper = driver.find_elements(By.CLASS_NAME,"JobSearchItem_content__TKBfA") 
        
            for job in range(sum):
                title_cake = wrapper[job].find_element(By.CLASS_NAME,"JobSearchItem_jobTitle__Fjzv2") 

                try:
                    salaries_cake = wrapper[job].find_element(By.CLASS_NAME,"fa-dollar-sign")
                    salary_cake = salaries_cake.find_element(By.XPATH,"..").find_element(By.XPATH,"..").find_element(By.XPATH,"..").find_element(By.XPATH,"..") #its parent class   
                    salary_text= salary_cake.text.strip()
                except:
                    salary_text=""


                companies_cake = wrapper[job].find_element(By.CLASS_NAME,"JobSearchItem_companyName__QKkj5")
           
            
                try:
                    places_cake = wrapper[job].find_element(By.CSS_SELECTOR,".JobSearchItem_featureSegments__I1Csc span")
                    place_cake = places_cake.text.strip()
                except:
                    place_cake = ""
    

                hrefs_cake = wrapper[job].find_element(By.CLASS_NAME ,"JobSearchItem_jobTitle__Fjzv2")
                href_cake = hrefs_cake.get_attribute("href").strip()
           
                if("資安" not in title_cake.text.strip()):
                    internCake_info = {'date':"",                                       #last updated date 
                                       'title':title_cake.text.strip(),                 #title
                                       'salary':salary_text,                            #salary
                                       'company':companies_cake.text.strip(),           #company name
                                       'place':place_cake,                              #place
                                       'url':href_cake}                                 #detail url
                

                if('股份有限公司' in (companies_cake.text)): 
                    companies.append(companies_cake.text.replace('股份有限公司','').strip()) #to increase similarity
                else:
                    companies.append(companies_cake.text.strip())
                
                #print(internCake_info)
                dicts.append(internCake_info)

            next_page()
            time.sleep(5)
    print("countcake:",len(dicts))
    
    #scrape data in 104
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
            
            if (('論件計酬' not in salaries104_processed[i]) and ('資安' not in titles_104[i].text)):
            
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




#data.to_excel('sample_data.xlsx', sheet_name='sheet1', index=False)  #export data to excel
