import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import time
import json
import re
from selenium.webdriver.common.action_chains import ActionChains
import string
from selenium.webdriver.support.select import Select
import math
import requests

items = []
variants=[]
driver = webdriver.Chrome(executable_path="C:/Users/16104/OneDrive/Web Drivers/chromedriver.exe")
url = 'https://wemakegood.ie/collections/all-1'
driver.get(url)
driver.maximize_window()

# Going through products
product_text = driver.find_element_by_class_name("count").text
split = product_text.split(" ")
prodAmount = split[4].replace('.','')
print("total product amount: " + prodAmount)
number = int(prodAmount)
totalPages = math.ceil(number / 26)  # 26 is the max amount of products on a page
print('{}{}'.format("total pages to paginate to: ", totalPages))
while True:
    for i in range(totalPages):
        time.sleep(1)
        prodCont = driver.find_element_by_xpath('//*[@id="collection-page"]/div[6]')
        products = prodCont.find_elements_by_class_name('prod-image')
        print('{}{}'.format("total amount of products per page: ", len(products)))
        print('{}{}'.format("page number: ", i))
        # for p in range(2):
        for p in range(len(products)):
            print('{}{}'.format("product number: ", p))
            prodCont = driver.find_element_by_xpath('//*[@id="collection-page"]/div[6]')
            products = prodCont.find_elements_by_class_name('prod-image')
            products[p].click()

        # pagination
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "row"))
            )
            # for last page
            if i == (totalPages - 1):
                break
            else:
                next = "document.getElementsByClassName('fa fa-angle-right')[0].click();"
                driver.execute_script(next)
        except (ElementNotVisibleException, NoSuchElementException):
            break
    break
# going back to category page
time.sleep(1)
for i in range(totalPages):
    driver.back()

driver.quit

