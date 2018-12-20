from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
rom slackclient import SlackClient
from flask import Flask, request, make_response, render_template


options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(r'C:\Users\student\Desktop\chromedriver.exe')
driver.get("https://finance.naver.com/")
searchText = driver.find_element_by_id("stock_items")
searchText.send_keys("삼성바이오로직스")
searchText.send_keys(Keys.ARROW_DOWN)
searchText.send_keys(Keys.RETURN)

time.sleep(1)
code=driver.current_url

url = code
keywords = []

# URL 주소에 있는 HTML 코드를 soup에 저장합니다.
soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
name = soup.find_all("div", class_="inner_area_left")

for i in name:
    name = i.get_text().strip()

keywords = name.split("\n")
print(keywords)

source=driver.page_source
soup = BeautifulSoup(source, "html.parser")

for i in soup.find_all("h4", class_="ellipsis_title2"):
    print(i.get_text())
