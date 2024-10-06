import requests
from bs4 import BeautifulSoup
import schedule
import time
import json
from datetime import datetime
from classN import NewsClass
import  sqlite3


url = "https://mtuci.ru/about_the_university/news/"


PATTERN_OUT = "%d.%m.%y"
day = datetime.strftime(datetime.today().date(), PATTERN_OUT)


def news_check():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/129.0.0.0 Safari/537.36'}
    startPagebs = BeautifulSoup(requests.get(url, headers=headers).text, "lxml")
    block = startPagebs.findAll('div', class_="news-list__item")
    data_forj = NewsClass(None, None, None, None, None)
    for item in block:
        if item.find('p', class_="meta").text.strip() == day:
            currentNew_url = "https://mtuci.ru" + item.find('a').attrs['href']
            currentArticle = BeautifulSoup(requests.get(currentNew_url, headers=headers).text, "lxml").find('div',
                                                                                                            class_="news-single")
            p = []
            for i in currentArticle.findAll('p'):
                p.append(i.text.strip())
            if p:
                data_forj.header = str(currentArticle.find('h2', class_="text-center").text.strip())
                data_forj.text = p
                data_forj.date = day
                data_forj.university = 'МТУСИ'
                data_forj.image = 'здесь будет картинка'

                # data_forj[str(currentArticle.find('h2', class_="text-center").text.strip())] = p

    with open('data.json', 'w', ) as file:
        json.dump(data_forj, file, indent=4, ensure_ascii=False)

news_check()
# schedule.every().hour.do(news_check)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
