import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.metrics import classification_report, auc
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve

from sklearn.tree import DecisionTreeClassifier, export_graphviz
import matplotlib.pyplot as plt
from get_dataframe import *
import math
import argparse
import graphviz
from sklearn.naive_bayes import GaussianNB



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

def trainSVC(x,y, xTest, yTest, dfTotal, classLblName, kernelChoice, degreeChoice=2, gamma='scale'):
    svcClassifier = svm.SVC(kernel=kernelChoice, degree=degreeChoice, gamma='scale', probability=True)
    y = y.astype('int')
    svcClassifier.fit(x.values, y.values)

    yTest = yTest.astype('int')
    yPred = svcClassifier.predict(xTest.values)
    yProbs = svcClassifier.predict_proba(xTest.values)
    print("\nClassification report for All Data")
    print(classification_report(yTest.values, yPred))
    print("Score for {}".format("All Data"))
    print(svcClassifier.score(xTest.values, yTest.values))
    svc = svm.SVC(kernel=kernelChoice, degree=args.degrees, gamma=args.gamma)
    scores = cross_val_score(svc, dfTotal.drop(classLblName, axis=1).astype('int').values,
                             dfTotal[classLblName].astype('int').values, cv=10)
    print("Accuracy for {}: {} (+/- {})".format("All Data", scores.mean(), scores.std() * 2))
    plotter(yTest, yProbs, "SVC : {}".format(kernelChoice))



def DTree(xTrain, yTrain, xTest, yTest, dfTotal, classLblName):
    clf = DecisionTreeClassifier(random_state=42)
    clf1 = DecisionTreeClassifier()
    clf1.fit(xTrain.values, yTrain.astype('int').values)
    yPred = clf1.predict(xTest.values)
    yProbs = clf1.predict_proba(xTest)
    yTest = yTest.astype('int')
    print("\nClassification report for All Data")
    print(classification_report(yTest.values, yPred))
    scores = cross_val_score(clf, dfTotal.drop(classLblName, axis=1).astype('int').values,
                             dfTotal[classLblName].astype('int').values, cv=10)
    print("Accuracy for {}: {} (+/- {})".format("All Data", scores.mean(), scores.std() * 2))
    dot_data = export_graphviz(clf1, out_file=None)
    graph = graphviz.Source(dot_data)
    graph.render("Decision Tree")
    print("Decision Tree Rendered")
    plotter(yTest, yProbs, "Decision Tree")


def random_forest(xTrain, yTrain, xTest, yTest, dfTotal, classLblName):
    clf = RandomForestClassifier(n_estimators=100, max_depth=3)
    clf1 = RandomForestClassifier(n_estimators=100, max_depth=3)
    clf1.fit(xTrain.values, yTrain.astype('int').values)
    yPred = clf1.predict(xTest.values)
    yProbs = clf1.predict_proba(xTest.values)
    yTest = yTest.astype('int')
    print("\nClassification report for All Data")
    print(classification_report(yTest.values, yPred))
    scores = cross_val_score(clf, dfTotal.drop(classLblName, axis=1).astype('int').values, dfTotal[classLblName].astype('int').values, cv=10)
    print("Accuracy for {}: {} (+/- {})".format("All Data", scores.mean(), scores.std()*2))
    plotter(yTest, yProbs, "Random Forest")



def GNB(xTrain, yTrain, xTest, yTest, dfTotal, classLblName):
    # Naive Bayes GaussianNB
    gnb1 = GaussianNB()
    gnb = GaussianNB()
    yPred = gnb.fit(xTrain.values, yTrain.astype('int').values).predict(xTest.values)
    yProbs = gnb.predict_proba(xTest)
    #yPred = clf1.predict(xTest.values)
    yTest = yTest.astype('int')
    print("\nClassification report for All Data")
    print(classification_report(yTest.values, yPred))
    scores = cross_val_score(gnb1, dfTotal.drop(classLblName, axis=1).astype('int').values, dfTotal[classLblName].astype('int').values, cv=10)
    print("Accuracy for {}: {} (+/- {})".format("All Data", scores.mean(), scores.std()*2))
    plotter(yTest, yProbs, "Gaussian Naive Bayes")



def plotter(yTest, yProbs, title):

    y_probs = []
    for i in range(len(yTest)):
        if yTest.values[i] == 1:
            y_probs.append(yProbs[i][1])
        else:
            y_probs.append(yProbs[i][0])

    fpr, tpr, thresholds = roc_curve(yTest.values, y_probs)
    under_curve = auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % under_curve)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve for {}'.format(title))
    plt.legend(loc="lower right")

def getArgs():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-k', dest='kernelChoice', type=str, default='linear',
                        help='Choices : rbf, poly, linear, sigmoid')
    parser.add_argument('-d', dest='degrees', type=int, default='2')
    parser.add_argument('-g', dest='gamma', type=str, default='scale', help='Choices : scale, auto')
    parser.add_argument('-m', dest='model', type=str, default='svc',
                        help='Choices : gnb -> Gaussian Naive Bayes, svc -> Support Vector Classifier, '
                             'rf -> Random Forest, dt -> Decision Tree')
    return parser.parse_args()

if __name__ == "__main__":

    # get command line arguments
    args = getArgs()

    # get company names and data frames
    companies = getCompaniesFromFile("companies.csv")
    companyToDfDict = get_dataframe(companies)

    # train on 85% of data
    trainPercentage = 0.85
    classLblName = 'label' # 0 or 1 depending on whether a fall or rise from prev day

    # put all data into one dataframe
    dfList = []
    for comp in companies:
        dfList.append(companyToDfDict[comp])
    dfTotal = pd.concat(dfList)

    # split the data
    xTrain, yTrain, xTest, yTest = splitCompanyData(dfTotal, trainPercentage, classLblName)

    # create model based on command line arguments
    if args.model == 'gnb':
        GNB(xTrain, yTrain, xTest, yTest, dfTotal, classLblName)
    elif args.model == 'svc':
        trainSVC(xTrain, yTrain, xTest, yTest, dfTotal, classLblName, args.kernelChoice, degreeChoice=args.degrees, gamma=args.gamma)
    elif args.model == 'rf':
        random_forest(xTrain, yTrain, xTest, yTest, dfTotal, classLblName)
    elif args.model == 'dt':
        DTree(xTrain, yTrain, xTest, yTest, dfTotal, classLblName)

    # plot the graph
    plt.show()
