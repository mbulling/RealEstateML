from flask import Flask, render_template, Blueprint, request
from os import path
import requests
from bs4 import BeautifulSoup
import string
import os
import pickle

import numpy as np
import pandas as pd
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import make_scorer
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV


def create_app():
    app = Flask(__name__)
    
    return app

data = pd.read_csv('https://raw.githubusercontent.com/RubixML/Housing/master/dataset.csv')
prices =  pd.read_csv('https://raw.githubusercontent.com/RubixML/Housing/master/dataset.csv')['SalePrice']
features =  pd.read_csv('https://raw.githubusercontent.com/RubixML/Housing/master/dataset.csv', usecols=['GrLivArea', 'FullBath', 'BedroomAbvGr'])

X_train, X_test, y_train, y_test = train_test_split(features,prices,test_size=0.2)


def performance_metric(y_true, y_predict):
    return r2_score(y_true,y_predict)

def fit_model(X, y):
    cv_sets = ShuffleSplit(X.shape[0], test_size = 0.20, random_state = 0)
    regressor = DecisionTreeRegressor()
    params = {'max_depth':range(1,11)}
    scoring_fnc = make_scorer(performance_metric)
    grid = GridSearchCV(estimator=regressor, param_grid=params, scoring=scoring_fnc, cv=cv_sets)
    grid = grid.fit(X, y)
    return grid.best_estimator_


reg = fit_model(X_train, y_train)

def getResult(list):
    list = list
    return reg.predict([list])

def retrieveHTML(address):
    """
    address type: address
    rtype: soup object
    """
    def zillowify(address):
        """
        address type: address in format "street,city,state"
        rtype: url string corresponding to address on homesnap
        """

        codes = { "alabama": "al", 
            "alaska": "ak", 
            "arizona": "az", "arkansas": "ar",
            "california": "ca", 
            "colorado": "co",
            "connecticut": "ct",
            "delaware": "de",
            "florida": "fl",
            "georgia": "ga",
            "hawaii": "hi",
            "idaho": "id",
            "illinois": "il",
            "indiana": "in",
            "iowa": "ia",
            "kansas": "ks",
            "kentucky": "ky",
            "louisiana": "la",
            "maine": "me",
            "maryland": "md",
            "massachusetts": "ma",
            "michigan": "mi",
            "minnesota": "mn",
            "mississippi": "ms",
            "missouri": "mo",
            "montana": "mt",
            "nebraska": "ne",
            "nevada": "nv",
            "new hampshire": "nh",
            "new jersey": "nj",
            "new mexico": "nm",
            "new york": "ny",
            "north carolina": "nc",
            "north dakota": "nd",
            "ohio": "oh",
            "oklahoma": "ok",
            "oregon": "or",
            "pennsylvania": "pa",
            "rhode island": "ri",
            "south carolina": "sc",
            "south dakota": "sd",
            "tennessee": "tn",
            "texas": "tx",
            "utah": "ut",
            "vermont": "vt",
            "virginia": "va",
            "washington": "wa",
            "west virginia": "wv",
            "wisconsin": "wi",
            "wyoming": "wy",
            "district of columbia": "dc",
            "american samoa": "as",
            "guam": "gu",
            "northern mariana islands": "mp",
            "puerto rico": "pr",
            "united states minor outlying islands": "um",
            "u.s. virgin islands": "vi"
        }        
        address = address.lower()
        for n in codes:
            if n in address:
                address  = address.replace(n, codes[n])

        comma1 = address.index(', ')
        comma2 = address.index(', ', comma1 + 1)

        street = address[:comma1]
        city = address[comma1+2:comma2]
        state = address[comma2+2:]

        street = street.translate(street.maketrans(' ', '-'))
        city = city.translate(city.maketrans(' ', '-'))
        print('https://www.homesnap.com/{state}/{city}/{street}'.format(street=street,city=city,state=state))
        return 'https://www.homesnap.com/{state}/{city}/{street}'.format(street=street,city=city,state=state)

    url = zillowify(address)
    res = requests.get(url).text
    return res


def generateInfo(html):
    """
    html type: string
    rtype: dictionary with 'bed', 'bath', 'sqft' as key values
    """
    def search(html, keyword):
        """
        keyword type: string
        rtype: most recent previous occurrence of a number
        """
        word = ''
        page = []
        for i, char in enumerate(html):
            if char == " ":
                page.append(word)
                word = ''
            else:
                word += char

        for i, w in enumerate(page):
            if not w.isalnum():
                page[i] = w.translate(str.maketrans('', '', string.punctuation))

        index = -1
        for i, w in enumerate(page):
            if w == keyword:
                index = i

        if index != -1:
            while index >= 0:
                if page[index].isnumeric():
                    return page[index]
                index -= 1
        return -1

    dict = {}
    dict['bed'] = search(html, 'bed')
    dict['bath'] = search(html, 'bath')
    dict['sqft'] = search(html, 'Sq')

    return dict

def scrape(address):
    html = retrieveHTML(address)
    info = generateInfo(html)
    return info


def addCommas(str):
    """
    1000 -> 1,000
    1000000 -> 1,000,000
    """
    if len(str) < 4:
        return str
    rev = str[::-1]
    res = ''
    for i, char in enumerate(rev):
        if i % 3 == 0 and i != 0:
            res =  res + ',' + char
        else:
            res += char
    
    return res[::-1]

        


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        addr = request.form.get('addr')
        m = scrape(addr)
        n = int(getResult([m['sqft'], m['bed'], m['bath']]))
        h = addCommas(str(n))
        if m['sqft'] == -1 or m['bed'] == -1 or m['bath'] == -1:
            m['sqft'] = -1
            m['bath'] = -1
            m['bed'] = -1
            return render_template("predict.html", test=0, test2=m, add="Sorry, That Address Does Not Exist In Our Database")
        return render_template("predict.html", test=h, test2=m, add=addr)
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")
    

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    return render_template("predict.html")








