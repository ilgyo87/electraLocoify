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
import pandas as pd
import io
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

productObjects = []
productObject = {
    "sku": 'sku',
    "name": 'name',
    "price": 'price',
    "categories": 'categories',
    "stockLevel": 'stockLevel',
    "images": 'images',
    "description": 'description',
    "variantSKU": '',
    "Type (field:class)": '',
    "variantPrice": '',
    "variantQuantity": '',
    "vendor": "info@wemakegood.ie",
}
productObjects.append(productObject)
df_data = pd.DataFrame(productObjects)
excelFile = df_data.to_excel("products-wemakegoodcloud.xlsx", index=False)

def export_excel(df):
  with io.BytesIO() as buffer:
    writer = pd.ExcelWriter(buffer)
    df.to_excel(writer)
    writer.save()
    return buffer.getvalue()


SEND_FROM = 'dsuhupcs@gmail.com'
SEND_PASS = "Danielsuh1$"
EXPORTERS = {'dataframe.xlsx': export_excel}

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
send_dataframe('dsuhupcs@gmail.com',"Test","whatever", df_data)
print('Mail Sent')