import numpy as np
import pandas as pd
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import make_scorer
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV

%matplotlib inline

DATA_CSV = 'CSV_DATA_SET'

data = pd.read_csv(DATA_CSV)
prices = data['DEPENDENT_VARIABLE']
features = data.drop('DEPENDENT_VARIABLE', axis=1)

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
