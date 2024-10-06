import json
import sqlite3
from pprint import pprint
import time
from flask import Flask, render_template





app = Flask(__name__)


def json_handler():
    connection = sqlite3.connect('parced_news.db')
    cursor = connection.cursor()
    with open("data.json") as f:
        all_news = f.read()
        all_news = json.loads(all_news)
        each_news = []
        #Согласуем id записей с базой данных
        id = cursor.execute("select id from Posts ORDER by id desc LIMIT 0,1;")
        last_id = cursor.fetchall()
        connection.commit()

        if last_id != 0:
            try:
                news_id = last_id[0][0]+1
            except IndexError:
                news_id = 0
        #Проверяем, существует ли уже такая запись в бд
        titles = cursor.execute("select news_title from Posts;")
        news_titles = cursor.fetchall()
        connection.commit()
        titles = []
        for name in news_titles:
            titles.append(name[0])

        for title in all_news:
            each_news.append(
                {'news_title': title,
                 'news_text': " ".join(all_news[title]),
                 'id': news_id
                 }
            )
            news_id+=1

        for sql_t in titles:
            for i in range(len(each_news)-1):
                if sql_t == each_news[i]['news_title']:
                    each_news.pop(i)


    return each_news

def create_new_post_in_db():
    connection = sqlite3.connect('parced_news.db')
    cursor = connection.cursor()
    news = json_handler()

    for i in range(len(news)-1):
        print(news[i]["id"])
        cursor.execute('INSERT INTO Posts (id, news_title, news_text) VALUES (?, ?, ?);', (news[i]["id"],news[i]["news_title"], news[i]["news_text"]))
        connection.commit()
    connection.close()

def sum_of_news():
    connection = sqlite3.connect('parced_news.db')
    cursor = connection.cursor()
    news_sum_db = cursor.execute("select count(*) from Posts;")
    news_sum = cursor.fetchall()[0][0]
    connection.commit()
    return news_sum



def get_articles():
    connection = sqlite3.connect('parced_news.db')
    cursor = connection.cursor()
    cursor.execute("select news_title, news_text from Posts")
    articles = cursor.fetchall()
    connection.close()
    return [{'title': title, 'text': text} for title, text in articles]

@app.route("/")
@app.route("/homepage")
def homepage():
    articles = get_articles()
    return render_template("homepage.html", articles=articles)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    print(get_articles())
    app.run(debug=True)







