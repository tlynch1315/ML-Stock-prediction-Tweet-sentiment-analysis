from get_dataframe import *
from math import *

def get_final_vals():
    di = get_dataframe()
    for comp in di:
        final_vals = []
        df = di[comp]
        for index, row in df.iterrows():
            if row['polarity'] < 0:
                final_vals.append(abs(row['value'])*-1)
            else:
                final_vals.append(abs(row['value']))
        df['final_vals'] = final_vals
    print di
    return di
#get_final_vals()
