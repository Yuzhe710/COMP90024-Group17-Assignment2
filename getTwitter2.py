import tweepy
from tweepy import Stream
import couchdb
from textblob import TextBlob
from urllib3.exceptions import ProtocolError
import csv
import time

consumer_key = 'OfAl9mdmjwx9yPYKdUHJe1jg5'
consumer_secret = 'vznydYvSCKOs6JBTmNJg8QS4M0TuJ3nUhbr1bmieHa2UMI7xiT'
access_token = '1213206459879571456-A3YklaYorRz8iaQZUvbBs4ukrqQPsc'
access_token_secret = 'eLjzrlxMWasU1cBSB7iulVOUp16A27RBisnABAUfKARZD'

count = 0


########################################################################
################ This is for storing into couchDB ######################
########################################################################
# try:
#     couchclient = couchdb.Server('http://yuzhe710:admin@localhost:5984/')
# except:
#     print("Cannot find CouchDB Server ... Exiting\n")
#     print("----_Stack Trace_-----\n")
#     raise

# try:
#     db = couchclient['twitter_test']
#     # db = couchclient.create('twitter_test')
#     print("Connected to the user database")
# except:
#     db = couchclient['default']
#     print("Connected to the default database")

class Std(Stream):
    # def on_data(self, data):
    #     if data[0].isdigit():
    #         pass
    #     else:
    #         global ttstart
    #         global ttend
    #
    #         if ttstart <= ttend:
    #             if data[0].isdigit():
    #                 pass
    #             else:
    #                 jsondata = json.loads(data)
    #                 db.save(jsondata)
    #                 ttstart += 1
    #     return True

    def on_data(self, status):
        global count
        global ttend
        # print(status)
        text = status.text
        # username = status.user.screen_name
        id_str = status.id_str
        createtime = str(status.created_at)
        # source = status.source
        # userlocation = status.user.location
        lang = status.lang
        retweeted = status.retweeted
        # placename = status.place.name
        geo = status.geo
        # blob = TextBlob(text)
        # sent = blob.sentiment
        # polarity = sent.polarity
        # subjectivity = sent.subjectivity
        if retweeted == False:
            data = [id_str, text, geo, lang, createtime]
            writer.writerow(data)
            # db.save({"id": id_str,"createtime":createtime,"source":source ,"text": text, "username": username,"userlocation":userlocation,"lang": lang, "placename": placename, "geo": geo,
            #         "polarity": polarity, "subjectivity": subjectivity})
            count += 1
            print(count)
        else:
            pass

    def on_error(self, status):
        print(status)
        

# l = Std()
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

#stream = Std(consumer_key, consumer_secret, access_token, access_token_secret)

# stream = tweepy.streaming.Stream(auth, Std(consumer_key, consumer_secret, access_token, access_token_secret))    
# api = tweepy.API(auth)

stream = Std(consumer_key, consumer_secret, access_token, access_token_secret)

save_file = open('Twitter.csv', 'w')


with open('Twitter.csv', 'w') as save_file:

    writer = csv.writer(save_file)
    header = ['id', 'text', 'geolocation', 'language', 'time']
    writer.writerow(header)

    while True:
        try:
            stream.filter(track = ['house'], locations=[144.33363404800002, -38.50298801599996, 145.8784120140001, -37.17509899299995], languages=["en"])
        except ProtocolError as e:
                print(f"{timestamp()} ProtocolError: {e}\n")
        except AttributeError as e:
            print(f"{timestamp()} AttributeError: {e}\n")
        except Exception as e:
            print(f"{timestamp()} Received unknown exception: {e}\n") 
        finally:
            save_file.close()
            continue  
