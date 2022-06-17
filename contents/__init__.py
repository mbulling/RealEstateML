from flask import Flask, render_template, Blueprint, request
from os import path

app = Flask(__name__)

def create_app():
    return app

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        addr = request.form.get('addr')
        addr2 = ''
        for c in addr:
            if c != ' ':
                addr2 = addr2 + c
            else:
                addr2 = addr2 + '-'
        addr = addr2
        return render_template("index.html", test=addr)
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")








