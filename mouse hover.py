#%%

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


#%%

driver = webdriver.Chrome( 'A:/Independent Research/chromedriver.exe')

#%%
driver.get("https://www.amazon.com/Best-Sellers-Appliances/zgbs/appliances")
driver.maximize_window()

nums = [x for x in range(1,21)]
        
#%%

element =  driver.find_element_by_class_name("a-icon-alt")
ActionChains(driver).move_to_element(element).perform()

rows =  driver.find_elements_by_class_name("a-histogram-row")
for each_row in rows:
    message = each_row.find_element_by_class_name("a-link-normal")
    print message.get_attribute("title")

#%%

elements = driver.find_elements_by_class_name("zg_itemImmersion")
element = elements[3].find_element_by_class_name("a-icon-alt")

ActionChains(driver).move_to_element(element).perform()

rows =  driver.find_elements_by_class_name("a-histogram-row")
for each_row in rows:
    message = each_row.find_element_by_class_name("a-link-normal")
    print message.get_attribute("title")

#%%        
for j in nums:
    
    string = "a-popover-"
    string2 = string + str(j)
    j = j - 1
    print string2
    
    element =  elements[j].find_element_by_class_name("a-icon-alt")
    ActionChains(driver).move_to_element(element).perform()

    table = driver.find_element_by_id("//div[@id='a-popover-1']")
    table = table.find_element_by_id("histogramTable")
#%% 
    rows =  table.find_elements_by_class_name("a-histogram-row")
    for each_row in rows:
        #print each_row
        message = each_row.find_element_by_class_name("a-link-normal")
        print message.get_attribute("title")

        
#%%
driver1.get("https://www.amazon.com/Best-Sellers-Appliances/zgbs/appliances")
driver1.maximize_window()

#%%
element =  driver.find_element_by_class_name("a-icon-alt")

ActionChains(driver).move_to_element(element).perform()

#%%

elements = driver.find_elements_by_class_name("zg_itemImmersion")

print elements
nums = [x for x in range(1,21)]
print nums

#%%        
for j in nums:
    
    string = "a-popover-"
    string2 = string + str(j)
    j = j - 1
    print string2
    
    element =  elements[j].find_element_by_class_name("a-icon-alt")
    hover = ActionChains(driver).move_to_element(element)
    hover.perform()

    table = driver.find_element_by_id("//div[@id='a-popover-1']")
    table = table.find_element_by_id("histogramTable")
#%% 
    rows =  table.find_elements_by_class_name("a-histogram-row")
    for each_row in rows:
        #print each_row
        message = each_row.find_element_by_class_name("a-link-normal")
        print message.get_attribute("title")
        
