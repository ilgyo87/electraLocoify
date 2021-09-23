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

productObjects=[]
variants=[]
results=[]
names =[]
totalProducts = 0
totalAdded = 0
def stringFinder(start, end, script):
    str1 = start
    str2 = end
    startP = script.find(str1) + len(str1)
    endP = script.find(str2, startP)
    string = script[startP:endP]
    return (str(string))
driver = webdriver.Chrome(executable_path="C:/Users/16104/PycharmProjects/electraLocoify/Web Drivers/chromedriver.exe")
options = Options()
options.headless = True
driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=options)
url = 'https://wemakegood.ie/collections/all-1'
driver.get(url)
driver.maximize_window()

# Finding amount of pages
product_text = driver.find_element_by_class_name("count").text
split = product_text.split(" ")
prodAmount = split[4].replace('.','')
print("total product amount: " + prodAmount)
number = int(prodAmount)
totalPages = math.ceil(number / 26)  # 26 is the max amount of products on a page
print('{}{}'.format("total pages to paginate to: ", totalPages))
# Going through pages
while True:
    for i in range(totalPages):
        prodCont = driver.find_element_by_xpath('//*[@id="collection-page"]/div[6]')
        products = prodCont.find_elements_by_class_name('prod-image')
        print('{}{}'.format("total amount of products per page: ", len(products)))
        print('{}{}'.format("page number: ", i+1))
        # for p in range(2):
        for p in range(len(products)):
            t=p+1
            variants.clear()
            prodCont = driver.find_element_by_xpath('//*[@id="collection-page"]/div[6]')
            products = prodCont.find_elements_by_class_name('prod-image')
            products[p].click()
            print('{}{}'.format("product number: ", t))

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            singleScript = str(soup.find('script', id = "product-json"))
            script = str(soup.find('script', class_= "analytics").find_previous('script').find_previous('script'))
            # single variant item
            for v in re.findall("\"option1\":[\s\S]*?\"weight_in_unit\":", singleScript):
                stringV = v
                variants.append(stringV)
            print(len(variants))
            time.sleep(2)
            if len(variants)>1:
                print("I got variants!")
                for w in range(len(variants)):
                    variantType = stringFinder('"option1": "','",',variants[w]).replace('u0026','')
                    variantSKU = stringFinder('"product_id": ',',',variants[w])
                    variantPrice = int(stringFinder('"price":',',',variants[w]))/100
                    variantQuantity = int(stringFinder('"inventory_quantity": ', ',', variants[w]))
                    sku = stringFinder('"id": ', ',', singleScript)
                    name = stringFinder('"title": "', '",', singleScript)
                    price = int(stringFinder('"price": ', ',', singleScript)) / 100
                    categories = stringFinder('"type": "', '",', singleScript)
                    stockLevel = ''
                    images = stringFinder('"images": ["', '],', singleScript).replace('\\', '').replace(',', '&&')
                    tags = stringFinder('"tags": ["', '],', singleScript).replace(',', '&&')
                    description = soup.find('div', class_='rte').text

                    productObject = {
                        "sku": sku,
                        "name": name,
                        "price": price,
                        "categories": categories,
                        "stockLevel": stockLevel,
                        "images": images,
                        "description": description,
                        "variantSKU": variantSKU,
                        "Type (field:class)": variantType,
                        "variantPrice": variantPrice,
                        "variantQuantity": variantQuantity,
                        "vendor": "info@wemakegood.ie",
                    }
                    if variantSKU not in names:
                        names.append(variantSKU)
                        productObjects.append(productObject)
                        print("product #", t, " added!")
                        print(productObject)
                        totalAdded += 1
                    else:
                        print("already in list!")

            else:
                print("I'm single!")
                sku = stringFinder('"id": ', ',', singleScript)
                name = stringFinder('"title": "', '",', singleScript)
                price = int(stringFinder('"price": ', ',', singleScript))/100
                categories = stringFinder('"type": "', '",', singleScript)
                stockLevel = int(stringFinder('"inventory_quantity": ', ',', singleScript))
                images = stringFinder('"images": ["', '],', singleScript).replace('\\','').replace(',','&&')
                tags = stringFinder('"tags": ["', '],', singleScript).replace(',','&&')
                description = soup.find('div',class_='rte').text

                productObject = {
                    "sku": sku,
                    "name": name,
                    "price": price,
                    "categories": categories,
                    "stockLevel": stockLevel,
                    "images": images,
                    "description": description,
                    "variantSKU": '',
                    "Type (field:class)": '',
                    "variantPrice": '',
                    "variantQuantity": '',
                    "vendor": "info@wemakegood.ie",
                }
                if sku not in names:
                    names.append(sku)
                    productObjects.append(productObject)
                    print("product #", t, " added!")
                    print(productObject)
                    totalAdded += 1
                else:
                    print("already in list!")


            driver.back()
            time.sleep(1)
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
                time.sleep(1)
        except (ElementNotVisibleException, NoSuchElementException):
            break
    break

print("total products: ", totalProducts)
print("total products in list", totalAdded)
# convert to excel file
df_data = pd.DataFrame(productObjects)
df_data.to_excel("products-wemakegood.xlsx", index=False)
driver.close()
driver.quit

