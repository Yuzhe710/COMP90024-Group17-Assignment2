# Save Aurin files into couchdb

import couchdb
import json
import csv

# 3 Aurin file path
mean_income_file_path = '/Users/osako15/Desktop/UNI/MSS2/COMP90024/Ass2/COMP90024-Group17-Assignment2/Aurin_data/2014-2018_mean_income.csv'
median_house_price_file_path = '/Users/osako15/Desktop/UNI/MSS2/COMP90024/Ass2/COMP90024-Group17-Assignment2/Aurin_data/2014-2018 median_house_price.csv'
pop_and_density_file_path = '/Users/osako15/Desktop/UNI/MSS2/COMP90024/Ass2/COMP90024-Group17-Assignment2/Aurin_data/2014-2018 population_and_density.csv'

### Couchdb Setup ######
masternode='172.26.132.32'
user='admin'
passeord='admin'
url = 'http://'+user+':'+passeord+'@'+masternode+':5984/'
couchclient = couchdb.Server(url)


# ###### Save the 2014-2018 mean_income 
datainfo = "mean_income_2014-2018"
if couchclient.__contains__(datainfo):
    couchclient.delete(datainfo)
couchclient.create(datainfo)
db = couchclient[datainfo]

n = 0
with open(mean_income_file_path, 'r') as f:
     reader = csv.reader(f)
     for row in reader:
        n = n + 1
        if n == 1:
            continue
        code = row[0]
        name = row[1]
        mean_income_2014 = row[2]
        mean_income_2015 = row[3]
        mean_income_2016 = row[4]
        mean_income_2017 = row[5]
        mean_income_2018 = row[6]
        # save to db
        db.save({"code":code, "name":name, "mean_income_2014":mean_income_2014, 
        "mean_income_2015":mean_income_2015, "mean_income_2016":mean_income_2016,
        "mean_income_2017":mean_income_2017, "mean_income_2018":mean_income_2018})

print("Save mean income into couch db done")

###### Save the 2014-2018 median_house_price
# datainfo = "median_house_price_2014-2018"
# if couchclient.__contains__(datainfo):
#     couchclient.delete(datainfo)
# couchclient.create(datainfo)
# db2 = couchclient[datainfo]

# n = 0
# with open(median_house_price_file_path, 'r') as f:
#      reader = csv.reader(f)
#      for row in reader:
#         n = n + 1
#         if n == 1:
#             continue
#         code = row[0]
#         name = row[1]
#         median_price_2014 = row[2]
#         median_price_2015 = row[3]
#         median_price_2016 = row[4]
#         median_price_2017 = row[5]
#         median_price_2018 = row[6]
#         # save to db
#         db2.save({"code":code, "name":name, "median_price_2014":median_price_2014, 
#         "median_price_2015":median_price_2015, "median_price_2016":median_price_2016,
#         "median_price_2017":median_price_2017, "median_price_2018":median_price_2018})

# print("Save median house price into couch db done")

# # Save the 2014-2018 population_and_density
# datainfo = "population_and_density_2014-2018"
# if couchclient.__contains__(datainfo):
#     couchclient.delete(datainfo)
# couchclient.create(datainfo)
# db3 = couchclient[datainfo]

# n = 0
# with open(pop_and_density_file_path, 'r') as f:
#      reader = csv.reader(f)
#      for row in reader:
#         n = n + 1
#         if n == 1:
#             continue
#         code = row[0]
#         name = row[1]
#         population_2014 = row[2]
#         population_den_2014_personkm2 = row[3]
#         population_2015 = row[4]
#         population__den_2015_personkm2 = row[5]
#         population_2016 = row[6]
#         population_den_2016_personkm2 = row[7]
#         population_2017 = row[8]
#         population_den_2017_personkm2 = row[9]
#         population_2018 = row[10]
#         population_den_2018_personkm2 = row[11]
#         # save to db
#         db3.save({"code":code, "name":name, "population_2014":population_2014, 
#         "population_den_2014_personkm2":population_den_2014_personkm2, "population_2015":population_2015,
#         "population__den_2015_personkm2":population__den_2015_personkm2, "population_2016":population_2016,
#         "population_den_2016_personkm2":population_den_2016_personkm2, "population_2017":population_2017,
#         "population_den_2017_personkm2":population_den_2017_personkm2, "population_2018":population_2018,
#         "population_den_2018_personkm2":population_den_2018_personkm2})

# print("Save population and density into couch db done")