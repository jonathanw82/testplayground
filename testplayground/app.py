import os
from flask import Flask, render_template
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", page_title="Home")


@app.route("/speechrecog")
def speechrecog():
    return render_template("speechrecog.html", page_title="speech rec")    


@app.route("/speechtext")
def speechtext():
    return render_template("speechtext.html", page_title="speech Text")  

if __name__ == "__main__":
    app.run(host=os.environ.get('IP', '127.0.0.1'),
            port=int(os.environ.get('PORT', 5000)),
            debug=os.getenv("DEVELOPMENT", False))