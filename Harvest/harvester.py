################################################################################
################ Haverster the Stream Tweets, with keyword melbourne house, save 
################ id, time, text, user_id, lang, general_emotion, top_emotion ###
################ And save it to couchdb on MRC  ################################
################################################################################

from typing import final
import tweepy
import couchdb
import time
import json
from tweepy import StreamingClient, StreamRule, Tweet
from textblob import TextBlob
import text2emotion as te

import nltk
nltk.download('omw-1.4')


def get_emotion_textbolb(text):
    if not isinstance(text,str):
        return 'Neutral'
    else:
        blob = TextBlob(text)

        score = blob.sentiment
        polarity = score.polarity
        subjectivity = score.subjectivity

        if polarity>0:
            label = 'Positive'
        elif polarity == 0:
            label = 'Neutral'
        elif polarity < 0:
            label = 'Negative'
        return label

def get_text2emotion(text):
    if not isinstance(text,str):
        return []
    else:
        result = []
        dic = te.get_emotion(text)
        for k in dic:
            result.append((k, dic[k]))
        result.sort(key=lambda tup: tup[1], reverse=True)
        return result[0][0]

class TweetListener(StreamingClient):
    """
    StreamingClient allows filtering and sampling of realtime Tweets using Twitter API v2.
    https://docs.tweepy.org/en/latest/streamingclient.html#tweepy.StreamingClient
    """

    def on_tweet(self, tweet: Tweet):
        # print(tweet.__repr__())
        global count
        text = tweet.text
        user_id = tweet.author_id
        id_str = str(tweet.id)
        createtime = str(tweet.created_at)
        lang = tweet.lang
        general_emotion = get_emotion_textbolb(text)
        top_emotion = get_text2emotion(text)
        count = count + 1
        try:
            db.save({"id": id_str,"createtime":createtime,"text": text, "user_id": user_id, "lang": lang,
                        "general_emotion": general_emotion, "top_emotion": top_emotion})
        except couchdb.HTTPError as e:
            print("ERROR: duplicate")
        except Exception as e:
            print(e)
        # print(tweet)
        print(count)

    def on_request_error(self, status_code):
        print(status_code)

    def on_connection_error(self):
        self.disconnect()

if __name__ == "__main__":

    # bearer_token='AAAAAAAAAAAAAAAAAAAAAFTkcQEAAAAA3O7geWIjYh6TD13FidqKmxOH8uw%3DWhtaMZvqE7YOZttckfL13e8Q48oJgID6sM3vakRdB8e8v60Kr4'

    bearer_token = 'AAAAAAAAAAAAAAAAAAAAAJtBcAEAAAAA3df5WVxmsRRRqYQQuwUcxuJMRzU%3DqYTQmXuAG4nXJQa96vxwmHI7cWDdDQ7Ge7QsGB1sdeO9rCgBGB'

    ## Couchdb setup ###
    masternode='172.26.132.32'
    user='admin'
    passeord='admin'
    url = 'http://'+user+':'+passeord+'@'+masternode+':5984/'
    try:
        couchclient = couchdb.Server(url)
    except:
        print("Cannot find CouchDB Server ... Exiting\n")
        print("----_Stack Trace_-----\n")
        raise

    try:
        db = couchclient['twitter']
        print("Connected to the user database")
    except:
        # db = couchclient['default']
        print("Connected to the default database")

    count = 0

    if not bearer_token:
        raise RuntimeError("Not found bearer token")

    client = TweetListener(bearer_token)

    # keyword:
    #   - "melbourne"
    rules = [
        StreamRule(value="house"),
        StreamRule(value="melbourne")
    ]

    # https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/api-reference/post-tweets-search-stream-rules
    # Remove existing rules
    resp = client.get_rules()
    if resp and resp.data:
        rule_ids = []
        for rule in resp.data:
            rule_ids.append(rule.id)

        client.delete_rules(rule_ids)

    # Validate the rule
    resp = client.add_rules(rules, dry_run=True)
    if resp.errors:
        raise RuntimeError(resp.errors)

    # Add the rule
    resp = client.add_rules(rules)
    if resp.errors:
        raise RuntimeError(resp.errors)

    # https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/api-reference/get-tweets-search-stream-rules
    print(client.get_rules())

    try:
        client.filter(tweet_fields=['lang', 'created_at'])
    except KeyboardInterrupt:
        client.disconnect()
