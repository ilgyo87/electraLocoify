from selenium import webdriver
from bs4 import BeautifulSoup
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

chrome_driver_path="C:/Users/16104/OneDrive/Web Drivers/chromedriver.exe"
delay=15
items = []
variants=[]
driver = webdriver.Chrome(executable_path=chrome_driver_path)
url = 'https://ribbonrouge.ie/collections/'
driver.get(url)

# Going through categories
categoryCont = driver.find_element_by_id('product-loop')
categories = categoryCont.find_elements_by_tag_name('img')
print(len(categories))
for i in range(len(categories)):
    categoryCont = driver.find_element_by_id('product-loop')
    categories = categoryCont.find_elements_by_tag_name('img')
    categories[i].click()
    time.sleep(1)

    # Going through products
    product_text = driver.find_element_by_class_name("count").text
    split = product_text.split(" ")
    prodAmount = split[4].replace('.','')
    print("total product amount: " + prodAmount)
    number = int(prodAmount)
    totalPages = math.ceil(number / 50)  # 50 is the max amount of products on a page
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
                prodCont = driver.find_element_by_xpath('//*[@id="product-loop"]')
                products = prodCont.find_elements_by_class_name('prod-image')
                products[p].click()
                time.sleep(1)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                scripts = soup.find('script', class_="product-json")
                singleProd = str(scripts)

                # non variant item
                begin = '  {'
                end = '"variants": ['
                start = singleProd.find(begin) + len(begin)
                end = singleProd.find(end, start)
                script = singleProd[startSKU:endSKU]
                print(script)

                # # Sku
                # beginSKU = 'window.SwymProductInfo.product = {"id":'
                # endSKU = ',"title":'
                # startSKU = script.find(beginSKU) + len(beginSKU)
                # endSKU = script.find(endSKU, startSKU)
                # sku = script[startSKU:endSKU]
                #
                # # Name
                # beginNam = '"title":"'
                # endNam = '","'
                # startNam = script.find(beginNam) + len(beginNam)
                # endNam = script.find(endNam, startNam)
                # name = script[startNam:endNam]
                #
                # # Price
                # beginPri = 'pr: '
                # endPri = '/100,'
                # startPri = script.find(beginPri) + len(beginPri)
                # endPri = script.find(endPri, startPri)
                # priceNum = script[startPri:endPri]
                # price = int(priceNum) / 100
                #
                # # Stock Level
                # beginSto = 'stk: '
                # endSto = ','
                # startSto = script.find(beginSto) + len(beginSto)
                # endSto = script.find(endSto, startSto)
                # stockLevel = script[startSto:endSto]
                #
                # # Description
                # beginDes = '"description":"'
                # endDes = '","published_at"'
                # startDes = script.find(beginDes) + len(beginDes)
                # endDes = script.find(endDes, startDes)
                # description = script[startDes:endDes]
                # # newDes = description.replace('\\u003cp\\u003e',"").replace('\\u003c',"").replace("\\/p", "").replace("\\u003e", "").replace('\\ndiv class=', "").replace('\\"item-excerpt trunc', "").replace('\\" itemprop=', "").replace('\\"description', "").replace('\\" data-height=', "").replace('\\"230', "").replace('\\"', "").replace('\\u003e', "").replace('\\nspan', "").replace('\\/spanbr', "").replace('\\n', "").replace('\\/div', "").replace('britem-infoitem-infoitem-info data-mce-fragment=1 data-mce-fragment=1', " ").replace('britem-info', " ").replace('brinfoinfo-textdiv id=content-text class=content-text', " ").replace('\\/span',"").replace('item-infoitem-infoitem-infoitem-info',"").replace('item-infoitem-toolscheckout-toolsprice-info-wrapitem-info-wrapitem-infoitem-infoitem-toolscheckout-toolsprice-info-wrapitem-info-wrapitem-infoitem-infoitem-info',"")
                #
                # # Images
                # beginImg = '"image","src":"'
                # endImg = '","width"'
                # startImg = script.find(beginImg) + len(beginImg)
                # endImg = script.find(endImg, startImg)
                # images = script[startImg:endImg]
                #
                # productObject = {
                #     "sku": sku,
                #     "name": name,
                #     "price": price,
                #     "stockLevel": stockLevel,
                #     "images": images,
                #     "categories": "books",
                #     "vendor": "secretbook@live.com",
                #     "description": description,
                #     # "relatedProducts": relatedList
                # }
                # items.append(productObject)
                # driver.back()
                # time.sleep(1)

                time.sleep(1)
                driver.back()

            # pagination
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "desktop-12 tablet-6 mobile-3"))
                )
                # for last page
                if i == (totalPages - 1):
                    break
                else:
                    next = "document.getElementsByClassName('paginext')[0].click();"
                    driver.execute_script(next)
            except (ElementNotVisibleException, NoSuchElementException):
                break
        break
        # going back to category page
    time.sleep(1)
    for i in range(totalPages):
        driver.back()