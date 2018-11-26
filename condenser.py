import time, tweepy, os, sys
from textblob import TextBlob
import json

### DICT MAPS NON_CONT TWEETS TO STOCK DATA ###
map_dict = {}
for i in range(1,23):
    map_dict[i] = {}

with open('stock_info.csv','r+') as f:
    text = f.readlines()


def touch(path):
    with open(path,'a'):
        os.utime(path,None)

if __name__ == "__main__":
    with open('companies.csv',"r+") as f:
        lines = f.readlines()
        titles = ["name","ticker","ceo"]
        for DAY in range(4,26):
            for line in lines:
                query = line.split(',')
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
                    print('Writing to '+writePath+'...\n')
                    writeFp.write('{0},{1}\n'.format(DAY-3,sum/n))
                except ZeroDivisionError:
                    continue
                writeFp.close()
