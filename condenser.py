import time, tweepy, os, sys
from textblob import TextBlob
import json

### DICT MAPS NON_CONT TWEETS TO STOCK DATA ###
map_dict = {1:'2018-10-05',2:'2018-10-07',3:'2018-10-08',4:'2018-10-09',5:'2018-10-10',6:'2018-10-11',\
            7:'2018-10-12',8:'2018-10-15',9:'2018-10-15',10:'2018-10-22',11:'2018-10-22',12:'2018-10-22',13:'2018-10-22',\
            14:'2018-10-23',15:'2018-10-25',16:'2018-10-29',17:'2018-10-30',18:'2018-11-01',19:'2018-11-02',20:'2018-11-04',\
            21:'2018-11-06',22:'2018-11-07',23:'2018-11-08'}


stocks = {}
with open('stock_info.csv','r+') as f:
    text = f.readlines()
    for line in text:
        split = line.split(',')
        try:
            stocks[split[0]].append(split[1:])
        except:
            stocks[split[0]] = [split[1:]]


def touch(path):
    with open(path,'a'):
        os.utime(path,None)

if __name__ == "__main__":
    with open('companies.csv',"r+") as f:
        lines = f.readlines()
        titles = ["name","ticker","ceo"]
        for DAY in range(4,26):
            date = map_dict[DAY-3]
            for line in lines:
                query = line.split(',')
                company = query[1]
                writePath ="data/clean/{0}-cleaned.txt".format(query[0])
                exists = os.path.isfile(writePath)
                if (exists==False):
                    touch(writePath)
                writeFp = open(writePath,'a')
                for i in range(1,len(query)-2):
                    titles.append("key{0}".format(i))
                n = 0
                sum = 0
                for i in range(0,len(query)-1):
                    path = "data/tweets/d{0}/{1}-{2}.txt".format(DAY,query[0],titles[i])
                    try:
                        with open(path,'r+') as fp:
                            data = fp.readlines()
                            n += len(data)
                            for twt in data:
                                try:
                                    tweet = json.loads(twt)
                                    testimonial = TextBlob(tweet['text'])
                                    sum += testimonial.sentiment.polarity*(1-testimonial.sentiment.subjectivity)
                                except UnicodeEncodeError:
                                    continue
                    except FileNotFoundError:
                        continue
                try:
                    stock_data_point = ''
                    for line in stocks[company]:
                        print(line[2],date)
                        if str(line[2])==str(date):
                            for pt in line:
                                stock_data_point+=',{0}'.format(pt)
                    print('Writing to '+writePath+'...\n')
                    print('{0},{1}{2}\n'.format(DAY-3,sum/n,stock_data_point))
                    writeFp.write('{0},{1}{2}\n'.format(DAY-3,sum/n,stock_data_point))
                except ZeroDivisionError:
                    continue
                writeFp.close()
