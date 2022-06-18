from flask import Flask, render_template, request, redirect
from os import path
import string
import os
from .views import scrape
from .views import getResult
from .views import addCommas

app = Flask(__name__)

def create_app():

    return app

        
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        addr = request.form.get('addr')
        m = scrape(addr)
        n = int(getResult([m['sqft'], m['bed'], m['bath']]))
        h = addCommas(str(n))
        # if m['sqft'] == -1 or m['bed'] == -1 or m['bath'] == -1:
        #     m['sqft'] = -1
        #     m['bath'] = -1
        #     m['bed'] = -1
        #     return render_template("predict.html", test=0, test2=m, add="Sorry, That Address Does Not Exist In Our Database")
        return render_template("predict.html", test=h, test2=m, add=addr)
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")
    

@app.route('/predict')
def predict():
    return render_template("predict.html")

@app.route('/home', methods=['GET', 'POST'])
def red():
    return redirect('/')










