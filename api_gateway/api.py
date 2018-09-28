from flask import Flask, render_template, url_for
from flask_pymongo import PyMongo

from config import *

app = Flask(__name__)
app.config.from_object('config')
data = PyMongo(app, config_prefix='MONGO')
#requests = Requests(mongo=data)

@app.route("/api", methods=["GET"])
def api():
    return "Welcome to our API!"

if __name__ == '__main__':
    app.run(port=3001, debug=True)
