import pandas as pd

def get_dataframe():
    columns = ['followers', 'polarity', 'sentiment_confidence', 'value']
    companies = []

    with open('companies.csv', 'r') as f:
        for line in f:
            parts = line.split(",")
            if parts[1] != 'SSNLF':
                companies.append(parts[0])
        f.close()
    dict_ = {}

    for comp in companies:
        curr = []
        df = pd.DataFrame(columns=columns)
        for i in range(1, 23):
            path = './data/clean/d{}/{}-cleaned.txt'.format(i, comp)
            data = pd.read_csv(path, names=columns)
            curr.append(data)
        frame = pd.concat(curr)
        dict_[comp]=frame

    return dict_
if __name__ == "__main__":
    li = get_dataframe()
