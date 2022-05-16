# ====================================
# COMP90024 Cluster and Cloud Computing
# Group 17 - Assignment 2
# Xunye Tian 1021181
# Kechen Zhao 957398
# Yuzhe Jie 1189869
# Qingyang Feng 980940
# Wentian Ding 1048673
# Last Updated: 2022-05-15
# Description: Twitter historical house price data processing and plotting of choropleths on sentiments of twitter data
# ====================================

import couchdb
import numpy as np
import pandas as pd
import re
from shapely.geometry import Point
import matplotlib.pyplot as plt

def main():
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

    def plot_percentage(data, hue, cmap, title, filename):
        fig, ax = plt.subplots(figsize = (10,10), dpi=100)
        data.plot(ax=ax,
            column=hue,
            legend=True,
            scheme='quantiles',#'UserDefined',
            #classification_kwds = {"bins":[20, 40, 60, 80, 100]},
            cmap = cmap,
            edgecolor = 'black',
            linewidth=0.3,
            missing_kwds={
                "color": "lightgrey",
                "label": "No/Too few data",
            },
        );
        ax.set_axis_off();
        ax.set_title(title, fontsize=18);
        plt.savefig(filename)

    plot_percentage(full_data, 'pos_pctg', 'Reds', 'Attitude towards House Price - Percentage of Positive Tweets', 'sentiment_cp_pos.png')
    plot_percentage(full_data, 'neu_pctg', 'YlOrBr', 'Attitude towards House Price - Percentage of Neutral Tweets', 'sentiment_cp_neu.png')
    plot_percentage(full_data, 'neg_pctg', 'Blues', 'Attitude towards House Price - Percentage of Negative Tweets', 'sentiment_cp_neg.png')

    data_points = sa3_mel.merge(pd.DataFrame(historic_house_price.groupby('geo_code')['label_textblob'].count()),
                                left_index=True, right_index=True, how='left')
    fig, ax = plt.subplots(figsize = (10,10), dpi=100)
    data_points.plot(ax=ax,
        column='label_textblob',
        legend=True,
        scheme='quantiles',
        cmap = 'Greens',
        edgecolor = 'black',
        linewidth=0.3,
        missing_kwds={
            "color": "lightgrey",
            "label": "No data",
        },
    );
    ax.set_axis_off();
    ax.set_title('Number of Data Points in SA3 Areas', fontsize=18);
    plt.savefig('sentiment_data_point.png')
