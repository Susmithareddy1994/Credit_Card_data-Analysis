# -*- coding: utf-8 -*-
"""Credit_Card_Data _analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YsU62As_rAaxsU07pa7Mnkj5Livm9bFz
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import joblib
import sys
sys.modules['sklearn.externals.joblib'] = joblib
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import fbeta_score, make_scorer
from sklearn.metrics import precision_score, recall_score, confusion_matrix

df = pd.read_csv("Credit_card.csv")

df.head()

df.shape

df.columns=df.iloc[0]

df = df.iloc[1: , :]

#The values in the dataset are represented in string
type(df.iloc[0]['LIMIT_BAL'])

#Converting the string values to integer
df = df.astype('int')

type(df.iloc[0]['LIMIT_BAL'])

X = df.iloc[:,:-1]
X

y = df.iloc[:,-1]
y

from sklearn.preprocessing import StandardScaler

#Splitting the dataset with train data ad test data
X_train, X_test, y_train, y_test=train_test_split(X,y, test_size=0.20, random_state=25)

X_train.shape,y_train.shape

#std = StandardScaler()
#X_train = std.fit_transform(X_train)
#X_test = std.transform(X_test)

from sklearn.linear_model import LogisticRegression

logreg1 = LogisticRegression(random_state=16)
logreg1.fit(X_train, y_train)
y_pred1 = logreg1.predict(X_test)
from sklearn import metrics
cnf_matrix = metrics.confusion_matrix(y_test, y_pred1)
cnf_matrix

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
print(classification_report(y_test, y_pred1))

from sklearn.metrics import precision_score

Class_1 =  precision_score(y_test, y_pred1, average='macro', labels=[1])
Class_1
Class_0 = precision_score(y_test,y_pred1, average='macro', labels=[0])
Class_0
p = ((Class_0)*100/2 + (Class_1)*100/2)
p

!pip install imbalanced-learn

from collections import Counter
from imblearn.over_sampling import RandomOverSampler
over_sampler = RandomOverSampler(random_state=42)
X_res, y_res = over_sampler.fit_resample(X_train, y_train)
print(f"Training target statistics: {Counter(y_res)}")
print(f"Testing target statistics: {Counter(y_test)}")

logreg = LogisticRegression(random_state=16)
logreg.fit(X_res, y_res)
y_pred = logreg.predict(X_test)
from sklearn import metrics
cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
cnf_matrix

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

Class_1 =  precision_score(y_test, y_pred, average='macro', labels=[1])
Class_1
Class_0 = precision_score(y_test,y_pred, average='macro', labels=[0])
Class_0
p = ((Class_0)*100/2 + (Class_1)*100/2)
p

from sklearn.metrics import make_scorer
!pip install mlxtend 
from mlxtend.feature_selection import SequentialFeatureSelector as sfs
def P(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    n = sum((tn, fp, fn, tp))
    return (((tn/n) * 100) // 2) + (((tp/n) * 100) // 2)
P_scoring = make_scorer(P, greater_is_better=True)

foward_feature_selection=sfs(logreg,k_features=(1,24),forward=True,floating=False, verbose=2,scoring=P_scoring).fit(X_res,y_res)

foward_feature_selection.k_feature_names_

foward_feature_selection.k_score_

x_train_new = X_train[[ 'SEX', 'EDUCATION', 'PAY_0', 'PAY_2', 'PAY_4', 'PAY_5', 'PAY_6', 'PAY_AMT2']]

logr = LogisticRegression()

logr.fit(x_train_new, y_train)

y_prediction=logr.predict(x_train_new)

accuracy_score(y_train, y_prediction)

print(classification_report(y_train,y_prediction))

Class_1 =  precision_score(y_train,y_prediction,average='macro', labels=[1])
Class_1
Class_0 = precision_score(y_train,y_prediction, average='macro', labels=[0])
Class_0
p = ((Class_0)*100/2 + (Class_1)*100/2)
p

from sklearn.ensemble import RandomForestClassifier
f= RandomForestClassifier(max_depth = 15, 
                                n_estimators = 500,
                                bootstrap = True)
f.fit(X_train, y_train)
f_y_pred = f.predict(X_test)
print(f"Random Forest Classification Report on total data")
cm=confusion_matrix(y_test, f_y_pred)
print(cm)
print(classification_report(y_test, f_y_pred), "\n")

Class_1 =  precision_score(y_test, f_y_pred, average='macro', labels=[1])
Class_1
Class_0 = precision_score(y_test,f_y_pred, average='macro', labels=[0])
Class_0
p = ((Class_0)*100/2 + (Class_1)*100/2)
p

from sklearn.metrics import make_scorer
!pip install mlxtend 
from mlxtend.feature_selection import SequentialFeatureSelector as sfs
def P(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    n = sum((tn, fp, fn, tp))
    return (((tn/n) * 100) // 2) + (((tp/n) * 100) // 2)
P_scoring = make_scorer(P, greater_is_better=True)

from sklearn.feature_selection import SelectFromModel

sfm = SelectFromModel(f, threshold=0.15)
sfm.fit(X_train, y_train)
for feature_list_index in sfm.get_support(indices=True):
    print(df.columns[feature_list_index])

X_important_train = sfm.transform(X_train)
X_important_test = sfm.transform(X_test)

clf_important = RandomForestClassifier(n_estimators=10000, random_state=0, n_jobs=-1)
clf_important.fit(X_important_train, y_train)
y_pred = f.predict(X_test)
accuracy_score(y_test, y_pred)

y_important_pred = clf_important.predict(X_important_test)
accuracy_score(y_test, y_important_pred)