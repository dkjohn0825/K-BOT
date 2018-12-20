import urllib.request  # 웹페이지 여는데 이용하는 모듈
from bs4 import BeautifulSoup  # 크롤링 하는데 이용하는 모듈

def main():
    # URL 데이터를 가져올 사이트 url 입력
    url = "https://finance.naver.com/news/"

    keywords = []

    # URL 주소에 있는 HTML 코드를 soup에 저장합니다.
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    name = soup.find_all("div", class_="inner_area_left")


    for i in name:
        name = i.get_text().strip()

    keywords=name.split("\n")
    print(keywords)

if __name__ == "__main__":
    main()
