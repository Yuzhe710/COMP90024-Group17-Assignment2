from tweepy import StreamingClient, StreamRule, Tweet
import csv

save_file = open('Twitter.csv', 'w')
writer = csv.writer(save_file)
header = ['id', 'text', 'geolocation', 'language', 'time']
writer.writerow(header)

class TweetListener(StreamingClient):
    """
    StreamingClient allows filtering and sampling of realtime Tweets using Twitter API v2.
    https://docs.tweepy.org/en/latest/streamingclient.html#tweepy.StreamingClient
    """

    def on_data(self, data):
        global count
        global ttend
        # print(status)
        text = data.text
        # username = status.user.screen_name
        id_str = data.id_str
        createtime = str(data.created_at)
        # source = status.source
        # userlocation = status.user.location
        lang = data.lang
        retweeted = data.retweeted
        # placename = status.place.name
        geo = data.geo
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

    def on_tweet(self, tweet: Tweet):
        print(tweet.__repr__())


    def on_request_error(self, status_code):
        print(status_code)

    def on_connection_error(self):
        self.disconnect()


if __name__ == "__main__":
    """
     - Save it in a secure location
     - Treat it like a password or a set of keys
     - If security has been compromised, regenerate it
     - DO NOT store it in public places or shared docs
    """
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAJtBcAEAAAAA3df5WVxmsRRRqYQQuwUcxuJMRzU%3DqYTQmXuAG4nXJQa96vxwmHI7cWDdDQ7Ge7QsGB1sdeO9rCgBGB"

    if not bearer_token:
        raise RuntimeError("Not found bearer token")

    client = TweetListener(bearer_token)

    # https://docs.tweepy.org/en/latest/streamingclient.html#streamrule
    # https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/integrate/build-a-rule
    # Operator availability (check the operators table)
    # - Core operators: Available when using any access level.
    # - Advanced operators: Available when using a Project with Academic Research access.
    # keyword:
    #   - "melbourne"
    rules = [
        StreamRule(value="house")

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

    # https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/api-reference/get-tweets-search-stream
    try:
        client.filter()
    except KeyboardInterrupt:
        client.disconnect()