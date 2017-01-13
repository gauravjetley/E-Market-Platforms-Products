#%% 

import requests
from bs4 import BeautifulSoup
import os
import csv
import pandas as pd
import numpy as np
import time

#%%   declaring 2 variable swhich will be used later while printing the statements 

i = 0
h = 0

#%%

file = open(os.path.expanduser("A:\\Independent Research\\Data files\\All_Subdepartments.csv"),"wb")

header = "department_name,Sub_departmentname,rank,product_name,product_link,product_image_link,product_reviews_link,product_ratings,product_ratings_count,product_price" + "\n"
file.write(bytes(header))

#%%

f = open('A:/Independent Research/Data files/amazon_webpage_links.csv')
csv_f = csv.reader(f)

df = pd.DataFrame(columns=('Department_name','Sub_Department_name', 'Sub_department_link'))

for row in csv_f:
  df.loc[i] = [row[0],row[2],row[3]]
  i = i + 1  

dept_links = set(zip(df.Department_name,df.Sub_Department_name,df.Sub_department_link))

#%% used only selenium

for each in dept_links:
    
    if (each[2] == "Sub-department link" or  each[2] == "No Sub Department Link" or each[1] == "Amazon Underground"):
        print()
    else:
        depart_name = each[0]
        subdepart_name = each[1]
        subdepartment_link = each[2]
    
    print str(h) + " --- " + depart_name + " ---- " + subdepart_name + " ---- " + subdepartment_link
    h = h + 1
    
    list2_data = requests.get(subdepartment_link)
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
                 data = depart_name + "," + subdepart_name + "," + rank + "," + product_name.replace(",","") + "," +  product_link + "," + product_image.replace(",","") + "," + product_reviews_link  + "," + product_ratings.replace("\n","")  + "," + product_ratings_count.replace(",","") + "," + product_price.replace(",","") + "\n"
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
            
                 data = depart_name + "," + subdepart_name + "," + rank + "," + product_name.replace(",","") + "," +  product_link + "," + product_image.replace(",","") + "," + product_reviews_link  + "," + product_ratings.replace("\n","")  + "," + product_ratings_count.replace(",","") + "," + product_price.replace(",","") + "\n"
                #print rank
                 file.write(bytes(data.encode("utf-8")))  
             
file.close()

#%% used only selenium but in different way for testing purposes

file = open(os.path.expanduser("A:\\Independent Research\\All_Subdepartments.csv"),"wb")
header = "department_name,Sub_departmentname,rank,product_name,product_link,product_image_link,product_reviews_link,product_ratings,product_ratings_count,product_price" + "\n"
file.write(bytes(header))

h = 0

xlsx = pd.ExcelFile('A:/Independent Research/sub_dept.xlsx')
df = pd.read_excel(xlsx, 'Sheet1')

#%%

for i in range(377,len(df)):
    depart_name = df.iloc[i,0] 
    sub_departname = df.iloc[i,1] 
    sub_departlink = df.iloc[i,2]
    
    if ( sub_departlink == "No Sub Department Link" or sub_departname == "Amazon Underground"):
        print()
    else:
        print str(h) + " --- " + depart_name + " ---- " + sub_departname + " ---- " + sub_departlink
        h = h + 1
    
        list2_data = requests.get(sub_departlink)
        amazon_data_list2  = BeautifulSoup(list2_data.content, 'html.parser')
        all_page_links = amazon_data_list2.find("div",{"id":"zg_paginationWrapper"}).find("ol",{"class":"zg_pagination"}).findAll("li")

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
                    data = depart_name + "," + sub_departname + "," + rank + "," + product_name.replace(",","") + "," +  product_link + "," + product_image.replace(",","") + "," + product_reviews_link  + "," + product_ratings.replace("\n","")  + "," + product_ratings_count.replace(",","") + "," + product_price.replace(",","") + "\n"
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
                        
                    if  zg_itemWrapper.find("div",{"class":"zg_reviews"}) is None:
                        product_reviews_link = "NA"
                        product_ratings = "NA"  
                    else:
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
                
                    if  zg_itemWrapper.find("div",{"class":"zg_itemPriceBlock_compact"}) is None:
                        product_price = "NA"
                    else:
                        if zg_itemWrapper.find("div",{"class":"zg_itemPriceBlock_compact"}).find("div",{"class":"zg_price"}).find("strong",{"class":"price"}) is None:
                            product_price = "NA"
                        else:
                            product_price = zg_itemWrapper.find("div",{"class":"zg_itemPriceBlock_compact"}).find("div",{"class":"zg_price"}).find("strong",{"class":"price"}).text
            
                    data = depart_name + "," + sub_departname + "," + rank + "," + product_name.replace(",","") + "," +  product_link + "," + product_image.replace(",","") + "," + product_reviews_link  + "," + product_ratings.replace("\n","")  + "," + product_ratings_count.replace(",","") + "," + product_price.replace(",","") + "\n"
                    file.write(bytes(data.encode("utf-8")))  

file.close()

#%%

   