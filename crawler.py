import time, tweepy, os
import json

DAY = "d1"
f = open("my_keys.txt","r+")
lines_ = f.readlines()
f.close()

consumer_key=lines_[0].strip('\n')
consumer_secret=lines_[1].strip('\n')
access_token=lines_[2].strip('\n')
access_token_secret=lines_[3].strip('\n')
print(lines_)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def touch(path):
    with open(path,'a'):
        os.utime(path,None)

with open('companies.csv',"r+") as f:
    lines = f.readlines()
    titles = ["name","ticker","ceo"]
    for line in lines:
        query = line.split(',')
        for i in range(1,len(query)-2):
            titles.append("key{0}".format(i))
        for i in range(0,len(query)-1):
            path = "data/tweets/{0}/{1}-{2}.txt".format(DAY,query[0],titles[i])
            exists = os.path.isfile(path)
            if (exists==False):
                touch(path)
                wf = open(path,"r+")
                que = query[i].strip('\n')
                data = api.search(q=que,count=1000)
                for status in data:
                    try:
                        wf.write("{0}\n".format(status))
                    except UnicodeEncodeError:
                        pass
                wf.close()
                print("Successfuly wrote {0} tweets to {1}\n\t\t\tusing search word {2}!".format(len(data),path,que))
