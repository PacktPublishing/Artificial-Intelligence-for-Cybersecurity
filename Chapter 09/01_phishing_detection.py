# https://github.com/Asbatel/PhishingDetection2
# Reference from here use the adaboost to do the phishing detection


import sys
import os
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from numpy import array
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt
import pickle
import time
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier


dataFile = sys.argv[1]

with open(dataFile) as f:
    content = f.readlines()
x = []
y = []
for line in content:
    data = line.split(';')
    vector = []
    counter = 0
    for item in data[1].split(','):
        vector.append(int(item))
    x.append(vector)
    y.append(int(data[2]))



totalAccuracy = 0.0
totalPrecision = 0.0
totalSpecificity = 0.0
totalRecall = 0.0

# prepare cross validation
k = 3
kfold = KFold(k, True, 1)

X = np.array(x)
Y = np.array(y)

begin = time.time()

for train_index, test_index in kfold.split(X):
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = Y[train_index], Y[test_index]
    classifier = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1), n_estimators=300)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)  #Predict the response for test dataset


    TP = 0.0
    TN = 0.0
    FP = 0.0
    N = 0.0
    P = 0.0

    for i in range(len(y_test)):
        if y_test[i]:
            P = P + 1
        else:
            N = N + 1
        if y_test[i] == y_pred[i] == 1:
            TP = TP + 1
        if y_test[i] == y_pred[i] == 0:
            TN = TN + 1
        if y_test[i] == 0 and y_pred[i] == 1:
            FP = FP + 1

    Accuracy = (TP + TN) / (P + N)
    Recall = TP / P
    Specificity = TN / N
    Precision = TP / (TP + FP)
    totalAccuracy += Accuracy
    totalRecall += Recall
    totalSpecificity += Specificity
    totalPrecision += Precision
    print ('Accuracy: ' + str(Accuracy))
    print ('Recall: ' + str(Recall))
    print ('Specificity: ' + str(Specificity))
    print ('Precision: ' + str(Precision))

    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

end = time.time()

print ('Total Accuracy: ' + str(totalAccuracy / k))
print ('Total Recall: ' + str(totalRecall / k))
print ('Total Specificity: ' + str(totalSpecificity / k))
print ('Total Precision: ' + str(totalPrecision / k))

print("time", end-begin)

filename = 'phishing_model.sav'
pickle.dump(classifier, open(filename, 'wb'))