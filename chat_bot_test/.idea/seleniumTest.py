import json
import os
import re
import urllib.request
import time
import itertools

from datetime import datetime
from random import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(r'C:\Users\student\Desktop\chromedriver.exe')
driver.get("https://finance.naver.com/")
searchText = driver.find_element_by_id("stock_items")
searchText.send_keys("셀트")
time.sleep(1)
searchText.send_keys(Keys.ARROW_DOWN)
time.sleep(1)
searchText.send_keys(Keys.RETURN)

time.sleep(1)
code = driver.current_url