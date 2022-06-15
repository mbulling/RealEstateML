from flask import Flask, render_template, Blueprint
from os import path

app = Flask(__name__)

def create_app():
    return app

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")








