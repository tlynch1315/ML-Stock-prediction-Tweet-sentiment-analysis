import pandas as pd 
import numpy as np 
from sklearn.svm import SVR
import matplotlib.pyplot as plt 
from get_dataframe import *
from sklearn.cross_validation import train_test_split

def trainSVR(X, Y, kernelChoice, degreeChoice=3, gammaChoice=0.1):
    if kernelChoice == "linear":
        svr = SVR(kernel = kernelChoice, C = '1e3')
    elif kernelChoice == "poly":
        svr = SVR(kernel = kernelChoice, C = '1e3', degree = degreeChoice)
    elif kernelChoice == "rbf": 
        svr = SVR(kernel = kernelChoice, C = '1e3', gamma = gammaChoice)
    else:
        print("ERROR in trainSVR, do not recognize the following svr kernel choice: {}", kernelChoice)

    return svr.fit(X, Y)

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
XTesla = dfTesla.drop(['value', 'date', 'change'], axis=1)
YTesla = dfTesla['value'].astype(float)
XTesla['followers'] = XTesla['followers'].astype(float)
XTesla['polarity'] = XTesla['polarity'].astype(float)
XTesla['sentiment_confidence'] = XTesla['sentiment_confidence'].astype(float)
print(dfTesla.shape)
print(XTesla.shape)
print(YTesla.shape)

XTrainTesla, XTestTesla, YTrainTesla, YTestTesla = train_test_split(XTesla, YTesla, random_state=42)

print(XTrainTesla.shape)
print(YTrainTesla.shape)

svr = trainSVR(XTrainTesla, YTrainTesla, "linear")
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