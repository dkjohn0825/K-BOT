# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.request
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template

app = Flask(__name__)

slack_token = "xoxb-507694811781-507328839316-rae0R7TRfnJRa1Jui0cFpxpT"
slack_client_id = "507694811781.507392690595"
slack_client_secret = "425568f377e385d1f3b051f0a5c6fd82"
slack_verification = "mA1X8EIb1BxfN9E84nVInEg2"
sc = SlackClient(slack_token)


# 크롤링 함수 구현하기
def _crawl_naver_keywords(text):
    count = 0
    result1 = []
    result2 = []
    text = re.sub(r'<@\S+> ', '', text)
    now = datetime.now()
    now_message="현재시간 : "+str(now.hour)+"시 " +str(now.minute)+"분 ("+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+")"

    url = "https://finance.naver.com/sise/sise_market_sum.nhn"
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    name = soup.find_all("a", class_="tltle")
    list = soup.find_all("td", class_="number")
    info = []
    for l in list:
        info.append(l.get_text().strip())

    price = []
    point = []
    percent = []

    keywords = []
    keywords2 = []

    if now.hour<9 and now.hour>=0:
        return now_message+"\n"+"🕒개장 시간이 아니에요~"
    else:
        if "어때" in text:
            texts=[]
            texts=text.split(" ")
            opinion(texts[0])

        elif "떡상" in text or "ㄸㅅ" in text or "가즈아" in text:
            for i in range(0, 50):
                if info[10 * i + 2][0] == "+":
                    keywords.append(
                        str(i + 1) + "위 : " + name[i].get_text().strip() + " / " + info[10 * i] + " ( 🔺 " + info[
                            10 * i + 1] + ")")
                    count += 1
                    if count == 10:
                        break
            return u'🧚가즈아~ 국내시총 Top 50 중 떡상종목(최대 10개)\n\n' + u'\n'.join(keywords)

        elif "떡락" in text or "ㄸㄹ" in text or "존버" in text:
            for i in range(0, 50):
                if info[10 * i + 2][0] == "-":
                    keywords2.append(
                        str(i + 1) + "위 : " + name[i].get_text().strip() + " / " + info[10 * i] + "( 🔻 " + info[
                            10 * i + 1] + ")")
                    count += 1
                    if count == 10:
                        break

            return u'🧟‍♂존버가즈아~ 국내시총 Top 50 중 떡락종목(최대 10개)\n\n' + u'\n'.join(keywords2)
        elif "뉴스" in text or "코스피" in text or "코스닥" in text:
            kos = []
            url = "https://finance.naver.com/news/"
            soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
            name = soup.find_all("div", class_="inner_area_left")

            for i in name:
                name=i.get_text().strip()

            kos = name.split("\n")

            kos_string = "코스피 : " + kos[3] + "(" + kos[4] + "), 코스닥 : " + kos[6] + "(" + kos[7] + "), 선물 : " + kos[
                9] + "(" + kos[10] + ")\n"+kos[0]+"\n\n"+kos[19]+"\n"+kos[23]+"\n"+kos[26]+"\n"

            return kos_string

        else:
            return now_message+u'\n\n- 💶챗봇주요 기능💶 - \n ☝떡상 (국내시총 - 떡상한 종목을 보여줍니다.)\n'+'✌떡락 (국내시총 - 떡상한 종목을 보여줍니다.)\n👌뉴스(주식 주요 뉴스 &코스피 &코스닥 정보를 보여줍니다.)\n'

def opinion(text):
    opinions=[]
    opinion_result=""
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(r'C:\Users\student\Desktop\chromedriver.exe')
    driver.get("https://finance.naver.com/")
    searchText = driver.find_element_by_id("stock_items")
    searchText.send_keys(text)
    searchText.send_keys(Keys.ARROW_DOWN)
    searchText.send_keys(Keys.RETURN)

    time.sleep(1)
    code = driver.current_url

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


# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])

    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]

        keywords = _crawl_naver_keywords(text)
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=keywords
        )

        return make_response("App mention message has been sent", 200, )

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                                 "application/json"
                                                             })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('127.0.0.1', port=5000)
