from datetime import datetime
from iexfinance import *


companies = []

with open('companies.csv', 'r') as f:
    for line in f:
        parts = line.split(",")
        if parts[1] != 'SSNLF':
            companies.append(parts[1])
    f.close()

start = datetime(2018,10,5)
end = datetime(2018, 11,25)
print(companies)

companies_dict = {x : get_historical_data(x, start=start, end=end, output_format='pandas') for x in companies}


with open('./stock_info.csv', 'w') as f:
    for company in companies_dict:
        df = companies_dict[company]
        res = 0
        for index, row in df.iterrows():
            pct_change = ((row['close']-row['open'])/row['open'])*100
            if row['open'] > row['close']:
                res = 0
            else:
                res = 1
            f.write('{},{},{},{},{},{},{},{},{}\n'.format(company, res, pct_change, index, row['open'],row['close'], row['high'], row['low'], row['volume']))
