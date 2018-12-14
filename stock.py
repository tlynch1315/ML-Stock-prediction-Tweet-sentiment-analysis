from datetime import datetime
from iexfinance import *

def get_companies():
    companies = []

    with open('companies.csv', 'r') as f:
        for line in f:
            parts = line.split(",")
            if parts[1] != 'SSNLF':
                companies.append(parts[1])
        f.close()
    return companies

def get_companies_full():
    companies = []

    with open('companies.csv', 'r') as f:
        for line in f:
            parts = line.split(",")
            if parts[1] != 'SSNLF':
                companies.append(parts[0])
        f.close()
    return companies


def get_prev_day_change():
    companies = get_companies()
    start = datetime(2018,10,4)
    end = datetime(2018, 11,25)

    companies_dict = {x : get_historical_data(x, start=start, end=end, output_format='pandas') for x in companies}


    with open('./stock_prev_info.csv', 'w') as f:
        for company in companies_dict:
            df = companies_dict[company]
            df['date'] = df.index
            df.index = range(len(df))
            for i in range(1,len(df)):
                pct_change = ((df.loc[i-1,'open']-df.loc[i,'open'])/df.loc[i-1,'open'])*100
                if df.loc[i-1, 'open'] > df.loc[i,'open']:
                    res = 0
                else:
                    res = 1
                f.write('{},{},{},{},{},{},{},{},{}\n'.format(company, res, pct_change, df.loc[i,'date'], df.loc[i,'open'],df.loc[i,'close'], df.loc[i, 'high'], df.loc[i, 'low'], df.loc[i, 'volume']))


def get_day_change():
    companies = get_companies()
    start = datetime(2018,10,5)
    end = datetime(2018, 11,25)

    companies_dict = {x : get_historical_data(x, start=start, end=end, output_format='pandas') for x in companies}


    with open('./stock_info.csv', 'w') as f:
        for company in companies_dict:
            df = companies_dict[company]
            for index, row in df.iterrows():
                pct_change = ((row['close']-row['open'])/row['open'])*100
                if row['open'] > row['close']:
                    res = 0
                else:
                    res = 1
                f.write('{},{},{},{},{},{},{},{},{}\n'.format(company, res, pct_change, index, row['open'],row['close'], row['high'], row['low'], row['volume']))
if __name__ == "__main__":
    get_prev_day_change()
