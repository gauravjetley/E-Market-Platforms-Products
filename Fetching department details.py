while True:
    print "This prints once a minute."
    time.sleep(20)  # Delay for 1 minute (60 seconds)
#%%

import requests
from bs4 import BeautifulSoup
import os
import csv
import pandas as pd
import numpy as np

#%%  Used only Selenium

#  creating the file All_Departments.csv where we have write the product detail collected
file = open(os.path.expanduser("A:\\Independent Research\\Data files\\All_Departments.csv"),"wb")
header = "department_name,rank,product_name,product_link,product_image_link,product_reviews_link,product_ratings,product_ratings_count,product_price" + "\n"
file.write(bytes(header))

# declared 2 variables which will help later in the code while printing the statements
i = 0
j = 0

# fetching the department name and department links from the amazon_webpage_links.csv
f = open('A:/Independent Research/Data files/amazon_webpage_links.csv')
csv_f = csv.reader(f)

df = pd.DataFrame(columns=('Department_name', 'department_link'))

for row in csv_f:
  if row[0] == "MP3 Downloads":
      print ""
  else:
      df.loc[j] = [row[0], row[1]]
      j = j +1  

unique_dept_links = set(zip(df.Department_name, df.department_link))

for each in unique_dept_links:
    
    department_link = each[1]
    department_name = each[0]
    print  str(i) + " --- " + department_name + " --- " + department_link
    list2_data = requests.get(department_link)
    amazon_data_list2  = BeautifulSoup(list2_data.content, 'html.parser')
    all_page_links = amazon_data_list2.find("div",{"id":"zg_paginationWrapper"}).find("ol",{"class":"zg_pagination"}).findAll("li")

    i = i + 1
    for each_page_link in all_page_links:
        
        page_link = each_page_link.find("a").get("href")
        print(page_link)
        list4_data = requests.get(page_link)
        amazon_data_list4  = BeautifulSoup(list4_data.content, 'html.parser')
    
        amazon_product_data = amazon_data_list4.find("div",{"id":"zg_left_col1"}).find("div",{"id":"zg_centerListWrapper"}).findAll("div",{"class":"zg_itemImmersion"})
        for list3 in amazon_product_data:
            rank = list3.find("div",{ "class":"zg_rankDiv"}).find("span",{"class":"zg_rankNumber"}).text
            if len(list3.find("div",{"class":"zg_itemWrapper"}).findAll("div")) == 0:
                product_name = "Product details are not avaliable for this rank"
                product_link = "NA"
                product_image = "NA"
                product_reviews_link = "NA"
                product_ratings = "NA"
                product_ratings_count = "NA"
                product_price = "NA"
                data = department_name + "," + rank + "," + product_name.replace(",","") + "," +  product_link + "," + product_image.replace(",","") + "," + product_reviews_link  + "," + product_ratings.replace("\n","")  + "," + product_ratings_count.replace(",","") + "," + product_price.replace(",","") + "\n"
                #print rank
                file.write(bytes(data.encode("utf-8")))  
            else:
                zg_itemWrapper = list3.find("div",{"class":"zg_itemWrapper"})
                
                if zg_itemWrapper.find("div",{"class":"zg_image"}) is None:
                    product_image = "NA"
                else:
                    product_image = zg_itemWrapper.find("div",{"class":"zg_image"}).find("div",{"class":"zg_itemImageImmersion"}).find("img").get("src")
                
                if zg_itemWrapper.find("div",{"class":"zg_title"}) is None:
                    product_name = "NA"
                    product_link = "NA"
                else:
                    product_name = zg_itemWrapper.find("div",{"class":"zg_title"}).text
                    product_link = zg_itemWrapper.find("div",{"class":"zg_title"}).find("a").get("href").replace("\n","")
            
                if zg_itemWrapper.find("div",{"class":"zg_reviews"}).find("a",{"class":"a-link-normal a-text-normal"}) is None:
                    product_reviews_link = "NA"
                    product_ratings = "NA"
                else:
                    product_reviews = zg_itemWrapper.find("div",{"class":"zg_reviews"}).findAll("a",{"class":"a-link-normal a-text-normal"})
                    product_reviews_link = product_reviews[0].get("href")
                    product_ratings = product_reviews[0].text
                
                if zg_itemWrapper.find("div",{"class":"zg_reviews"}).find("span",{"class":"a-size-small"}) is None:
                    product_ratings_count = "NA"
                else:
                    product_ratings_count = zg_itemWrapper.find("div",{"class":"zg_reviews"}).find("span",{"class":"a-size-small"}).find("a",{"class":"a-link-normal"}).text 
                
                if zg_itemWrapper.find("div",{"class":"zg_itemPriceBlock_compact"}).find("div",{"class":"zg_price"}).find("strong",{"class":"price"}) is None:
                    product_price = "NA"
                else:
                    product_price = zg_itemWrapper.find("div",{"class":"zg_itemPriceBlock_compact"}).find("div",{"class":"zg_price"}).find("strong",{"class":"price"}).text
            
                data = department_name + "," + rank + "," + product_name.replace(",","") + "," +  product_link + "," + product_image.replace(",","") + "," + product_reviews_link  + "," + product_ratings.replace("\n","")  + "," + product_ratings_count.replace(",","") + "," + product_price.replace(",","") + "\n"
                #print rank
                file.write(bytes(data.encode("utf-8")))  
            
file.close()

#%% Using both Selenium and Beautiful Soup

import requests
from bs4 import BeautifulSoup
import os
import csv
import pandas as pd
import numpy as np
import random

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait

#%% creating the file All_Departments.csv for writing the product details fetched from website

file = open(os.path.expanduser("A:\\Independent Research\\Data files\\All_Departments.csv"),"wb")

header = "department_name,rank,product_name,product_link,product_image_link,product_reviews_link,product_ratings,product_ratings_count,product_price" + "\n"
file.write(bytes(header))

#%% fetching  unique departments list

xlsx = pd.ExcelFile('A:/Independent Research/Data files/dept.xlsx')
df = pd.read_excel(xlsx, 'Sheet1')

#%%

nums = [x for x in range(0,40)]
random.shuffle(nums)

pages = [x for x in range(0,5)]
random.shuffle(pages)

#%%

driver = webdriver.Chrome( 'A:/Independent Research/Drivers/chromedriver.exe')
driver1 = webdriver.Chrome( 'A:/Independent Research/Drivers/chromedriver.exe')

#driver2 = webdriver.Firefox(executable_path ='A:/Independent Research/Drivers/geckodriver.exe')

#%%

for num in nums:
    
    department_name = df.iloc[num,0]
    department_link = df.iloc[num,1]
    
    print  str(num) + " --- " + department_name + " --- " + department_link
    
    driver.get(department_link)
    driver.maximize_window()
    
    all_page_links = driver.find_elements_by_xpath("//div[@id='zg_paginationWrapper']/ol[@class='zg_pagination']/li")
    
    for each in all_page_links:
        page = each.find_element_by_tag_name("a")
        page_link = page.get_attribute("href")
        print page_link
        
        driver1.get(page_link)
        driver1.maximize_window()
        
        amazon_data_list4  = BeautifulSoup(driver1.page_source)
        amazon_product_data = amazon_data_list4.find("div",{"id":"zg_left_col1"}).find("div",{"id":"zg_centerListWrapper"}).findAll("div",{"class":"zg_itemImmersion"})
        
        elements = driver1.find_elements_by_class_name("zg_itemImmersion")
        
        for list3 in amazon_product_data:
            rank = list3.find("div",{ "class":"zg_rankDiv"}).find("span",{"class":"zg_rankNumber"}).text
            
            if len(list3.find("div",{"class":"zg_itemWrapper"}).findAll("div")) == 0:
                product_name = "Product details are not avaliable for this rank"
                product_link = "NA"
                product_image = "NA"
                product_reviews_link = "NA"
                product_ratings = "NA"
                product_ratings_count = "NA"
                product_price = "NA"
                data = department_name + "," + rank + "," + product_name.replace(",","") + "," +  product_link + "," + product_image.replace(",","") + "," + product_reviews_link  + "," + product_ratings.replace("\n","")  + "," + product_ratings_count.replace(",","") + "," + product_price.replace(",","") + "\n"
                #print rank
                file.write(bytes(data.encode("utf-8")))  

            else:
                zg_itemWrapper = list3.find("div",{"class":"zg_itemWrapper"})
                
                if zg_itemWrapper.find("div",{"class":"zg_image"}) is None:
                    product_image = "NA"
                else:
                    product_image = zg_itemWrapper.find("div",{"class":"zg_image"}).find("div",{"class":"zg_itemImageImmersion"}).find("img").get("src")
                
                if zg_itemWrapper.find("div",{"class":"zg_title"}) is None:
                    product_name = "NA"
                    product_link = "NA"
                else:
                    product_name = zg_itemWrapper.find("div",{"class":"zg_title"}).text
                    product_link = zg_itemWrapper.find("div",{"class":"zg_title"}).find("a").get("href").replace("\n","")
            
                if zg_itemWrapper.find("div",{"class":"zg_reviews"}).find("a",{"class":"a-link-normal a-text-normal"}) is None:
                    product_reviews_link = "NA"
                    product_ratings = "NA"
                else:
                    product_reviews = zg_itemWrapper.find("div",{"class":"zg_reviews"}).findAll("a",{"class":"a-link-normal a-text-normal"})
                    product_reviews_link = product_reviews[0].get("href")
                    product_ratings = product_reviews[0].text
                
                if zg_itemWrapper.find("div",{"class":"zg_reviews"}).find("span",{"class":"a-size-small"}) is None:
                    product_ratings_count = "NA"
                else:
                    product_ratings_count = zg_itemWrapper.find("div",{"class":"zg_reviews"}).find("span",{"class":"a-size-small"}).find("a",{"class":"a-link-normal"}).text 
                
                if zg_itemWrapper.find("div",{"class":"zg_itemPriceBlock_compact"}).find("div",{"class":"zg_price"}).find("strong",{"class":"price"}) is None:
                    product_price = "NA"
                else:
                    product_price = zg_itemWrapper.find("div",{"class":"zg_itemPriceBlock_compact"}).find("div",{"class":"zg_price"}).find("strong",{"class":"price"}).text
            
                data = department_name + "," + rank + "," + product_name.replace(",","") + "," +  product_link + "," + product_image.replace(",","") + "," + product_reviews_link  + "," + product_ratings.replace("\n","")  + "," + product_ratings_count.replace(",","") + "," + product_price.replace(",","") + "\n"
                #print rank
                file.write(bytes(data.encode("utf-8")))  
            
file.close()

#%%

 