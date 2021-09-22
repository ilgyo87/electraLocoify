import pandas as pd
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

sort_by_type="newest"
chrome_driver_path="C:/Users/16104/OneDrive/Web Drivers/chromedriver.exe"
delay=15
items = []
variants=[]
driver = webdriver.Chrome(executable_path=chrome_driver_path)
url = 'https://www.thesecretbookstore.ie/collections/all-books'
driver.get(url)

try:
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID,'adroll_consent_accept')))
    driver.find_element_by_id('adroll_consent_accept').click()
except TimeoutException:
    print('Loading exceeds delay time')

def extract_text(soup_obj,tag,attribute_name,attribute_value):
    txt = soup_obj.find(tag, {attribute_name: attribute_value}).text().strip() if soup_obj.find(tag, {attribute_name: attribute_value}) else ''
    return txt

pagination = driver.find_element_by_class_name("pagination-custom")
pages = pagination.find_elements_by_tag_name('a')
print(len(pages))
pageAmount = pages[2].text
print('{}{}'.format("total pages to paginate to: ", pageAmount))
totalPages = int(pageAmount)

# for i in range(totalPages):
for i in range(101,164):
    time.sleep(1)
    pageURL = '{}{}{}'.format(url, "?page=", i + 1)
    print(pageURL)
    driver.get(pageURL)
    driver.maximize_window()
    prodCont = driver.find_element_by_xpath('//*[@id="CollectionSection"]/div/div[1]/div')
    products = prodCont.find_elements_by_class_name('product-grid-item')
    print('{}{}'.format("total amount of products per page: ", len(products)))
    print('{}{}'.format("page number: ", i + 1))
    for p in range(len(products)):
    # for p in range(2):
        print('{}{}'.format("product number: ", p + 1))
        prodCont = driver.find_element_by_xpath('//*[@id="CollectionSection"]/div/div[1]/div')
        products = prodCont.find_elements_by_class_name('product-grid-item')
        products[p].click()
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        scripts = soup.find('script', id="swym-snippet")
        script = str(scripts)

        # Sku
        beginSKU = 'window.SwymProductInfo.product = {"id":'
        endSKU = ',"title":'
        startSKU = script.find(beginSKU) + len(beginSKU)
        endSKU = script.find(endSKU, startSKU)
        sku = script[startSKU:endSKU]

        # Name
        beginNam = '"title":"'
        endNam = '","'
        startNam = script.find(beginNam) + len(beginNam)
        endNam = script.find(endNam, startNam)
        name = script[startNam:endNam]

        # Price
        beginPri = 'pr: '
        endPri = '/100,'
        startPri = script.find(beginPri) + len(beginPri)
        endPri = script.find(endPri, startPri)
        priceNum = script[startPri:endPri]
        price = int(priceNum) / 100

        # Stock Level
        beginSto = 'stk: '
        endSto = ','
        startSto = script.find(beginSto) + len(beginSto)
        endSto = script.find(endSto, startSto)
        stockLevel = script[startSto:endSto]

        # Description
        beginDes = '"description":"'
        endDes = '",'
        startDes = script.find(beginDes) + len(beginDes)
        endDes = script.find(endDes, startDes)
        description = script[startDes:endDes]
        newDes = description.replace('\\','').replace('u003cp','').replace('u003en','').replace('003c/p','').replace('u003e','').replace('u003cdiv','').replace('class="item-info"','').replace('class="item-excerpt trunc"','').replace('itemprop="description"','').replace('data-height="230"','').replace('u003cspan','').replace('u003c/span','').replace('u003cbr','').replace('u003c/div','').replace('class="item-tools"','').replace('class="checkout-tools"','').replace('class="price-info-wrap"','').replace('class="item-info-wrap"','').replace('u003c/emu','').replace('class="product_description"','').replace('u003c/i','').replace('u003c/li','').replace('u003cli','').replace('\xa0','').replace('data-mce-fragment="1"','').replace('class="block block--dark"','').replace('class="page"','').replace('class="l-container"','').replace('class="g-row"','').replace('class="page__content"','').replace('class="g-col g-span8"','').replace('class="book"','').replace('class="flex-reorder"','').replace('class="book__about flex-reorder-1"','').replace('class="accordion accordion--mobile is-active"','').replace('data-attach="App.Accordion"','').replace('data-accordion-options=\'{"mobileOnly": "true"}\'','').replace('class="accordion__content"','').replace('class="hb-content hb-content-book-detail"','').replace('class="hb-content-text hb-content-text-book-detail"','').replace('class="description bottom show-all"','').replace('u003cul','').replace('u003c/ul','').replace('class="container__content u-separator-right"u003csection','').replace('class="component','').replace('class="post-text"u003csection','').replace('uu003c/sectionu003c/section','').replace('u003c/section','').replace('u003ci','').replace('class="product-essential col1-set"','').replace('class="product-collateral"','').replace('id="ja-tab-products"','').replace('class="ja-tab-content"','').replace('id="ja-tab-description"','').replace('class="box-collateral box-description"','').replace('class="std"','').replace('                                                                                                          u003cstrongu003c/strong   u003csection id="comp-kkfbw8un1" data-testid="columns" class="_3BQmz" id="comp-kkfbw8un3" class="_1HpZ_" data-mesh-id="comp-kkfbw8un3inlineContent" data-testid="inline-content" class="" data-mesh-id="comp-kkfbw8un3inlineContent-gridContainer" data-testid="mesh-container-content" id="comp-kkfbw8un5" class="_1Z_nJ animating-screenIn-exit" data-testid="richTextElement" data-angle="0" data-angle-style-location="style"','').replace('u                                                                                                          u003cstrongu003c/strong   u003csection id="comp-kkfbw8un1" class="_3BQmz" data-testid="columns" class="_1HpZ_" id="comp-kkfbw8un3" class="" data-testid="inline-content" data-mesh-id="comp-kkfbw8un3inlineContent" data-testid="mesh-container-content" data-mesh-id="comp-kkfbw8un3inlineContent-gridContainer" data-angle-style-location="style" data-angle="0" data-testid="richTextElement" class="_1Z_nJ animating-screenIn-exit" id="comp-kkfbw8un5"                                                                                                                                                                                                                                                                                                     ','').replace(' u      data-hook="content-wrapper" class="_3cRjW"','').replace('u003c/strongu','').replace('uu003cstrong','').replace('u class="col-sm-6" class="tab-content" class="tab-pane active" id="tab-description"           ','').replace('','').replace('','').replace('','')

        # Images
        beginImg = '"image","src":"'
        endImg = '","width"'
        startImg = script.find(beginImg) + len(beginImg)
        endImg = script.find(endImg, startImg)
        images = script[startImg:endImg]
        newImages = images.replace('\\', '')

        productObject = {
            "sku": sku,
            "name": name,
            "price": price,
            "stockLevel": stockLevel,
            "images": newImages,
            "categories": "books",
            "vendor": "secretbook@live.com",
            "description": newDes,
            # "relatedProducts": relatedList
        }
        items.append(productObject)
        print(productObject)
        driver.back()
        time.sleep(1)
        # try:
        #     WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME,'shopify-section header-section')))
        # except TimeoutException:
        #     print('Loading exceeds delay time')
        #     break
        # else:
        #     soup = BeautifulSoup(driver.page_source, 'html.parser')
        #     prodCont = soup.find('div',{'class': 'grid-uniform'})
        #     products = prodCont.find_all('div',{'class': 'product-grid-item'})
        #     print(len(products))

# convert to excel file
df_data = pd.DataFrame(items)
df_data.to_excel("products-secretbookstore5.xlsx", index=False)

driver.quit()


