#%%

import requests
from bs4 import BeautifulSoup
import os
import csv
import pandas as pd

#%% Fetching the web page links

page = requests.get("https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_e_0_e_1")
amazon_data  = BeautifulSoup(page.content, 'html.parser')

file = open(os.path.expanduser("A:\\Independent Research\\Data files\\amazon_webpage_links.csv"),"wb")

dept = 0
amazon_dept_best_sellers  = amazon_data.find("ul",{"id":"zg_browseRoot"})

print len(amazon_dept_best_sellers.find("ul").findAll("li"))

for list1 in amazon_dept_best_sellers.find("ul").findAll("li"):
    
    dept = dept + 1
    print dept, " Department Name ------ ", list1.text
    
    list1_data = requests.get(list1.find("a").get("href"))
    amazon_data_list1  = BeautifulSoup(list1_data.content, 'html.parser')
    amazon_data_list1_list2 = amazon_data_list1.find("ul",{"id":"zg_browseRoot"})
    
    
    if amazon_data_list1_list2.find("ul").find("ul") is None :
        data = list1.text + "," + list1.find("a").get("href") + "," + "No Sub Department" + ","+ "No Sub Department Link" + "\n"
        print data
        file.write(bytes(data))
    else :   
        for list2 in amazon_data_list1_list2.find("ul").find("ul").findAll("li"):
             
            print "       Sub Department ---- " + list2.text
            if  list2.text == "Thread & Floss":
                data =  list1.text.replace(",","") + "," + list1.find("a").get("href") + "," + list2.text.replace(",","") + ","+ list2.find("a").get("href") + "," + " We will deal this later. There ia a bug in the Amazon web site!!!!!"  + "\n"
                file.write(bytes(data.encode("utf-8")))
                print "       Sub Department ---- " + list2.text + " -- We will deal this later. There ia a bug in the Amazon web site!!!!!"
            
            elif list2.text == "Yarn" or list2.text == "Jerseys" or list2.text == "Tax Preparation" or list2.text == "Photography" or list2.text == "Musical Instruments" or list2.text == "Pretend Play" or list2.text == "Shoes" or list2.text == "Test Preparation" or list2.text == "Office Lighting" or list2.text == "Hats" or list2.text == "Bags & Cases"  or list2.text == "Digital Picture Frames" or list2.text == "Puzzles & Games"  or list2.text == "Literary Journals"  or list2.text == "Men's Interest" or list2.text == "Music"  or list2.text == "Animal Care & Pets" or list2.text == "Religion" or list2.text == "Travel" or list2.text == "Women's Interest" or list2.text == "Pest Control" or list2.text == "Sports & Leisure":
                 data =  list1.text.replace(",","") + "," + list1.find("a").get("href") + "," + list2.text.replace(",","") + ","+ list2.find("a").get("href") + "," + " We have already collected this details. There ia a bug in the Amazon web site!!!!! " +","+ "No Child Links " + "\n"
                 file.write(bytes(data.encode("utf-8")))
                 print "       Sub Department ---- " + list2.text + " We have already collected this details. There ia a bug in the Amazon web site!!!!!"
            else:
                 list2_data = requests.get(list2.find("a").get("href"))
             
                 amazon_data_list2  = BeautifulSoup(list2_data.content, 'html.parser')
                 amazon_data_list1_list222 = amazon_data_list2.find("div",{"id":"zg_left_colleft"})
             
                 zg_left_col1wrap = amazon_data_list1_list222.find("div",{"id":"zg_left_col1wrap"})
                 zg_left_col2 = amazon_data_list1_list222.find("div",{"id":"zg_left_col2"})
                 if zg_left_col2.find("ul",{"id":"zg_browseRoot"}).find("ul").find("li", {"class":"zg_browseUp"}) is None:
                     data =  list1.text.replace(",","") + "," + list1.find("a").get("href") + "," + list2.text.replace(",","") + ","+ list2.find("a").get("href") + "," + "No Child Elements" +","+ "No Child Links " + "\n"
                     file.write(bytes(data.encode("utf-8")))
                 else:
                     child_links = zg_left_col2.find("ul",{"id":"zg_browseRoot"}).find("ul").find("ul").find("ul").findAll("li")
                     for each_child_link in child_links:
                         print "                  Child/Categories ---- " + each_child_link.find("a").text 
                         data =  list1.text.replace(",","") + "," + list1.find("a").get("href") + "," + list2.text.replace(",","") + ","+ list2.find("a").get("href") + "," + each_child_link.find("a").text  +","+ each_child_link.find("a").get("href") +  "\n"
                         #print(each_child_link)
                         file.write(bytes(data.encode("utf-8")))                                            
file.close()


#%% testing for a particular range of departments

file = open(os.path.expanduser("A:\\Independent Research\\Data files\\amazon_webpage_links_test.csv"),"wb")
dept = 0

page = requests.get("https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_e_0_e_1")
amazon_data  = BeautifulSoup(page.content, 'html.parser')
amazon_dept_best_sellers  = amazon_data.find("ul",{"id":"zg_browseRoot"})

print len(amazon_dept_best_sellers.find("ul").findAll("li"))   # checking on how many departments avaliable

for num in range(34,40):
    
     for list1 in amazon_dept_best_sellers.find("ul").findAll("li")[num]:

         print num, " Department Name ------ ", list1.text
         
         list1_data = requests.get(list1.get("href"))

         amazon_data_list1  = BeautifulSoup(list1_data.content, 'html.parser')
         amazon_data_list1_list2 = amazon_data_list1.find("ul",{"id":"zg_browseRoot"})
    
         if amazon_data_list1_list2.find("ul").find("ul") is None :
             data = list1.text + "," + list1.find("a").get("href") + "," + "No Sub Department" + ","+ "No Sub Department Link" + "\n"
             print data
             file.write(bytes(data))
         else :   
             for list2 in amazon_data_list1_list2.find("ul").find("ul").findAll("li"):
                 print "       Sub Department ---- " + list2.text
                 if  list2.text == "Thread & Floss":
                     print "       Sub Department ---- " + list2.text + " -- We will deal this later. There ia a bug in the Amazon web site!!!!!"
                 elif list2.text == "Yarn" or list2.text == "Jerseys" or list2.text == "Tax Preparation" or list2.text == "Photography" or list2.text == "Musical Instruments" or list2.text == "Pretend Play" or list2.text == "Shoes" or list2.text == "Test Preparation" or list2.text == "Office Lighting" or list2.text == "Hats" or list2.text == "Bags & Cases"  or list2.text == "Digital Picture Frames" or list2.text == "Puzzles & Games"  or list2.text == "Literary Journals"  or list2.text == "Men's Interest" or list2.text == "Music"  or list2.text == "Animal Care & Pets" or list2.text == "Religion" or list2.text == "Travel" or list2.text == "Women's Interest" or list2.text == "Pest Control" or list2.text == "Sports & Leisure":
                     print "        The Sub Department ---- " + list2.text + " We have already collected this details. There ia a bug in the Amazon web site!!!!!"
                 else:
                     list2_data = requests.get(list2.find("a").get("href"))
             
                     amazon_data_list2  = BeautifulSoup(list2_data.content, 'html.parser')
                     amazon_data_list1_list222 = amazon_data_list2.find("div",{"id":"zg_left_colleft"})
             
                     zg_left_col1wrap = amazon_data_list1_list222.find("div",{"id":"zg_left_col1wrap"})
                     zg_left_col2 = amazon_data_list1_list222.find("div",{"id":"zg_left_col2"})
                     if zg_left_col2.find("ul",{"id":"zg_browseRoot"}).find("ul").find("li", {"class":"zg_browseUp"}) is None:
                         data =  list1.text.replace(",","") + "," + list1.get("href") + "," + list2.text.replace(",","") + ","+ list2.find("a").get("href") + "," + "No Child Elements" +","+ "No Child Links " + "\n"
                         file.write(bytes(data.encode("utf-8")))
                     else:
                         child_links = zg_left_col2.find("ul",{"id":"zg_browseRoot"}).find("ul").find("ul").find("ul").findAll("li")
                         for each_child_link in child_links:
                             print "                  Child/Categories ---- " + each_child_link.find("a").text 
                             data =  list1.text.replace(",","") + "," + list1.get("href") + "," + list2.text.replace(",","") + ","+ list2.find("a").get("href") + "," + each_child_link.find("a").text  +","+ each_child_link.find("a").get("href") +  "\n"
                         #print(each_child_link)
                             file.write(bytes(data.encode("utf-8")))   
file.close()

