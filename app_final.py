
import sqlite3
from flask import Flask, render_template, request



connection = sqlite3.connect("parced_news.db", check_same_thread=False)
cursor = connection.cursor()
connection.row_factory = sqlite3.Row
connection.text_factory = lambda b: b.decode(errors = 'ignore')
app = Flask(__name__)


def get_articles_from_db():
    cursor.execute("select news_title, news_text, news_date, university_name, news_img "
                   "from Posts where deleted = 0 "
                   "order by id"
                   " desc limit 2;")
    data = cursor.fetchall()
    return [{"title": title, "text": text,  "name": name,"date": date, "image": image} for title, text, date, name, image in data]

@app.route("/load_articles", methods=['GET', 'POST'])
def load_articles():
    id = request.args.get('id')
    # Устанавливаем параметр
    cursor.execute("SELECT news_title, news_text, university_name, news_date, news_img, id FROM Posts where id > ? limit 1;",
                   (id,))

    articles = cursor.fetchall()
    return [{
        "id": id_t,
        "title":title,
        "text":text,
        "name":name,
        "image":image,
        "date": date
    }
    for title, text, name,date , image, id_t in articles
    ]


@app.route('/get_ids', methods=['GET', 'POST'])
def get_ids():
    conn = sqlite3.connect('parced_news.db')
    cursor = conn.cursor()

    # Получаем список всех ID из таблицы
    cursor.execute("SELECT id FROM Posts where deleted = 0;")
    ids = [row[0] for row in cursor.fetchall()]

    conn.close()
    return ids


@app.route("/", methods=['GET', 'POST'])
@app.route("/homepage", methods=['GET', 'POST'])
def homepage():
    articles = get_articles_from_db()
    return render_template("homepage.html", articles=articles)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/search", methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        query = request.form['query']
        results = connection.execute('select * from Posts where university_name like ? order by id DESC ;',
                                     ('%' + query + '%',)).fetchall()

    return render_template("search.html", results=results)

if __name__ == "__main__":
    print(get_ids())
    app.run(debug=True, port=1000)
