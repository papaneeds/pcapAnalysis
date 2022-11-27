# This python file loads a model and then reads in a dataset and classifies
# the data in the dataset

import sys
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix

def applyModels(models, X, y):

    for key in models.keys():
        print("Applying model " + key)

        # all parameters not specified are set to their defaults
        predictions = models[key].predict(X)

        print("predictions=", predictions)

        TN, FP, FN, TP = confusion_matrix(y, predictions).ravel()
        #result = loaded_model.score(X_test, Y_test)

        print('True Positive(TP)  = ', TP)
        print('False Positive(FP) = ', FP)
        print('True Negative(TN)  = ', TN)
        print('False Negative(FN) = ', FN)

        accuracyScore =  (TP + TN) / (TP + FP + TN + FN)
        precisionScore = TP/(TP + FP)
        recallScore = TP/(TP + FN)

def applyModel(model, X, y):

    print("Applying single model ")

    # all parameters not specified are set to their defaults
    predictions = model.predict(X)

    print("predictions=", predictions)

    TN, FP, FN, TP = confusion_matrix(y, predictions).ravel()
    #result = loaded_model.score(X_test, Y_test)

    print('True Positive(TP)  = ', TP)
    print('False Positive(FP) = ', FP)
    print('True Negative(TN)  = ', TN)
    print('False Negative(FN) = ', FN)

    accuracyScore =  (TP + TN) / (TP + FP + TN + FN)
    precisionScore = TP/(TP + FP)
    recallScore = TP/(TP + FN)


[program, modelFileName, testDatasetFilename] = sys.argv

# load the model from disk
#models = pickle.load(open(modelFileName, 'rb'))
model = pickle.load(open(modelFileName, 'rb'))

# load the test dataset from disk
dataSet = pickle.load(open(testDatasetFilename, 'rb'))

X = dataSet['data']
y = dataSet['target']

print("X=", X, X.shape)
print("y=", y, y.shape)

ss = StandardScaler()
X = ss.fit_transform(X)

#applyModels(models, X, y)

applyModel(model, X, y)

