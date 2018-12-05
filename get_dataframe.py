import pandas as pd
from stock import *
from tabulate import tabulate


def get_3_day_frame():
    columns = ['followers', 'polarity', 'sentiment_confidence', 'value', 'date', 'change', 'open']



def get_dataframe(companies):
    columns = ['followers', 'polarity', 'sentiment_confidence', 'value', 'date', 'change', 'open']
    dict_ = {}

    for comp in companies:
        curr = []
        df = pd.DataFrame(columns=columns)
        for i in range(1, 22):
            print(i, comp)
            path = './data/clean/d{}/{}-cleaned.csv'.format(i, comp)
            data = pd.read_csv(path, names=columns)
            daydf = pd.DataFrame(columns=['positive','negative', 'neutral', 'label'])
            if len(data) > 0:
                daydf.at[0,'positive'] = len(data.loc[data['polarity'] > 0])
                daydf.at[0,'negative'] = len(data.loc[data['polarity'] < 0])
                daydf.at[0,'neutral'] = len(data.loc[data['polarity'] == 0])
                #print(daydf.at[0,'positive'])
                #print(data)
                if data.at[0,'change'] < 0:
                    daydf.at[0,'label'] = 0
                else:
                    daydf.at[0,'label'] = 1
            else:
                daydf.at[0,'positive'] = 0
                daydf.at[0,'negative'] = 0
                daydf.at[0,'neutral'] = 0
                #print(daydf.at[0,'positive'])
                #print(data)
                daydf.at[0,'label'] = 0
            curr.append(daydf)

        frame = pd.concat(curr)
        frame.index = [x for x in range(len(curr))]
        dfList = []
        for i in range(len(frame)):
            newdf = pd.DataFrame(columns=['positive','negative', 'neutral', 'label'])
            if i < 3:
                newdf.at[0,'positive'] = frame.loc[i, 'positive']
                newdf.at[0,'negative'] = frame.loc[i, 'negative']
                newdf.at[0,'neutral'] = frame.loc[i, 'neutral']
                newdf.at[0,'label'] = frame.at[i,'label']
            else:
                newdf.at[0,'positive'] = frame.loc[i-3, 'positive'] + frame.loc[i-2, 'positive'] + frame.loc[i-1, 'positive']
                newdf.at[0,'negative'] = frame.loc[i-3, 'negative'] + frame.loc[i-2, 'negative'] + frame.loc[i-1, 'negative']
                newdf.at[0,'neutral'] = frame.loc[i-3, 'neutral'] + frame.loc[i-2, 'neutral'] + frame.loc[i-1, 'neutral']
                newdf.at[0,'label'] = frame.at[i,'label']
            dfList.append(newdf)
            '''print("NEW DATAFRAME")
            print(newdf)
            print("OLD DATAFRAME")
            print(frame.iloc[i])'''
            #if i > 3:
            #    exit()
            #print(tabulate(newdf, headers='keys', tablefmt='psql'))

        fr = pd.concat(dfList)

        dict_[comp]=fr

    return dict_


def prep_dataframe(dict_):
    df = pd.DataFrame(columns=['prev3', 'prev2', 'prev1', 'label'])
    for comp in dict_.keys():
        curr = dict_[comp]
        print(curr)



if __name__ == "__main__":
    companies = get_companies_full()
    li = get_dataframe(companies)
    for comp in li:
        #print(li[comp].index)
        print(tabulate(li[comp], headers='keys', tablefmt='psql'))
