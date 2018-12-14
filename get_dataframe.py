import pandas as pd
from stock import *
from tabulate import tabulate



def get_dataframe(companies):
    columns = ['followers', 'polarity', 'sentiment_confidence', 'value', 'date', 'change', 'open']
    dict_ = {}

    for comp in companies:
        curr = []
        for i in range(1, 23):
            daydf = pd.DataFrame(columns=['positive','negative', 'neutral', 'label'])
            try:
                path = './data/clean/d{}/{}-cleaned.csv'.format(i, comp)
                data = pd.read_csv(path, names=columns)
                if len(data) > 0:
                    daydf.at[0,'positive'] = len(data.loc[data['polarity'] > 0])
                    daydf.at[0,'negative'] = len(data.loc[data['polarity'] < 0])
                    daydf.at[0,'neutral'] = len(data.loc[data['polarity'] == 0])

                    if data.at[0,'change'] < 0:
                        daydf.at[0,'label'] = 0
                    else:
                        daydf.at[0,'label'] = 1
                else:
                    daydf.at[0,'positive'] = 0
                    daydf.at[0,'negative'] = 0
                    daydf.at[0,'neutral'] = 0

                    daydf.at[0,'label'] = 0
                curr.append(daydf)
            except FileNotFoundError:
                daydf.at[0,'positive'] = 0
                daydf.at[0,'negative'] = 0
                daydf.at[0,'neutral'] = 0
                daydf.at[0,'label'] = 0
        frame = pd.concat(curr)
        frame.index = [x for x in range(len(curr))]
        dfList = []
        for i in range(len(frame)):
            newdf = pd.DataFrame(columns=['positive','negative', 'neutral', 'label'])
            if i < 3:
                newdf.at[0,'positive'] = frame.loc[i, 'positive']*3
                newdf.at[0,'negative'] = frame.loc[i, 'negative']*3
                newdf.at[0,'neutral'] = frame.loc[i, 'neutral']*3
                newdf.at[0,'label'] = frame.at[i,'label']
            else:
                newdf.at[0,'positive'] = frame.loc[i-3, 'positive'] + frame.loc[i-2, 'positive'] + frame.loc[i-1, 'positive']
                newdf.at[0,'negative'] = frame.loc[i-3, 'negative'] + frame.loc[i-2, 'negative'] + frame.loc[i-1, 'negative']
                newdf.at[0,'neutral'] = frame.loc[i-3, 'neutral'] + frame.loc[i-2, 'neutral'] + frame.loc[i-1, 'neutral']
                newdf.at[0,'label'] = frame.at[i,'label']
            dfList.append(newdf)
        fr = pd.concat(dfList)
        fr.index = [x for x in range(len(dfList))]
        dict_[comp]=fr

    return dict_




if __name__ == "__main__":
    companies = get_companies_full()
    li = get_dataframe(companies)
    for comp in li:
        print(comp)
        print(tabulate(li[comp], headers='keys', tablefmt='psql'))
