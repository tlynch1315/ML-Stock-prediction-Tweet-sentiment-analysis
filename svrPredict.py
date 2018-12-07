import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
from get_dataframe import *
import math
import argparse


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

def trainSVC(x,y, kernelChoice, degreeChoice=2, gamma='scale'):
    '''if kernelChoice == 'linear':
        svcClassifier = svm.SVC(kernel=kernelChoice)
    elif kernelChoice == 'poly':
        svcClassifier = svm.SVC(kernel=kernelChoice, degree=degreeChoice, gamma='scale')
    else:'''
    svcClassifier = svm.SVC(kernel=kernelChoice, degree=degreeChoice, gamma='scale')

        #print("Error: Can't recognize your kernel choice of [{}] for SVC".format(kernelChoice))
    y = y.astype('int')
    svcClassifier.fit(x.values, y.values)
    return svcClassifier

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-k', dest='kernelChoice', type=str, default='linear')
    parser.add_argument('-d', dest='degrees', type=int, default='2')
    parser.add_argument('-g', dest='gamma', type=str, default='scale')
    args = parser.parse_args()
    companies = getCompaniesFromFile("companies.csv")
    companyToDfDict = get_dataframe(companies)

    trainPercentage = 0.85
    classLblName = 'label' # 0 or 1 depending on whether a fall or rise from prev day
    svcKernelChoice = 'poly'
    dfList = []
    for comp in companies:
        dfList.append(companyToDfDict[comp])
    dfTotal = pd.concat(dfList)
    xTrain, yTrain, xTest, yTest = splitCompanyData(dfTotal, trainPercentage, classLblName)
    svcClassifier = trainSVC(xTrain, yTrain, args.kernelChoice, degreeChoice=args.degrees, gamma=args.gamma)
    yTest = yTest.astype('int')
    yPred = svcClassifier.predict(xTest.values)
    print("\nClassification report for All Data")
    print(classification_report(yTest.values, yPred))
    print("Score for {}".format("All Data"))
    print(svcClassifier.score(xTest.values, yTest.values))

    # cross validation
    svc = svm.SVC(kernel=svcKernelChoice, degree=args.degrees, gamma=args.gamma)
    scores = cross_val_score(svc, dfTotal.drop(classLblName, axis=1).astype('int').values, dfTotal[classLblName].astype('int').values, cv=3)
    print("Accuracy for {}: {} (+/- {})".format("All Data", scores.mean(), scores.std()*2))
