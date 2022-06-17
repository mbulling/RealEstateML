from flask import Flask, render_template, Blueprint, request
from os import path
import requests
from bs4 import BeautifulSoup
import string
import pickle

app = Flask(__name__)

def create_app():
    return app


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
        comma1 = address.index(',')
        comma2 = address.index(',', comma1 + 1)

        street = address[:comma1]
        city = address[comma1+1:comma2]
        state = address[comma2+1:]

        street = street.translate(street.maketrans(' ', '-'))
        city = city.translate(city.maketrans(' ', '-'))
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


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        addr = request.form.get('addr')
        # addr2 = ''
        # for c in addr:
        #     if c != ' ':
        #         addr2 = addr2 + c
        #     else:
        #         addr2 = addr2 + ','
        # addr = addr2
        m = scrape(addr)
        loaded_model = pickle.load(open('real_estate_model.sav', 'rb'))
        result = loaded_model.predict([6000,2,3])
        print(result)
        return render_template("index.html", test=m)
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")
    

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    return render_template("predict.html")








