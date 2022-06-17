import pickle

def getResult(list):
    loaded_model = pickle.load(open('real_estate_model.sav', 'rb'))
    result = loaded_model.predict([[6000,2,3]])
    return result 