import random

import requests
from bs4 import BeautifulSoup
import schedule
import time
from datetime import datetime
import sqlite3
import warnings
from bs4 import GuessedAtParserWarning

warnings.filterwarnings('ignore', category=GuessedAtParserWarning)
# url = "https://mtuci.ru/about_the_university/news/"

PATTERN_OUT = "%d.%m.%y"
date = datetime.strftime(datetime.today().date(), PATTERN_OUT)
PATTERN_OUT2 = "%d"
day = datetime.strftime(datetime.today().date(), PATTERN_OUT2)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'}


def NewsDump(currentArticle, title, university_name, img):
    connection = sqlite3.connect('parced_news.db')
    cursor = connection.cursor()
    p = ''
    for i in currentArticle.findAll('p'):
        if i.text.strip:
            p += '\n' + i.text.strip()
    cursor.execute("select news_title from Posts;")
    News_name = cursor.fetchall()
    connection.commit()
    # print(News_name)

    for i in range(len(News_name)):
        if News_name[i][0].strip() == title:
            p = ''
    if p != '':
        cursor.execute(
            'INSERT INTO Posts (news_title, news_text, university_name, news_date, news_img, deleted) '
            'VALUES (?, ?, ?, ?, ?, ?);',
            (title, p, university_name, str(date), img, '0'))
        connection.commit()
    connection.close()


def MTUCI_check():
    url = 'https://mtuci.ru/about_the_university/news/'
    startPagebs = BeautifulSoup(requests.get(url, headers=headers).text, 'lxml')
    block = startPagebs.findAll('div', class_="news-list__item")
    block.append(startPagebs.find('div', class_="news-list__first-item"))
    university_name = 'МТУСИ'

    # connection = sqlite3.connect('parced_news.db')
    # cursor = connection.cursor()

    for item in block:
        if item.find('p', class_="meta").text.strip() == date:
            currentNew_url = "https://mtuci.ru" + item.find('a').attrs['href']
            time.sleep(random.randint(3, 8))
            currentArticle = BeautifulSoup(requests.get(currentNew_url, headers=headers).text, "lxml").find('div',
                                                                                                            class_="news-single")
            img_src = "https://mtuci.ru" + item.find('img').attrs['src']
            time.sleep(random.randint(3, 8))
            img = requests.get(img_src, headers=headers).content
            title = str(currentArticle.find('h2', class_="text-center").text.strip())
            print(title)
            NewsDump(currentArticle, title, university_name, img)
    #         p = ''
    #         for i in currentArticle.findAll('p'):
    #             if i.text.strip:
    #                 p += '\n' + i.text.strip()
    #         cursor.execute("select news_title from Posts;")
    #         News_name = cursor.fetchall()
    #         connection.commit()
    #         # print(News_name)
    #
    #         for i in range(len(News_name)):
    #             if News_name[i][0].strip() == title:
    #                 p = ''
    #         if p != '':
    #             cursor.execute(
    #                 'INSERT INTO Posts (news_title, news_text, university_name, news_date, news_img, deleted) '
    #                 'VALUES (?, ?, ?, ?, ?, ?);',
    #                 (title, p, university_name, str(date), img, '0'))
    #             connection.commit()
    # connection.close()


def MAI_check():
    url = "https://mai.ru/press/news/"
    startPagebs = BeautifulSoup(requests.get(url, headers=headers).text, "lxml")
    block = startPagebs.findAll('div', class_="col-sm-6 col-lg-6 mb-3 mb-lg-5")
    university_name = 'МАИ'
    # connection = sqlite3.connect('parced_news.db')
    # cursor = connection.cursor()

    for item in block:
        if int(str(item.find('span', class_="badge bg-primary rounded-pill fw-normal px-2").text[:2]).strip()) == int(
                day):
            currentNew_url = url + item.find('a', class_="card h-100 card-transition").attrs['href']
            time.sleep(random.randint(3, 8))
            currentArticle = BeautifulSoup(requests.get(currentNew_url, headers=headers).text, "lxml").find('article',
                                                                                                            itemprop="articleBody")
            img_src = 'https://mai.ru/' + item.find('img', class_="card-img-top").attrs['src']
            time.sleep(random.randint(3, 8))
            img = requests.get(img_src, headers=headers).content
            title = currentArticle.find('h1').text.strip()
            print(title)
            NewsDump(currentArticle,title,university_name,img)


def Baum_check():
    url = "https://kf.bmstu.ru/news"
    startPagebs = BeautifulSoup(requests.get(url, headers=headers).text, "lxml")
    block = startPagebs.findAll('div', class_="l-news-list-col col-12 col-md-4")
    university_name = 'МГТУ им. Баумана'
    for item in block:
        if int(item.find('span', class_="l-news-date").find('span').text) == int(day):
            currentNew_url = 'https://kf.bmstu.ru' + item.find('a', class_="l-news-element").attrs['href']
            time.sleep(random.randint(3, 8))
            currentArticle = BeautifulSoup(requests.get(currentNew_url, headers=headers).text, "lxml").find('div', class_ ="l-typography-text")

            title = item.find('span', class_="l-news-title").text
            print(title)
            img_src = 'https://kf.bmstu.ru/' + item.find('img').attrs['src']
            time.sleep(random.randint(3, 8))
            img = requests.get(img_src, headers=headers).content
            NewsDump(currentArticle, title, university_name, img)


def MIREA_check():
    url = 'https://www.mirea.ru/news/'
    startPagebs = BeautifulSoup(requests.get(url, headers=headers).text, 'lxml')
    block = startPagebs.findAll('div', class_="uk-card uk-card-default")
    university_name = 'МИРЭА'
    for item in block:
        # print(date[:5])
        if item.find('div', class_="uk-margin-small-bottom uk-text-small").text.strip()[:5] == date[:5]:
            currentNew_url = "https://www.mirea.ru" + item.find('a').attrs['href']
            time.sleep(random.randint(3,8))
            newpage =  BeautifulSoup(requests.get(currentNew_url, headers=headers).text, 'lxml')
            currentArticle =newpage.find('div', class_="news-item-text uk-margin-bottom")
            title = item.find('a', class_="uk-link-reset").text
            print(title)
            img_src = 'https://www.mirea.ru' + newpage.find('div', class_="uk-card uk-card-default").find('img').attrs['src']
            img = requests.get(img_src, headers=headers).content
            NewsDump(currentArticle, title, university_name, img)








MTUCI_check()
MAI_check()
Baum_check()
MIREA_check()


# schedule.every().hour.do(news_check)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
