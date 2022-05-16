# Save Aurin files into couchdb

import couchdb
import json
import csv

# 3 Aurin file path
mean_income_file_path = '/Users/osako15/Desktop/UNI/MSS2/COMP90024/Ass2/COMP90024-Group17-Assignment2/Aurin_data/2014-2018_mean_income.csv'
median_house_price_file_path = '/Users/osako15/Desktop/UNI/MSS2/COMP90024/Ass2/COMP90024-Group17-Assignment2/Aurin_data/2014-2018 median_house_price.csv'
pop_and_density_file_path = '/Users/osako15/Desktop/UNI/MSS2/COMP90024/Ass2/COMP90024-Group17-Assignment2/Aurin_data/2014-2018 population_and_density.csv'
lang_spoken_at_home_file_path = '/Users/osako15/Desktop/UNI/MSS2/COMP90024/Ass2/COMP90024-Group17-Assignment2/Aurin_data/lang_spoken_at_home.csv'


### Couchdb Setup ######
masternode='172.26.132.32'
user='admin'
passeord='admin'
url = 'http://'+user+':'+passeord+'@'+masternode+':5984/'
couchclient = couchdb.Server(url)


# # ###### Save the 2014-2018 mean_income 
# datainfo = "mean_income_2014-2018"
# if couchclient.__contains__(datainfo):
#     couchclient.delete(datainfo)
# couchclient.create(datainfo)
# db = couchclient[datainfo]

# n = 0
# with open(mean_income_file_path, 'r') as f:
#      reader = csv.reader(f)
#      for row in reader:
#         n = n + 1
#         if n == 1:
#             continue
#         code = row[0]
#         name = row[1]
#         mean_income_2014 = row[2]
#         mean_income_2015 = row[3]
#         mean_income_2016 = row[4]
#         mean_income_2017 = row[5]
#         mean_income_2018 = row[6]
#         # save to db
#         db.save({"code":code, "name":name, "mean_income_2014":mean_income_2014, 
#         "mean_income_2015":mean_income_2015, "mean_income_2016":mean_income_2016,
#         "mean_income_2017":mean_income_2017, "mean_income_2018":mean_income_2018})

# print("Save mean income into couch db done")

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


# # Save the lang_spoken_at_home
datainfo = "lang_spoken_at_home"
if couchclient.__contains__(datainfo):
    couchclient.delete(datainfo)
couchclient.create(datainfo)
db4 = couchclient[datainfo]
n = 0
with open(lang_spoken_at_home_file_path, 'r') as f:
     reader = csv.reader(f)
     for row in reader:
        n = n + 1
        if n == 1:
            continue
        sp_oth_la_se_as_au_la_oth_p = row[0]
        sp_oth_lan_ind_ary_lan_sinh_p = row[1]
        spks_other_lang_thai_p = row[2]
        spks_other_lang_vietnamese_p = row[3]
        spks_othr_lang_afrikaans_p = row[4]
        spks_othr_lang_macedonian_p = row[5]
        sp_oth_la_se_as_au_la_fili_p = row[6]
        spks_othr_lan_chin_lan_othr_p = row[7]
        tot_p = row[8]
        spks_othr_lang_aus_ind_lang_p = row[9]
        sp_oth_lan_persian_ex_dari_p = row[10]
        sp_oth_lan_ind_ary_lan_punj_p = row[11]
        spks_othr_lang_korean_p = row[12]
        spks_othr_lang_croatian_p = row[13]
        spks_other_lang_spanish_p = row[14]
        spks_othr_lan_chin_lan_mand_p = row[15]
        spks_other_lang_other_p = row[16]
        spks_othr_lang_polish_p = row[17]
        sp_oth_lan_indo_ary_lan_oth_p = row[18]
        sp_oth_lan_indo_ary_lan_tot_p = row[19]
        sp_oth_lan_indo_ary_lan_hin_p = row[20]
        spks_othr_lang_french_p = row[21]
        spks_eng_on_p = row[22]
        sp_oth_la_se_as_au_la_tot_p = row[23]
        spks_othr_lang_arabic_p = row[24]
        spks_other_lang_maltese_p = row[25]
        spks_othr_lang_dutch_p = row[26]
        spks_other_lang_tamil_p = row[27]
        spks_other_lang_italian_p = row[28]
        spks_other_lang_serbian_p = row[29]
        sp_oth_lan_indo_ary_lan_urd_p = row[30]
        spks_othr_lan_chin_lan_tot_p = row[31]
        sp_oth_la_se_as_au_la_indo_p = row[32]
        spks_other_lang_turkish_p = row[33]
        spks_other_lang_russian_p = row[34]
        sa4_code16 = row[35]
        spks_othr_lang_greek_p = row[36]
        sp_oth_la_se_as_au_la_tag_p = row[37]
        spks_othr_lan_chin_lan_cant_p = row[38]
        sp_oth_lan_indo_ary_lan_ben_p = row[39]
        spks_other_lang_samoan_p = row[40]
        spks_othr_lang_german_p = row[41]
        spks_othr_lang_japanese_p = row[42]

        
        # save to db
        db4.save({"sp_oth_la_se_as_au_la_oth_p":sp_oth_la_se_as_au_la_oth_p, 
                  "sp_oth_lan_ind_ary_lan_sinh_p":sp_oth_lan_ind_ary_lan_sinh_p, 
                  "spks_other_lang_thai_p":spks_other_lang_thai_p,
                  "spks_other_lang_vietnamese_p":spks_other_lang_vietnamese_p,
                  "spks_othr_lang_afrikaans_p":spks_othr_lang_afrikaans_p,
                  "spks_othr_lang_macedonian_p":spks_othr_lang_macedonian_p,
                  "sp_oth_la_se_as_au_la_fili_p":sp_oth_la_se_as_au_la_fili_p,
                  "spks_othr_lan_chin_lan_othr_p":spks_othr_lan_chin_lan_othr_p,
                  "tot_p":tot_p,
                  "spks_othr_lang_aus_ind_lang_p":spks_othr_lang_aus_ind_lang_p,
                  "sp_oth_lan_persian_ex_dari_p":sp_oth_lan_persian_ex_dari_p,
                  "sp_oth_lan_ind_ary_lan_punj_p":sp_oth_lan_ind_ary_lan_punj_p,
                  "spks_othr_lang_korean_p":spks_othr_lang_korean_p,
                  "spks_othr_lang_croatian_p":spks_othr_lang_croatian_p,
                  "spks_other_lang_spanish_p":spks_other_lang_spanish_p,
                  "spks_othr_lan_chin_lan_mand_p":spks_othr_lan_chin_lan_mand_p,
                  "spks_other_lang_other_p":spks_other_lang_other_p,
                  "spks_othr_lang_polish_p":spks_othr_lang_polish_p,
                  "sp_oth_lan_indo_ary_lan_oth_p":sp_oth_lan_indo_ary_lan_oth_p,
                  "sp_oth_lan_indo_ary_lan_tot_p":sp_oth_lan_indo_ary_lan_tot_p,
                  "sp_oth_lan_indo_ary_lan_hin_p":sp_oth_lan_indo_ary_lan_hin_p,
                  "spks_othr_lang_french_p":spks_othr_lang_french_p,
                  "spks_eng_on_p":spks_eng_on_p,
                  "sp_oth_la_se_as_au_la_tot_p":sp_oth_la_se_as_au_la_tot_p,
                  "spks_othr_lang_arabic_p":spks_othr_lang_arabic_p,
                  "spks_other_lang_maltese_p":spks_other_lang_maltese_p,
                  "spks_othr_lang_dutch_p":spks_othr_lang_dutch_p,
                  "spks_other_lang_tamil_p":spks_other_lang_tamil_p,
                  "spks_other_lang_italian_p":spks_other_lang_italian_p,
                  "spks_other_lang_serbian_p":spks_other_lang_serbian_p,
                  "sp_oth_lan_indo_ary_lan_urd_p":sp_oth_lan_indo_ary_lan_urd_p,
                  "spks_othr_lan_chin_lan_tot_p":spks_othr_lan_chin_lan_tot_p,
                  "sp_oth_la_se_as_au_la_indo_p":sp_oth_la_se_as_au_la_indo_p,
                  "spks_other_lang_turkish_p":spks_other_lang_turkish_p,
                  "spks_other_lang_russian_p":spks_other_lang_russian_p,
                  "sa4_code16":sa4_code16,
                  "spks_othr_lang_greek_p":spks_othr_lang_greek_p,
                  "sp_oth_la_se_as_au_la_tag_p":sp_oth_la_se_as_au_la_tag_p,
                  "spks_othr_lan_chin_lan_cant_p":spks_othr_lan_chin_lan_cant_p,
                  "sp_oth_lan_indo_ary_lan_ben_p":sp_oth_lan_indo_ary_lan_ben_p,
                  "spks_other_lang_samoan_p":spks_other_lang_samoan_p,
                  "spks_othr_lang_german_p":spks_othr_lang_german_p,
                  "spks_othr_lang_japanese_p":spks_othr_lang_japanese_p})

print("Save lang spoken at home into couch db done")