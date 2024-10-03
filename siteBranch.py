from flask import Flask, render_template
from pprint import pprint



app = Flask(__name__)
@app.route("/")
def news_text():
    with open("data.json") as f:
        a = f.read()

        text = a
        template = '/news.html'
    return render_template(template,text=text)

if __name__ == "__main__":

    app.run()