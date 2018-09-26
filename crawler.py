import time, tweepy, os
import json


f = open("my_keys.txt","r+")
lines = f.readlines()
f.close()

consumer_key=lines[0].strip('\n')
consumer_secret=lines[1].strip('\n')
access_token=lines[2].strip('\n')
access_token_secret=lines[3].strip('\n')
print(lines)


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


class FilteredStream(tweepy.StreamListener):
    def __init__(self,time_limit=60):
        self.start_time = time.time()
        self.limit = time_limit
        self.File = open("data.txt","r+")
        super(FilteredStream,self).__init__()

    def on_status(self,status):
        if (time.time() - self.start_time) < self.limit:
            try:
                self.File.write("{0},{1},{2}\n".format(status.id_str,status.text,status.created_at))
            except UnicodeEncodeError:
                pass
            return True
        else:
            self.File.close()
            return False


stream = tweepy.Stream(auth=api.auth,listener=FilteredStream(time_limit=10))
stream.filter(locations=[-124,24,-66,49])
print("done")
