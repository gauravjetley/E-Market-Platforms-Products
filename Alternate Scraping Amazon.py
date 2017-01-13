#%%
import requests
from bs4 import BeautifulSoup
import os
import csv

#%%# creating a function to retun the soup data

def make_soup(url):
    thepage = urllib.urlopen(url)
    soupdata = BeautifulSoup(thepage, "html.parser")
    return soupdata
    
#%%

page = requests.get("https://www.amazon.com//gp/site-directory/ref=nav_shopall_btn")
amazon = BeautifulSoup(page.content, 'html.parser')

#%%

amazon_data = amazon.find("div", {"class":"a-container fsdContainerWrapper"}).findAll("div",{"class":"a-column a-span3 fsdColumn fsdColumn_3"})
print(amazon_data)

#%%

for depart_cols in amazon_data:
    for deprt_items in depart_cols.findAll("div", {"class":"fsdDeptBox"}):
        department_link = deprt_items.find("img",{"class":"fsdDeptFullImage"}).get("src")
        department_name = deprt_items.find("h3",{"class":"fsdDeptTitle"}).text
        print department_name + " -- "+ department_link
        for deprt_links in deprt_items.find("div",{"class":"fsdDeptCol"}).findAll("a"):
            print deprt_links.text + " -- "+ deprt_links.get("href")+ "\n" 

#%%

page = requests.get("https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_e_0_e_1")
amazon_data  = BeautifulSoup(page.content, 'html.parser')

#%%
header = "Department_name,Sub_Department_name,Rank,item_name,item_link,Rating, rating_link,ratings_count,price,Prime_status" + "\n"
file = open(os.path.expanduser("A:\\Independent Research\\amazon_scrape.csv"),"wb")

page = requests.get("https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_e_0_e_1")
amazon_data  = BeautifulSoup(page.content, 'html.parser')

dept = 0
amazon_dept_best_sellers  = amazon_data.find("ul",{"id":"zg_browseRoot"})

print len(amazon_dept_best_sellers.find("ul").findAll("li"))

for list1 in amazon_dept_best_sellers.find("ul").findAll("li"):
    
    dept = dept + 1
    print dept, " -----Department Name ------ ", list1.text
    
    if list1.text == "Appstore for Android" :
        print("this department will be processed later")
    else:

        list1_data = requests.get(list1.find("a").get("href"))
        amazon_data_list1  = BeautifulSoup(list1_data.content, 'html.parser')
        amazon_data_list1_list2 = amazon_data_list1.find("ul",{"id":"zg_browseRoot"})
        
              
        if amazon_data_list1_list2.find("ul").find("ul") is None :
           print "No sub links available for the department"         
        else :   
           for list2 in amazon_data_list1_list2.find("ul").find("ul").findAll("li"):
               print list2.text, " --- Sub department name ", list2.find("a").get("href")
               
               list2_data = requests.get(list2.find("a").get("href"))
               amazon_data_list2  = BeautifulSoup(list2_data.content, 'html.parser')
               all_page_links = amazon_data_list2.find("div",{"id":"zg_paginationWrapper"}).find("ol",{"class":"zg_pagination"}).findAll("li")
            
               for each_page_link in all_page_links:
                   page_link = each_page_link.find("a").get("href")
                #print(page_link)
                   list4_data = requests.get(page_link)
                   amazon_data_list4  = BeautifulSoup(list4_data.content, 'html.parser')
        
                   amazon_data_list1_list2_list3 = amazon_data_list4.find("div",{"id":"zg_left_col1"}).find("div",{"id":"zg_centerListWrapper"}).findAll("div",{"class":"zg_itemImmersion"})
                   for list3 in amazon_data_list1_list2_list3:
                       rank = list3.find("div",{ "class":"zg_rankDiv"}).find("span",{"class":"zg_rankNumber"}).text

                       if list3.find("div",{"class":"zg_itemWrapper"}).find("div",{"class":"a-section a-spacing-none p13n-asin"}) is None:
                           print("Product details are not avaliable for this rank", rank.replace("\n",""))
                           product_name = "NA"
                           product_link = "NA"
                           rating = "NA"
                           rating_link = "NA"
                           ratings_count = "NA"
                           product_price = "NA"
                           product_prime = "NA"
                       else:
                           product_name = list3.find("div",{"class":"zg_itemWrapper"}).find("div",{"class":"a-section a-spacing-none p13n-asin"}).find("a",{"class":"a-link-normal"}).text
                           product_link = list3.find("div",{"class":"zg_itemWrapper"}).find("div",{"class":"a-section a-spacing-none p13n-asin"}).find("a",{"class":"a-link-normal"}). get("href")
                    
                           if list3.find("div",{"class":"zg_itemWrapper"}).find("div",{"class":"a-section a-spacing-none p13n-asin"}).find("div",{"class":"a-icon-row a-spacing-none"}) is None:
                               print("No Ratings available for this product", rank.replace("\n",""))
                               rating = "NA"
                               rating_link = "NA"
                               ratings_count = "NA"
                           else:
                               rating       = list3.find("div",{"class":"zg_itemWrapper"}).find("div",{"class":"a-section a-spacing-none p13n-asin"}).find("div",{"class":"a-icon-row a-spacing-none"}).find("a",{"class":"a-link-normal"}).get("title")
                               rating_link  = list3.find("div",{"class":"zg_itemWrapper"}).find("div",{"class":"a-section a-spacing-none p13n-asin"}).find("div",{"class":"a-icon-row a-spacing-none"}).find("a",{"class":"a-link-normal"}).get("href")
                               ratings_count = list3.find("div",{"class":"zg_itemWrapper"}).find("div",{"class":"a-section a-spacing-none p13n-asin"}).find("div",{"class":"a-icon-row a-spacing-none"}).find("a",{"class":"a-size-small a-link-normal"}).text
                    
                           if list3.find("div",{"class":"zg_itemWrapper"}).find("div",{"class":"a-section a-spacing-none p13n-asin"}).find("div",{"class":"a-row"}) is None:
                               product_price = "No Price avaliable for the product"
                               product_prime = "Not Sure"
                           else:
                               prod_price_details = list3.find("div",{"class":"zg_itemWrapper"}).find("div",{"class":"a-section a-spacing-none p13n-asin"}).find("div",{"class":"a-row"})
                               if prod_price_details.find(attrs = {"class":"aok-offscreen p13n-sc-offscreen"}) is None:
                                   product_price = prod_price_details.find(attrs = {"class":"a-size-base a-color-price"}).find(attrs = {"class":"p13n-sc-price"}).text
                                   if prod_price_details.find(attrs = {"class":"a-icon a-icon-prime a-icon-small"}) is None:
                                       product_prime = "Not Prime"
                                   else:
                                       product_prime = prod_price_details.find(attrs = {"class":"a-icon a-icon-prime a-icon-small"}).get("aria-label")
                               else:
                                   product_price = "Find the product price in the link......"
                                   product_prime = "Not Sure"
                          #print rank.replace("\n","") + " " + product_name + " " + product_link + " " + rating + " " + rating_link + " " + ratings_count
                           Product_data = list1.text + "," + list2.text + "," + rank.replace("\n","") + "," + product_name.replace(",","") + "," + product_link + "," + rating + "," + rating_link + "," + ratings_count + "," + product_price + "," + product_prime + "\n"
                           file.write(bytes(Product_data.encode("utf-8")))
 
#%%

page = requests.get("https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_e_0_e_1")
amazon_data  = BeautifulSoup(page.content, 'html.parser')

file = open(os.path.expanduser("A:\\Independent Research\\amazon_scrape.csv"),"wb")

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
                print "       Sub Department ---- " + list2.text + " -- We will deal this later. There ia a bug in the Amazon web site!!!!!"
            elif list2.text == "Yarn" or list2.text == "Test Preparation" or list2.text == "Office Lighting"  or list2.text == "Bags & Cases"  or list2.text == "Digital Picture Frames" or list2.text == "Puzzles & Games"  or list2.text == "Literary Journals"  or list2.text == "Men's Interest" or list2.text == "Music"  or list2.text == "Animal Care & Pets" or list2.text == "Religion" or list2.text == "Travel" or list2.text == "Women's Interest" or list2.text == "Pest Control"  or list2.text == "Photography" or list2.text == "Tax Preparation" or list2.text == "Sports & Leisure":
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


#%%

page = requests.get("https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_e_0_e_1")
amazon_data  = BeautifulSoup(page.content, 'html.parser')

file = open(os.path.expanduser("A:\\Independent Research\\amazon_scrape.csv"),"wb")

dept = 0
amazon_dept_best_sellers  = amazon_data.find("ul",{"id":"zg_browseRoot"})

print len(amazon_dept_best_sellers.find("ul").findAll("li"))


for num in range(36,40):
    
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
                 elif list2.text == "Yarn" or list2.text == "Jerseys" or list2.text == "Musical Instruments" or list2.text == "Pretend Play" or list2.text == "Shoes" or list2.text == "Test Preparation" or list2.text == "Office Lighting" or list2.text == "Hats" or list2.text == "Bags & Cases"  or list2.text == "Digital Picture Frames" or list2.text == "Puzzles & Games"  or list2.text == "Literary Journals"  or list2.text == "Men's Interest" or list2.text == "Music"  or list2.text == "Animal Care & Pets" or list2.text == "Religion" or list2.text == "Travel" or list2.text == "Women's Interest" or list2.text == "Pest Control" or list2.text == "Sports & Leisure":
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

