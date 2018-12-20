from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup



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

url = code.replace('main', 'board')

driver.quit()
soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
for ul in soup.find_all("td", class_="title"):
    opinions.append(ul.get_text())

for i in range(0, len(opinions)):
    print(opinions[i].find('a')['title'])


for i in range(0 , len(opinions)):
    opinion_result+=opinions[i]


return opinion_result
