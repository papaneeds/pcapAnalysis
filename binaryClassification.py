# This program inputs two datasets that have two different classifications and then
# mergest them into a single dataset. 
# It then does a logistic regression binary classification on the datasets
# as outlined in:
# https://www.learndatasci.com/glossary/binary-classification/
# and
# https://towardsdatascience.com/logistic-regression-using-python-sklearn-numpy-mnist-handwriting-recognition-matplotlib-a6b31e2b166a
#

import sys
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

[program, inputFilenameClass1, inputFilenameClass2] = sys.argv

# Read in the datasets and concatenate them

dataSet1 = pickle.load(open(inputFilenameClass1, "rb" ))
dataSet2 = pickle.load(open(inputFilenameClass2, "rb" ))

df1 = dataSet1['data']
df2 = dataSet2['data']

X = pd.concat([df1, df2], axis=0)
print('shape of df1', df1.shape)
print("shape of df2", df2.shape)
print("shape of X", X.shape)

y1 = dataSet1['target']
y2 = dataSet2['target']

y = pd.concat([y1, y2], axis=0)
print(y1.shape, y2.shape, y.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

ss_train = StandardScaler()
X_train = ss_train.fit_transform(X_train)

ss_test = StandardScaler()
X_test = ss_test.fit_transform(X_test)

# all parameters not specified are set to their defaults
model = LogisticRegression()

model.fit(X_train, y_train)

predictions = model.predict(X_test)

cm = confusion_matrix(y_test, predictions)

TN, FP, FN, TP = confusion_matrix(y_test, predictions).ravel()

print('True Positive(TP)  = ', TP)
print('False Positive(FP) = ', FP)
print('True Negative(TN)  = ', TN)
print('False Negative(FN) = ', FN)

accuracy =  (TP + TN) / (TP + FP + TN + FN)

print('Accuracy of the binary classifier = {:0.3f}'.format(accuracy))
