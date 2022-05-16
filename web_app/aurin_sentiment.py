# ====================================
# COMP90024 Cluster and Cloud Computing
# Group 17 - Assignment 2
# Xunye Tian 1021181
# Kechen Zhao 957398
# Yuzhe Jie 1189869
# Qingyang Feng 980940
# Wentian Ding 1048673
# Last Updated: 2022-05-15
# Description: Plotting of correlation between sentiments of twitter data and indicator statistics from AURIN
# ====================================

import couchdb
import numpy as np
import pandas as pd
import re
from shapely.geometry import Point
import matplotlib.pyplot as plt

couch_client = couchdb.Server('http://admin:admin@172.26.132.32:5984/')
db1 = couch_client['median_house_price_2014-2018']
rows = db1.view('_all_docs', include_docs=True)
house = [row['doc'] for row in rows]
median_house_price = pd.DataFrame(house)
median_house_price['code'] = median_house_price['code'].astype(int)
median_house_price = median_house_price.set_index('code')

db2 = couch_client['mean_income_2014-2018']
rows = db2.view('_all_docs', include_docs=True)
income = [row['doc'] for row in rows]
mean_income = pd.DataFrame(income)
mean_income['code'] = mean_income['code'].astype(int)
mean_income = mean_income.set_index('code')

db3 = couch_client['population_and_density_2014-2018']
rows = db3.view('_all_docs', include_docs=True)
pop = [row['doc'] for row in rows]
pop_density = pd.DataFrame(pop)
pop_density['code'] = pop_density['code'].astype(int)
pop_density = pop_density.set_index('code')

couch_client = couchdb.Server('http://admin:admin@172.26.132.32:5984/')
db1 = couch_client['historic_house_price']
rows = db1.view('_all_docs', include_docs=True)
house = [row['doc'] for row in rows]
historic_house_price = pd.DataFrame(house)

db2 = couch_client['mean_income_2014-2018']
rows = db2.view('_all_docs', include_docs=True)
income = [row['doc'] for row in rows]
income = pd.DataFrame(income)
income.index = income['code'].astype(int)

# Load SA3 shape files
# Statistical Area Level 3 (SA3) ASGS Ed 2016 Digital Boundaries in MapInfo Interchange Format
import geopandas as gpd
sa3 = gpd.read_file('https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_sa3_2016_aust_midmif.zip&1270.0.55.001&Data%20Cubes&31ACD8D865DE06E5CA257FED00144DEE&0&July%202016&12.07.2016&Latest')
sa3['SA3_CODE_2016'] = sa3['SA3_CODE_2016'].astype(int)
sa3 = sa3.set_index('SA3_CODE_2016')
sa3_mel = sa3.loc[income.index, ['geometry']]

historic_house_price = historic_house_price.drop('geo_param',1)

cord = []
get = 0
for i in range(len(historic_house_price)):
    cord2 = re.findall("-\d+\.\d+", str(historic_house_price['coordinates'][i]))
    cord1 = re.findall("\d+\.\d+", str(historic_house_price['coordinates'][i]))

    cord.append((cord1 ,cord2))

# assign geo location
geo_code = []
for i in range(len(historic_house_price)):
    if (cord[i][0] == []) is False and (cord[i][1] == []) is False:
        point = Point(float(cord[i][0][0]), float(cord[i][1][0]))
        find = False
        for code, row in sa3_mel.iterrows():
        #for poly in sa3_mel['geometry']:
            poly = row['geometry']
            if poly.contains(point) == True:
                geo_code.append(code)
                find = True
                break
        if find == False:
            geo_code.append('Not found')
    else:
        geo_code.append('Not found')
historic_house_price['geo_code'] = geo_code

# sentiment by SA3
from collections import Counter
import numpy as np
def sentiment_percentage(labels):
    counts = Counter(labels)
    neg = counts['negative']
    pos = counts['positive']
    neu = counts['neutral']
    s = len(labels)
    return np.round(np.array([pos, neu, neg])/s*100, 2)

grouped_SA3 = pd.DataFrame(historic_house_price.groupby('geo_code')['label_textblob'].apply(list))
# only keep section with more than 5 data points
min_data_point = 50
grouped_SA3= grouped_SA3[grouped_SA3['label_textblob'].map(lambda d: len(d)) > min_data_point]
percentages = []
for code, row in grouped_SA3.iterrows():
    percentages.append(sentiment_percentage(row['label_textblob']))
grouped_SA3['pos_pctg'] = [p[0] for p in percentages]
grouped_SA3['neu_pctg'] = [p[1] for p in percentages]
grouped_SA3['neg_pctg'] = [p[2] for p in percentages]

full_data = sa3_mel.merge(grouped_SA3, left_index=True, right_index=True, how='left')

# remove nan in pair of data
def remove_nan(x, y):
    new_x = []
    new_y = []
    for i in range(len(x)):
        if (not np.isnan(x[i])) and (not np.isnan(y[i])):
            new_x.append(x[i])
            new_y.append(y[i])
    return np.array(new_x), np.array(new_y)

# avg house price vs. pos percentage
median_house_price['avg_med_hp'] = (median_house_price.median_price_2014.values.astype(float) +
                                    median_house_price.median_price_2015.values.astype(float) +
                                    median_house_price.median_price_2016.values.astype(float) +
                                    median_house_price.median_price_2017.values.astype(float) +
                                    median_house_price.median_price_2018.values.astype(float))/5
hp_sentiment = median_house_price.merge(full_data, left_index=True, right_index=True, how='left')

# plot
fig, ax = plt.subplots(1, 3, figsize = (17,5), dpi=100)
x0, y0 = remove_nan(hp_sentiment['avg_med_hp'].values/1000000, hp_sentiment['pos_pctg'].values)
ax[0].scatter(x0, y0, color = 'maroon')
ax[0].plot(x0, np.polyval(np.polyfit(x0, y0, 1), x0), color = 'maroon')
ax[0].tick_params(axis='both', which='major', labelsize=12)
ax[0].set_ylabel('Percentage of Positive Tweets (%)', fontsize = 12)
ax[0].set_xlabel('Average Median House Price (Million)', fontsize = 12)
ax[0].set_ylim(30, 50)

x1, y1 = remove_nan(hp_sentiment['avg_med_hp'].values/1000000, hp_sentiment['neu_pctg'].values)
ax[1].scatter(x1, y1, color = 'seagreen')
ax[1].plot(x1, np.polyval(np.polyfit(x1, y1, 1), x1), color = 'seagreen')
ax[1].tick_params(axis='both', which='major', labelsize=12)
ax[1].set_ylabel('Percentage of Negative Tweets (%)', fontsize = 12)
ax[1].set_xlabel('Average Median House Price (Million)', fontsize = 12)
ax[1].set_ylim(35, 55)

x2, y2 = remove_nan(hp_sentiment['avg_med_hp'].values/1000000, hp_sentiment['neg_pctg'].values)
ax[2].scatter(x2, y2, color = 'darkblue')
ax[2].plot(x2, np.polyval(np.polyfit(x2, y2, 1), x2), color = 'darkblue')
ax[2].tick_params(axis='both', which='major', labelsize=12)
ax[2].set_ylabel('Percentage of Negative Tweets (%)', fontsize = 12)
ax[2].set_xlabel('Average Median House Price (Million)', fontsize = 12)
ax[2].set_ylim(5, 25)
fig.suptitle('Correlation Between House Price and Twitter Emotions', fontsize = 20)
plt.savefig('./static/images/hp_emotion.png')

# mean income vs. pos percentage
mean_income['avg_mean_income'] = (mean_income.mean_income_2014.values.astype(float) +
                                    mean_income.mean_income_2015.values.astype(float) +
                                    mean_income.mean_income_2016.values.astype(float) +
                                    mean_income.mean_income_2017.values.astype(float) +
                                    mean_income.mean_income_2018.values.astype(float))/5
income_sentiment = mean_income.merge(full_data, left_index=True, right_index=True, how='left')

# plot
fig, ax = plt.subplots(1, 3, figsize = (17,5), dpi=100)

x0, y0 = remove_nan(income_sentiment['avg_mean_income'].values/1000, income_sentiment['pos_pctg'].values)
ax[0].scatter(x0, y0, color = 'maroon')
ax[0].plot(x0, np.polyval(np.polyfit(x0, y0, 1), x0), color = 'maroon')
ax[0].tick_params(axis='both', which='major', labelsize=12)
ax[0].set_ylabel('Percentage of Positive Tweets (%)', fontsize = 12)
ax[0].set_xlabel('Average Mean Income (Thousand)', fontsize = 12)
ax[0].set_ylim(30, 50)

x1, y1 = remove_nan(income_sentiment['avg_mean_income'].values/1000, income_sentiment['neu_pctg'].values)
ax[1].scatter(x1, y1, color = 'seagreen')
ax[1].plot(x1, np.polyval(np.polyfit(x1, y1, 1), x1), color = 'seagreen')
ax[1].tick_params(axis='both', which='major', labelsize=12)
ax[1].set_ylabel('Percentage of Negative Tweets (%)', fontsize = 12)
ax[1].set_xlabel('Average Mean Income (Thousand)', fontsize = 12)
ax[1].set_ylim(30, 50)

x2, y2 = remove_nan(income_sentiment['avg_mean_income'].values/1000, income_sentiment['neg_pctg'].values)
ax[2].scatter(x2, y2, color = 'darkblue')
ax[2].plot(x2, np.polyval(np.polyfit(x2, y2, 1), x2), color = 'darkblue')
ax[2].tick_params(axis='both', which='major', labelsize=12)
ax[2].set_ylabel('Percentage of Negative Tweets (%)', fontsize = 12)
ax[2].set_xlabel('Average Mean Income (Thousand)', fontsize = 12)
ax[2].set_ylim(0, 20)
fig.suptitle('Correlation Between Income and Twitter Emotions', fontsize = 20)
plt.savefig('./static/images/income_emotion.png')

# population density vs. pos percentage
pop_density['avg_pop_den'] = (pop_density.population_den_2014_personkm2.values.astype(float) +
                                pop_density.population__den_2015_personkm2.values.astype(float) +
                                pop_density.population_den_2016_personkm2.values.astype(float) +
                                pop_density.population_den_2017_personkm2.values.astype(float) +
                                pop_density.population_den_2018_personkm2.values.astype(float))/5
popDen_sentiment = pop_density.merge(full_data, left_index=True, right_index=True, how='left')

# plot
fig, ax = plt.subplots(1, 3, figsize = (17,5), dpi=100)
x0, y0 = remove_nan(popDen_sentiment['avg_pop_den'].values/1000, popDen_sentiment['pos_pctg'].values)
ax[0].scatter(x0, y0, color = 'maroon')
ax[0].plot(x0, np.polyval(np.polyfit(x0, y0, 1), x0), color = 'maroon')
ax[0].tick_params(axis='both', which='major', labelsize=12)
ax[0].set_ylabel('Percentage of Positive Tweets (%)', fontsize = 12)
ax[0].set_xlabel('Average Population Density (Thousand person / $km^2$)', fontsize = 12)
ax[0].set_ylim(30, 50)

x1, y1 = remove_nan(popDen_sentiment['avg_pop_den'].values/1000, popDen_sentiment['neu_pctg'].values)
ax[1].scatter(x1, y1, color = 'seagreen')
ax[1].plot(x1, np.polyval(np.polyfit(x1, y1, 1), x1), color = 'seagreen')
ax[1].tick_params(axis='both', which='major', labelsize=12)
ax[1].set_ylabel('Percentage of Negative Tweets (%)', fontsize = 12)
ax[1].set_xlabel('Average Population Density (Thousand person / $km^2$)', fontsize = 12)
ax[1].set_ylim(30, 50)

x2, y2 = remove_nan(popDen_sentiment['avg_pop_den'].values/1000, popDen_sentiment['neg_pctg'].values)
ax[2].scatter(x2, y2, color = 'darkblue')
ax[2].plot(x2, np.polyval(np.polyfit(x2, y2, 1), x2), color = 'darkblue')
ax[2].tick_params(axis='both', which='major', labelsize=12)
ax[2].set_ylabel('Percentage of Negative Tweets (%)', fontsize = 12)
ax[2].set_xlabel('Average Population Density (Thousand person / $km^2$)', fontsize = 12)
ax[2].set_ylim(5, 25)
fig.suptitle('Correlation Between Population Density and Twitter Emotions', fontsize = 20)
plt.savefig('./static/images/popDen_emotion.png')