import pandas as pd 
import numpy as np 
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt 
from get_dataframe import *
import math


def trainSVR(X, Y, kernelChoice, C=1, degreeChoice=3, gammaChoice=1e-5):
    if kernelChoice == "linear":
        mySVR = SVR(kernel = kernelChoice, C = 1)
    elif kernelChoice == "poly":
        mySVR = SVR(kernel = kernelChoice, C = 1, degree = degreeChoice)
    elif kernelChoice == "rbf": 
        mySVR = SVR(kernel = kernelChoice, C = 100, gamma = gammaChoice)
    else:
        print("ERROR in trainSVR, do not recognize the following svr kernel choice: {}", kernelChoice)

    return mySVR.fit(X, Y)

def splitCompanyData(df, trainPercentage, labelName):
    trainDays = np.random.rand(len(df)) < trainPercentage

    trainDf = df[trainDays]
    xTrainDf = trainDf.drop(labelName, axis=1)
    yTrainDf = trainDf[labelName]

    testDf = df[~trainDays]
    xTestDf = testDf.drop(labelName, axis=1)
    yTestDf = testDf[labelName]

    return xTrainDf, yTrainDf, xTestDf, yTestDf


def getCompaniesFromFile(filename):
    companies = []
    with open(filename, 'r') as f:
        for line in f:
            parts  = line.split(",")
            companies.append(parts[0])
        f.close()
    return companies

def trainSVC(x,y, kernelChoice, degreeChoice=3):
    if kernelChoice == 'linear':
        svcClassifier = svm.SVC(kernel=kernelChoice)
    elif kernelChoice == 'poly':
        svcClassifier = svm.SVC(kernel=kernelChoice, degree=degreeChoice)
    else:
        print("Error: Can't recognize your kernel choice of [{}] for SVC".format(kernelChoice))
    y = y.astype('int')
    svcClassifier.fit(x.values, y.values)
    return svcClassifier

if __name__ == "__main__":
    companies = getCompaniesFromFile("companies.csv")
    companyToDfDict = get_dataframe(companies)

    trainPercentage = 0.85
    classLblName = 'label' # 0 or 1 depending on whether a fall or rise from prev day
    svcKernelChoice = 'linear'
    for comp in companies:
        xTrain, yTrain, xTest, yTest = splitCompanyData(companyToDfDict[comp], trainPercentage, classLblName)
        svcClassifier = trainSVC(xTrain, yTrain, svcKernelChoice)
        yTest = yTest.astype('int')
        yPred = svcClassifier.predict(xTest.values)
        print("\nClassification report for {}".format(comp))
        print(classification_report(yTest.values, yPred))
        print("Score for {}".format(comp))
        print(svcClassifier.score(xTest.values, yTest.values))

        # cross validation
        svc = svm.SVC(kernel=svcKernelChoice)
        scores = cross_val_score(svc, companyToDfDict[comp].drop(classLblName, axis=1).astype('int').values, companyToDfDict[comp][classLblName].astype('int').values, cv=3)
        print("Accuracy for {}: {} (+/- {})".format(comp, scores.mean(), scores.std()*2))





