import tweepy
import time
import json
import text2emotion as te

# client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAJtBcAEAAAAA3df5WVxmsRRRqYQQuwUcxuJMRzU%3DqYTQmXuAG4nXJQa96vxwmHI7cWDdDQ7Ge7QsGB1sdeO9rCgBGB')
client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAAVxcQEAAAAA4gsJmKveGFiNVlzdqbI6ac8mTU8%3DmGOCwKYSOiRCPKkZ75yEDuvjqglIJdK0rKFDTBKgSrxUqlEXA8')

key_words = ['(rent OR price OR cost OR payment) (house OR housing OR apartment OR residence OR mansion OR residence)',
             '(buy OR pay OR purchase OR afford OR affordable) (house OR housing OR apartment OR residence OR mansion OR residence)',
             '(can\'t OR cannot OR unable OR incapable) (buy OR pay OR purchase OR afford OR affordable) (house OR housing OR apartment OR residence OR mansion OR residence)',
             '(want OR wanted OR wish OR like) (buy OR pay OR purchase OR afford OR affordable) (house OR housing OR apartment OR residence OR mansion OR residence)']

city_key = ['(Creswick OR Daylesford OR Ballan OR creswick OR daylesford OR ballan)',
            '(Heathcote OR Castlemaine OR Kyneton OR heathcote OR castlemaine OR kyneton)',
            '(Geelong OR geelong)',
            '(Surf Coast OR Bellarine Peninsula OR surf coast OR bellarine peninsula)',
            '(Upper Goulburn Valley OR upper goulburn valley)',
            '(Baw Baw OR baw baw)',
            '(Gippsland OR Gippsland South West OR gippsland OR gippsland south west)',
            '(Brunswick OR Coburg OR brunswick OR coburg)',
            '(Darebin South OR darebin south)',
            '(Darebin North OR darebin north)',
            '(Essendon OR essendon)',
            '(Melbourne City OR Melbourne OR melbourne OR melbourne city)',
            '(Port Phillip OR port phillip)',
            '(Boroondara OR boroondara)',
            '(Kingston OR kingston)',
            '(Stonnington West OR stonnington west)',
            '(Manningham West OR manningham west)',
            '(Manningham East OR manningham east)',
            '(Whitehorse West OR whitehorse west)',
            '(Whitehorse East OR whitehorse east)',
            '(Yarra OR yarra)',
            '(Bayside OR bayside)',
            '(Stonnington East OR stonnington east)',
            '(Glen Eira OR glen eira)',
            '(Banyule OR banyule)',
            '(Nillumbik OR Kinglake OR nillumbik OR kinglake)',
            '(Whittlesea OR Wallan OR whittlesea OR wallan)',
            '(Keilor OR keilor)',
            '(Macedon Ranges OR macedon ranges)',
            '(Moreland OR Moreland North OR moreland OR moreland north)',
            '(Sunbury OR sunbury)',
            '(Tullamarine OR Broadmeadows OR tullamarine OR broadmeadows)',
            '(Knox OR knox)',
            '(Maroondah OR maroondah)',
            '(Yarra Ranges OR yarra ranges)',
            '(Cardinia OR cardinia)',
            '(Casey North OR casey north)',
            '(Casey South OR casey south)',
            '(Dandenong OR dandenong)',
            '(Monash OR monash)',
            '(Brimbank OR brimbank)',
            '(Hobsons Bay OR hobsons bay)',
            '(Maribyrnong OR maribyrnong)',
            '(Melton OR Bacchus Marsh OR melton OR bacchus marsh)',
            '(Wyndham OR wyndham)',
            '(Frankston OR frankston)',
            '(Mornington Peninsula OR mornington peninsula)']

cities = ['Creswick - Daylesford - Ballan',
          'Heathcote - Castlemaine - Kyneton',
          'Geelong',
          'Surf Coast - Bellarine Peninsula',
          'Upper Goulburn Valley',
          'Baw Baw',
          'Gippsland - South West',
          'Brunswick - Coburg',
          'Darebin - South',
          'Darebin - North',
          'Essendon',
          'Melbourne City',
          'Port Phillip',
          'Boroondara',
          'Kingston',
          'Stonnington - West',
          'Manningham - West',
          'Manningham - East',
          'Whitehorse - West',
          'Whitehorse - East',
          'Yarra',
          'Bayside',
          'Stonnington - East',
          'Glen Eira',
          'Banyule',
          'Nillumbik - Kinglake',
          'Whittlesea - Wallan',
          'Keilor',
          'Macedon Ranges',
          'Moreland - North',
          'Sunbury',
          'Tullamarine - Broadmeadows',
          'Knox',
          'Maroondah',
          'Yarra Ranges',
          'Cardinia',
          'Casey - North',
          'Casey - South',
          'Dandenong',
          'Monash',
          'Brimbank',
          'Hobsons Bay',
          'Maribyrnong',
          'Melton - Bacchus Marsh',
          'Wyndham',
          'Frankston',
          'Mornington Peninsula']

maxResults = 100
num_page = 10

results = []
for i in range(len(key_words)):
    for j in range(len(city_key)):
        # search_turn = 0
        # next_token = None
        for page in range(num_page):
            query = key_words[i] + ' ' + city_key[j] + ' -is:retweet lang:en'
            
            tweets = client.search_recent_tweets(query=query, tweet_fields=['created_at'],
                                                    max_results=maxResults)
            next_token = tweets.meta.get("next_token")
            # print(next_token)
            # search_turn += 1
            if tweets.data:
                for tweet in tweets.data:
                    tweet = dict(tweet)
                    data = {}
                    data['id'] = str(tweet['id'])
                    data['text'] = tweet['text']
                    data['time'] = str(tweet['created_at'])
                    data['place'] = cities[j]
                    data['emotion'] = str(te.get_emotion(tweet['text']))
                    results.append(data)
            if (next_token == None):
                break
        print('number of turn for ' + cities[j] + ' in every topic: ')
    
print(len(results))

save_file = open('Twitter6.json', 'w')
json.dump(results, save_file)
save_file.close()

# with open('Twitter3.json', 'w', encoding='utf-8') as f:
#     json.dump(f, results)
    # write json file