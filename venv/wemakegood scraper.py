import math
import re
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.message import EmailMessage
from email.mime.application import MIMEApplication
import io
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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

options = Options()
options.headless = True
options.add_argument('--no-sandbox')
# driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)
driver = webdriver.Chrome("C:/Users/16104/PycharmProjects/electraLocoify/Web Drivers/chromedriver.exe", options=options)
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
        for p in range(2):
        # for p in range(len(products)):
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


print("total products: ", prodAmount)
print("total products in list", totalAdded)
# convert to excel file
df_data = pd.DataFrame(productObjects)
df_data.to_excel("products-wemakegoodcloud.xlsx", index=False)

def export_excel(df):
  with io.BytesIO() as buffer:
    writer = pd.ExcelWriter(buffer)
    df.to_excel(writer)
    writer.save()
    return buffer.getvalue()


SEND_FROM = 'dsuhupcs@gmail.com'
SEND_PASS = "Danielsuh1$"
EXPORTERS = {'products-wemakegoodcloud.xlsx': export_excel}

def send_dataframe(send_to, subject, body, df):
  multipart = MIMEMultipart()
  multipart['From'] = SEND_FROM
  multipart['To'] = send_to
  multipart['Subject'] = subject
  for filename in EXPORTERS:
    attachment = MIMEApplication(EXPORTERS[filename](df))
    attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    multipart.attach(attachment)
  multipart.attach(MIMEText(body, 'html'))
  s = smtplib.SMTP('smtp.gmail.com', 587)
  s.starttls() #enable security
  s.login(SEND_FROM, SEND_PASS) #login with mail_id and password
  s.sendmail(SEND_FROM, send_to, multipart.as_string())
  s.quit()
send_dataframe('dsuhupcs@gmail.com',"WeMakeGood Scraper",'{}{}{}{}'.format("total products: ", prodAmount,"\ntotal products in list: ", totalAdded ), df_data)
print('Mail Sent')
driver.close()
driver.quit

