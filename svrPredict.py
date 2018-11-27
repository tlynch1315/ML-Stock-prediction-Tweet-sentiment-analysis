import pandas as pd 
import numpy as np 
from sklearn.svm import SVR
import matplotlib.pyplot as plt 
from get_dataframe import *
from sklearn.cross_validation import train_test_split

def trainSVR(X, Y, kernelChoice, degreeChoice=3, gammaChoice=1e-5):
    if kernelChoice == "linear":
        mySVR = SVR(kernel = kernelChoice, C = 1)
    elif kernelChoice == "poly":
        mySVR = SVR(kernel = kernelChoice, C = 1, degree = degreeChoice)
    elif kernelChoice == "rbf": 
        mySVR = SVR(kernel = kernelChoice, C = 100, gamma = gammaChoice)
    else:
        print("ERROR in trainSVR, do not recognize the following svr kernel choice: {}", kernelChoice)

    return mySVR.fit(X, Y)

kernel = "linear"
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

dfTesla = tweet_dict["Tesla"]
XTesla = dfTesla.drop(['value', 'date', 'change', 'open'], axis=1)
YTesla = dfTesla['value'].astype(float)
print(XTesla['followers'])
XTesla['followers'] = XTesla['followers'].astype(float)
XTesla['polarity'] = XTesla['polarity'].astype(float)
XTesla['sentiment_confidence'] = XTesla['sentiment_confidence'].astype(float)

XTrainTesla, XTestTesla, YTrainTesla, YTestTesla = train_test_split(XTesla.values, YTesla.values, random_state=42)

print("XTRAIN")
print(XTrainTesla)
print("YTRAIN")
print(YTrainTesla)

YTrainTesla *= 1000

teslaSVR = trainSVR(XTrainTesla, YTrainTesla, "rbf")
YPredictTesla = []
for tweet in XTestTesla:
    print(tweet.reshape(1,-1))
    YPredictTesla.append(teslaSVR.predict(tweet.reshape(1,-1)))
YTestTesla *= 1000
print(YTestTesla)
print(YPredictTesla)
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