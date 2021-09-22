import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import time
import requests
import re
import csv
import json
#hello
driver = webdriver.Chrome(executable_path="C:/Users/16104/OneDrive/Web Drivers/chromedriver.exe")
url = 'https://www.magne.ie/collections'
categories = []
items = []
productObjects = []
results = []
waste = []
names = []
totalProducts = 0
totalAdded = 0
driver.get(url)
driver.maximize_window()
catalog = driver.find_element_by_xpath('//*[@id="nav"]/div/nav[1]/ul/li[2]/a').click()
productObject = {}
content = driver.page_source
soup = BeautifulSoup(content, "html.parser")

for cat in soup.findAll("h4", class_="title"):
    print(cat.text)
    if cat.text not in categories:
        categories.append(cat.text)
categories.remove(categories[0])
print(len(categories))

# loop through categories in catalog
for cat in range(len(categories)):
    categories = driver.find_elements_by_class_name("title")[cat]
    catName = categories.text
    categories.click()

    # loop through products in page
    while True:
        product_amount = len(driver.find_elements_by_class_name("title"))
        print(product_amount)
        totalProducts += product_amount
        for i in range(product_amount):
            p = i + 1
            time.sleep(1)
            products = driver.find_elements_by_class_name("title")[i]
            products.click()

            # product details
            quantity = driver.find_element_by_class_name("purchase").text
            if quantity == "Sold Out":
                quantity = 0
            else:
                quantity = 1

            descriptions = []
            description = driver.find_element_by_class_name("description")
            each = description.find_elements_by_tag_name("p")
            for i in range(len(each)):
                descriptions.append(each[i].text)
            each2 = description.find_elements_by_tag_name("span")
            for i in range(len(each2)):
                descriptions.append(each2[i].text)
            each3 = description.find_elements_by_tag_name("div")
            for i in range(len(each3)):
                descriptions.append(each3[i].text)

            image = driver.find_element_by_class_name("zoom").get_attribute("href")
            price = driver.find_element_by_class_name("price").text
            beginTxt = '?v='
            start = image.find(beginTxt) + len(beginTxt)
            sku = image[start:]

            try:
                relateds = []
                related = driver.find_element_by_xpath('//*[@id="product"]/div[3]')
                eachRel = related.find_elements_by_tag_name("h4")
                for i in range(len(eachRel)):
                    relateds.append(eachRel[i].text)
            except (ElementNotVisibleException, NoSuchElementException):
                relateds.clear()

            try:
                images = []
                imageCont = driver.find_element_by_class_name("span1")
                eachImg = imageCont.find_elements_by_tag_name("a")
                for i in range(len(eachImg)):
                    images.append(eachImg[i].get_attribute("href"))
            except (ElementNotVisibleException, NoSuchElementException):
                images.append(image)


            def listToString(s):
                str1 = " "
                return (str1.join(s))


            imageList = listToString(images).replace(" ", "&&")
            descriptionList = listToString(descriptions)
            relatedList = listToString(relateds).replace(" ", "&&")

            productObject = {
                "name": driver.find_element_by_class_name("title").text,
                "price": price[1:],
                "images": imageList,
                "description": descriptionList,
                "sku": sku,
                "categories": catName,
                "relatedProducts": relatedList,
                "vendor": "magne@magne.ie",
                "quantity": quantity
            }
            if sku not in names:
                names.append(sku)
                productObjects.append(productObject)
                print("product #", p, " added!")
                print(productObject)
                totalAdded += 1
            else:
                print("already in list!")

            driver.back()
        # pagination
        try:
            driver.find_element_by_class_name("next").click()
            time.sleep(2)
        except (ElementNotVisibleException, NoSuchElementException):
            driver.find_element_by_xpath('//*[@id="nav"]/div/nav[1]/ul/li[2]/a').click()
            break
print("total products: ", totalProducts)
print("total products in list", totalAdded)
# convert to excel file
df_data = pd.DataFrame(items)
df_data.to_excel("products-magne.xlsx", index=False)
driver.close()


