
import sqlite3
from flask import Flask, render_template, request
import os



app = Flask(__name__)
connection = sqlite3.connect("parced_news.db", check_same_thread=False)
cursor = connection.cursor()


def get_articles_from_db():
    cursor.execute("select id, news_title, news_text, university_name, news_date "
                   "from Posts where deleted = 0 ")
    data = cursor.fetchall()
    return [{"id": str(ids), "title": title, "text": text,  "name": name, "date": date} for ids, title, text, name, date in data]


def download_images_from_db():
    cursor.execute("SELECT id, news_img from Posts ")
    record = cursor.fetchall()
    for row in record:
        photo = row[1]
        photo_id = str(row[0])
        photo_path = os.path.join("static", "temp", photo_id + ".jpeg")
        with open(photo_path, 'wb') as file:
            file.write(photo)


@app.route("/")
@app.route("/homepage")
def homepage():
    articles = get_articles_from_db()
    return render_template("homepage.html", articles=articles)


@app.route("/about")
def about():
    return render_template("about.html")





if __name__ == "__main__":
    download_images_from_db()
    app.run(port=1000, debug=True)


















