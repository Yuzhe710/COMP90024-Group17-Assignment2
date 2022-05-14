import csv
import json

house_price_path = '/Users/osako15/Desktop/UNI/MSS2/COMP90024/Ass2/COMP90024-Group17-Assignment2/Harvest/historic_twitter_data/housetwitter1.csv'
house_price_json_path = '/Users/osako15/Desktop/UNI/MSS2/COMP90024/Ass2/COMP90024-Group17-Assignment2/Harvest/historic_twitter_data/housetwitter1.json'

data = []

n = 0

with open(house_price_path, encoding='utf-8') as f:
    csvReader = csv.DictReader(f)

    for rows in csvReader:
        # key = rows['text']
        data.append(rows)
        # print(rows)
        # break

with open(house_price_json_path, 'w', encoding='utf-8') as jsonf:
    jsonf.write(json.dumps(data))