import requests
from bs4 import BeautifulSoup
import schedule
import time
import json
from datetime import datetime

from dateutil.utils import today

url = "https://mtuci.ru/about_the_university/news/"

PATTERN_OUT = "%d.%m.%y"
day = datetime.strftime(datetime.today().date(), PATTERN_OUT)


def news_check():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/129.0.0.0 Safari/537.36'}
    startPagebs = BeautifulSoup(requests.get(url, headers=headers).text, "lxml")
    block = startPagebs.findAll('div', class_="news-list__item")
    data_forj = []
    for item in block:
        if item.find('p', class_="meta").text.strip() == day:
            # print(item.find('a').attrs['href'])
            currentNew_url = "https://mtuci.ru" + item.find('a').attrs['href']
            # BeautifulSoup(requests.get(currentNew_url, headers=headers).text, "lxml").find('div', class_="news-single")
            # print(BeautifulSoup(requests.get(currentNew_url, headers=headers).text, "lxml").find('div', class_="news-single").text)
            data_forj.append(BeautifulSoup(requests.get(currentNew_url, headers=headers).text, "lxml").find('div',
                                                                                                            class_="news-single").text)
    try:
        data = json.load(open('data.json'))
    except:
        data = []
    data.append(data_forj)
    with open('data.json', 'w', ) as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


news_check()
