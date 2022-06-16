import requests
from bs4 import BeautifulSoup



def zillowify(address):
    pass



def soupify(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup


