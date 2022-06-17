import pickle
import os
import requests

def getResult(list):
    # with open('real_estate_model.sav', 'rb') as myfile:
    #     loaded_model = pickle.load(myfile)
    # with open('real_estate_model.sav', 'r', encoding='utf-8') as file1:
    #     loaded_model = pickle.load(file1)
    with open('real_estate_model.sav', "rb") as file:
        unpickler = pickle.Unpickler(file);
    
    loaded_model = pickle.load(unpickler)
    result = unpickler.predict([[6000,2,3]])
    return result 