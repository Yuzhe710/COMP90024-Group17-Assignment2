# ====================================
# COMP90024 Cluster and Cloud Computing
# Group 17 - Assignment 2
# Xunye Tian 1021181
# Kechen Zhao 957398
# Yuzhe Jie 1189869
# Qingyang Feng 980940
# Wentian Ding 1048673
# Last Updated: 2022-05-15
# Description: Plotting SA3 areas in the greater melbourne area
# ====================================

import couchdb
import pandas as pd
import matplotlib.pyplot as plt

def main():
    couch_client = couchdb.Server('http://admin:admin@172.26.132.32:5984/')
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
    sa3_mel = sa3.loc[income.index, ['SA3_NAME_2016']]
    sa3_mel['Melbourne'] = 1

    sa3_vic = sa3[sa3['STATE_NAME_2016'] == 'Victoria']
    full_data = sa3.merge(sa3_mel, left_index=True, right_index=True, how='left')

    fig, ax = plt.subplots(figsize = (10,10), dpi=100)
    full_data.plot(ax=ax,
        column = 'Melbourne',
        cmap = 'summer',
        edgecolor = 'black',
        linewidth=0.5,
        missing_kwds={
                "color": "lightgrey",
                "label": "No/Too few data",
            },
    );
    ax.set_xlim(142, 148)
    ax.set_ylim(-40, -36)
    ax.set_axis_off();
    ax.set_title('The Greater Melbourne Area', fontsize=18);
    plt.savefig('greater_melbourne.png')