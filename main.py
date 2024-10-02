import requests
from bs4 import BeautifulSoup
import schedule
import time
import json
from datetime import datetime

url = "https://mtuci.ru/about_the_university/news/"


def news_check():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/129.0.0.0 Safari/537.36'}
    startPagebs = BeautifulSoup(requests.get(url, headers=headers).text, "lxml").contents[1]
    block = startPagebs.findAll('div', class_="news-list__item")
    print(block)


news_check()
