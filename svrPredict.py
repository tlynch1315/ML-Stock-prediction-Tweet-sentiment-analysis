import pandas as pd 
import numpy as np 
from sklearn.svm import SVR
import matplotlib.pyplot as plt 
from get_dataframe import *
from sklearn.cross_validation import train_test_split
import math
from sklearn.metrics import r2_score

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

def getCompanyData(dictionary, companyName):
    df = dictionary[companyName]
    df = df.drop(['change', 'open'],axis=1)

    grouped = df.groupby('date')

    totalDays = len(grouped)
    trainingDays = math.floor(0.75*totalDays)
    testingDays = totalDays - trainingDays

    dateList = [date for date in grouped]

    trainList = dateList[:trainingDays]
    testList = dateList[:testingDays]

    trainDF = trainList.pop(0)[1]
    testDF = testList.pop(0)[1]

    for day in trainList:
        trainDF = trainDF.append(day[1])

    for day in testList:
        testDF = testDF.append(day[1])

    print(trainDF.head())
    print(len(trainDF))
    print(len(testDF))
    print(len(grouped))
    XTrainData = trainDF.drop(['value', 'date'], axis=1)
    XTestData = testDF.drop(['value', 'date'],axis=1)

    YTrainData = trainDF['value']
    YTestData = testDF['value']

    return XTrainData, XTestData, YTrainData, YTestData


# total days = 23
df = pd.read_csv("./final.csv")
tweet_dict = get_dataframe()

companies = []

with open('companies.csv', 'r') as f:
    for line in f:
        parts = line.split(",")
        if parts[1] != 'SSNLF':
            companies.append(parts[0])
    f.close()


print(companies)



XTrainTesla, XTestTesla, YTrainTesla, YTestTesla = getCompanyData(tweet_dict, 'Tesla')

# make numbers a little more intuitive to look at
YTrainTesla *= 1000
YTestTesla *= 1000


"""
dfTesla = dfTesla.drop([ 'change', 'open'], axis=1)

groupedTesla = 

YTesla = dfTesla['value'].astype(float)
XTesla['followers'] = XTesla['followers'].astype(float)
XTesla['polarity'] = XTesla['polarity'].astype(float)
XTesla['sentiment_confidence'] = XTesla['sentiment_confidence'].astype(float)

XTesla = XTesla.groupby(date)

# group by dates
totalDays = len(XTesla)
trainingDays = math.floor(0.75*totalDays)
testingDays = totalDays - trainingDays
for feature in XTesla:
    XTesla.feature
    print(days)

XTrainTesla, XTestTesla, YTrainTesla, YTestTesla = train_test_split(XTesla.values, YTesla.values, random_state=42)
"""
kernel = "linear"
svr_C = 100
svr_degree = 2
svr_gamma = 1e-5
teslaSVR = trainSVR(XTrainTesla, YTrainTesla, "rbf", svr_C, svr_degree, svr_gamma)

print(type(XTestTesla))
YPredictTesla = []
for index,row in XTestTesla.iterrows():
    YPredictTesla.append(teslaSVR.predict(row.reshape(1,-1)))

print(type(YPredictTesla[0]))

plt.plot(range(len(YTestTesla)),YTestTesla)
plt.plot(range(len(YTestTesla)),YPredictTesla)
plt.show()

"""
print("5TH")
print(dfTesla[dfTesla["date"] == "2018-10-05"]['change'][0])
print(dfTesla[dfTesla["date"] == "2018-10-05"]['value'].sum())
print("8TH")
print(dfTesla[dfTesla["date"] == "2018-10-08"]['change'][0])
print(dfTesla[dfTesla["date"] == "2018-10-08"]['value'].sum())

print("value")
print(dfTesla.groupby('date')['value'].sum())
print("change")
print(dfTesla.groupby('date')['change'].mean())
"""