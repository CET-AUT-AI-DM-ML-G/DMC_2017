# 2. Import libraries and modules
import numpy as np
import pandas as pd
import math
import csv
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.externals import joblib

# 3. Load red wine data.
dataset_url = 'c4.csv'
data = pd.read_csv (dataset_url, sep=',').drop ('id', axis=1)

#print data.isnull().any()

#4. Split data into training and test sets
y = data.avg5
X = data.drop('avg5' , axis=1)#.drop('id' , axis=1)#.drop('tavg5' , axis=1)

# y = data.quality
# X = data.drop('quality', axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.5,
                                                    random_state=123,
                                                    )

# 5. Declare data preprocessing steps
pipeline = make_pipeline(preprocessing.StandardScaler(),
                         RandomForestRegressor(n_estimators=100))

# 6. Declare hyperparameters to tune
hyperparameters = {'randomforestregressor__max_features': ['auto', 'sqrt', 'log2'],
                   'randomforestregressor__max_depth': [None, 5, 3, 1]}

# 7. Tune model using cross-validation pipeline
clf = GridSearchCV(pipeline, hyperparameters, cv=10)

clf.fit(X_train, y_train)

# 8. Refit on the entire training set
# No additional code needed if clf.refit == True (default is True)

# 9. Evaluate model pipeline on test data
pred = clf.predict(X_test)
pred2=clf.predict(X_train)

# print X_test
# print pred


print r2_score(y_test, pred)
print math.sqrt(mean_squared_error(y_test, pred))
print math.sqrt(mean_squared_error(y_train, pred2))

# 10. Save model for future use
joblib.dump(clf, 'rf_regressor.pkl')
# To load: clf2 = joblib.load('rf_regressor.pkl')
# with open ('forest_out.csv', 'w') as name:
#     fieldnames = ['id',
#                   'avg1',
#                   'avg2',
#                   'avg3',
#                   'avg4', 'avg5'
#                   ]
#
#     writer = csv.DictWriter (name, fieldnames=fieldnames)
#     writer.writeheader ()
#
#     for i in range(len(pred)):
#         writer.writerow ({'id': id,
#                           'avg1': data.avg1.values[i],
#                           'avg3': data.avg2.values[i],
#                           'avg4': data.avg3.values[i],
#                           'avg5': data.avg4.values[i],
#                           'avg6': pred[i]
#                           })
