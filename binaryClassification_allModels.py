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
from sklearn.metrics import confusion_matrix

models = {}

# Logistic Regression
from sklearn.linear_model import LogisticRegression
models['Logistic Regression'] = LogisticRegression()

# Support Vector Machines
from sklearn.svm import LinearSVC
models['Support Vector Machines'] = LinearSVC()

# Decision Trees
from sklearn.tree import DecisionTreeClassifier
models['Decision Trees'] = DecisionTreeClassifier()

# Random Forest
from sklearn.ensemble import RandomForestClassifier
models['Random Forest'] = RandomForestClassifier()

# Naive Bayes
from sklearn.naive_bayes import GaussianNB
models['Naive Bayes'] = GaussianNB()

# K-Nearest Neighbors
from sklearn.neighbors import KNeighborsClassifier
models['K-Nearest Neighbor'] = KNeighborsClassifier()

from sklearn.metrics import accuracy_score, precision_score, recall_score

accuracy, precision, recall = {}, {}, {}

[program, inputFilenameClass1, inputFilenameClass2, outputModelsFilename] = sys.argv

# Read in the datasets and concatenate them

dataSet1 = pickle.load(open(inputFilenameClass1, "rb" ))
dataSet2 = pickle.load(open(inputFilenameClass2, "rb" ))

df1 = dataSet1['data']
df2 = dataSet2['data']

X = pd.concat([df1, df2], axis=0)
print('shape of df1, df2, X', df1.shape, df2.shape, X.shape)

y1 = dataSet1['target']
y2 = dataSet2['target']

y = pd.concat([y1, y2], axis=0)
print('shape of y1, y2, y', y1.shape, y2.shape, y.shape)

# Split your dataset into 75% training data and 25% test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# Scale your training and testing datasets.
# It is important to scale them separately in order to prevent bleed from one
# dataset into the other.
ss_train = StandardScaler()
X_train = ss_train.fit_transform(X_train)

ss_test = StandardScaler()
X_test = ss_test.fit_transform(X_test)

# Loop through all the models and see what each model predicts
for key in models.keys():
    print("Applying model " + key)

    # all parameters not specified are set to their defaults
    models[key].fit(X_train, y_train)

    predictions = models[key].predict(X_test)

    #cm = confusion_matrix(y_test, predictions)
    #print(cm)

    TN, FP, FN, TP = confusion_matrix(y_test, predictions).ravel()

    print('True Positive(TP)  = ', TP)
    print('False Positive(FP) = ', FP)
    print('True Negative(TN)  = ', TN)
    print('False Negative(FN) = ', FN)

    accuracyScore =  (TP + TN) / (TP + FP + TN + FN)
    precisionScore = TP/(TP + FP)
    recallScore = TP/(TP + FN)

    print('Accuracy= {:0.3f}, Precision= {:0.3f}, Recall= {:0.3f}'.format(accuracyScore, precisionScore, recallScore))

    # calculate metrics
    #accuracy[key] = accuracy_score(predictions, y_test)
    #precision[key] = precision_score(predictions, y_test)
    #recall[key] = recall_score(predictions, y_test)

    #print('Accuracy= {:0.3f}, Precision= {:0.3f}, Recall= {:0.3f}'.format(accuracy[key], precision[key], recall[key]))

# Now, save all the models to file
pickle.dump(models, open(outputModelsFilename, 'wb'))
print('saved models to file=', outputModelsFilename)
