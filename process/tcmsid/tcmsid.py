import requests
from lxml import etree
from bs4 import BeautifulSoup
import xml.etree.ElementTree as et
import json
import pandas as pd

# TODO: extract the herb ingreidients
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)

yrl_2 = 'https://tcm.scbdd.com/home/view_category/'
url = 'http://cadd.pharmacy.nankai.edu.cn/yatcm/herb?paramsType=1'
a = requests.get(url)

content = a.text

j = json(content)
parser = MyHTMLParser()
b = parser.feed(content)
root = etree.fromstring(content)
tree = et.parse(content)
html_tag = tree.getroot()
soup = BeautifulSoup(content, 'lxml')

# lxml
for link in soup.find_all("p"):
    print("Inner Text: {}".format(link.text))
    print("Title: {}".format(link.get("title")))
    print("href: {}".format(link.get("href")))
from urllib.request import urlopen
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
url_3 ='http://119.3.41.228:8000/tcmid/ingredient/645/'
url = "http://cadd.pharmacy.nankai.edu.cn/yatcm/herb/514/herb-compound"
with requests.Session() as session:
    session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
    session.get("http://cadd.pharmacy.nankai.edu.cn/yatcm/herb/514/herb-compound")

    response = session.get(url, headers={"Accept" : "application/json, text/javascript, */*; q=0.01",
                                         "X-Requested-With": "XMLHttpRequest",
                                         "Referer": "http://cadd.pharmacy.nankai.edu.cn",
                                         "Host": "www.cadd.pharmacy.nankai.edu.cn"})
    print(response)

with open('result/YaTCM.html') as a:
    text = a.read()

import re
page = requests.get(url, headers= {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"})
page=page.content
k = re.findall(r'</app-jsme>(.*?)background', text, re.DOTALL)


from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
url = "http://cadd.pharmacy.nankai.edu.cn/yatcm/herb/514/herb-compound"
driver = webdriver.PhantomJS('C:\\hyapp\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
driver.get(url)
try:
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "myDynamicElement"))
    )
finally:
    driver.quit()

element = driver.find_element_by_tag_name('mat-row')
element.get_attribute('innerHTML')
element = driver.find_element_by_class_name('table-section-container')

# This will get the initial html - before javascript
html1 = driver.page_source

# This will get the html after on-load javascript
html2 = driver.execute_script("return document.documentElement.innerHTML;")
