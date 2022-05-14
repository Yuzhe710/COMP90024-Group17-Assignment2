# This file save historic twitter data into couchdb
import couchdb
import pandas as pd

masternode='172.26.132.32'
user='admin'
passeord='admin'
url = 'http://'+user+':'+passeord+'@'+masternode+':5984/'
couchclient = couchdb.Server(url)

print("successfully connected to couchdb") 

datainfo = "historic_house_price"
if couchclient.__contains__(datainfo):
    couchclient.delete(datainfo)
couchclient.create(datainfo)
db = couchclient[datainfo]

print("database created")

hostoric_house_price_path = '/Users/osako15/Desktop/UNI/MSS2/COMP90024/Ass2/COMP90024-Group17-Assignment2/Harvest/historic_twitter_data/housetwitter1.csv'

data_frame = pd.read_csv(hostoric_house_price_path)

text_list = list(data_frame['text'])
tidy_text_list = list(data_frame['tidy_text'])
polarity_score_vader_list = list(data_frame['polarity_score_vader'])
polarity_score_textblob_list = list(data_frame['polarity_score_textblob'])
label_vader_list = list(data_frame['label_vader'])
label_textblob_list = list(data_frame['label_textblob'])
coordinates_list = list(data_frame['coordinates'])


for i in range(0, len(data_frame)):
    text = str(text_list[i])
    tidy_text = str(tidy_text_list[i])
    polarity_score_vader = str(polarity_score_vader_list[i])
    polarity_score_textblob = str(polarity_score_textblob_list[i])
    label_vader = str(label_vader_list[i])
    label_textblob = str(label_textblob_list[i])
    coordinates = str(coordinates_list[i])

    db.save({"text":text, "tidy_text":tidy_text, "polarity_score_vader":polarity_score_vader, 
        "polarity_score_textblob":polarity_score_textblob, "label_vader":label_vader,
        "label_textblob":label_textblob, "coordinates":coordinates})
    # print(text)
    print(i)

# TOTAL_LINE = 2500002