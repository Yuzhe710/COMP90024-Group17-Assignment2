# ====================================
# COMP90024 Cluster and Cloud Computing
# Group 17 - Assignment 2
# Xunye Tian 1021181
# Kechen Zhao 957398
# Yuzhe Jie 1189869
# Qingyang Feng 980940
# Wentian Ding 1048673
# Last Updated: 2022-05-15
# Description: Aurin Data process and plot generate
# ====================================
# In[98]:


import couchdb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[99]:


couch_client = couchdb.Server('http://admin:admin@172.26.132.32:5984/')
db1 = couch_client['median_house_price_2014-2018']
rows = db1.view('_all_docs', include_docs=True)
house = [row['doc'] for row in rows]
median_house_price = pd.DataFrame(house)

db2 = couch_client['mean_income_2014-2018']
rows = db2.view('_all_docs', include_docs=True)
income = [row['doc'] for row in rows]
mean_income = pd.DataFrame(income)

db3 = couch_client['population_and_density_2014-2018']
rows = db3.view('_all_docs', include_docs=True)
pop = [row['doc'] for row in rows]
pop_density = pd.DataFrame(pop)


# ## Pre-Processing

# In[100]:


mean_income = pd.DataFrame.transpose(mean_income)
area_name = mean_income.iloc[1]
mean_income = mean_income.rename(columns = area_name)
mean_income.columns = mean_income.iloc[3]
mean_income = mean_income.drop(['_id', '_rev', 'name', 'code'], 0)


# In[101]:


median_house_price = pd.DataFrame.transpose(median_house_price)
area_name = median_house_price.iloc[1]
median_house_price = median_house_price.rename(columns = area_name)
median_house_price.columns = median_house_price.iloc[3]
median_house_price = median_house_price.drop(['_id', '_rev', 'name', 'code'], 0)


# In[102]:


pop_density = pd.DataFrame.transpose(pop_density)
area_name = pop_density.iloc[1]
pop_density = pop_density.rename(columns = area_name)
pop_density.columns = pop_density.iloc[3]
pop_density = pop_density.drop(['_id', '_rev', 'name', 'code'], 0)


# In[103]:


total_population = pop_density.loc[['population_2014',
                                    'population_2015',
                                    'population_2016',
                                    'population_2017',
                                    'population_2018']]


# In[104]:


density = pop_density.loc[['population_den_2014_personkm2',
                           'population__den_2015_personkm2',
                           'population_den_2016_personkm2',
                           'population_den_2017_personkm2',
                           'population_den_2018_personkm2']]


# ## Trend Analysis

# In[105]:


area = "Yarra"
area_agg = pd.DataFrame()
area_agg['mean income'] = list(mean_income[area])
area_agg['median house price'] = list(median_house_price[area])
area_agg['total population'] = list(total_population[area])
area_agg.index = ['2014', '2015', '2016', '2017', '2018']
area_agg = area_agg.astype(str).astype(float).astype(int)


# In[106]:


plt.bar(area_agg.index, area_agg['median house price'], color = 'pink', width = 0.4)
plt.plot(area_agg['median house price'], marker = '*', color = 'orange', ms = 10)
plt.title('Median House Price of: ' + area)


# In[107]:


for location in density.columns:
    area = location
    area_agg = pd.DataFrame()
    area_agg['mean income'] = list(mean_income[area])
    area_agg['median house price'] = list(median_house_price[area])
    area_agg['population'] = list(total_population[area])
    area_agg.index = ['2014', '2015', '2016', '2017', '2018']
    area_agg = area_agg.astype(str).astype(float).astype(int)

    f1 = plt.figure()
    plt.bar(area_agg.index, area_agg['mean income'], color = 'pink', width = 0.4)
    plt.plot(area_agg['mean income'], marker = '*', color = 'orange', ms = 10)
    plt.title('Mean income of: ' + area)
    f1.savefig("Mean_income_of:_" + area, bbox_inches='tight', dpi=600)

    f2 = plt.figure()
    plt.bar(area_agg.index, area_agg['median house price'], color = 'pink', width = 0.4)
    plt.plot(area_agg['median house price'], marker = '*', color = 'orange', ms = 10)
    plt.title('Median House Price of: ' + area)
    f2.savefig("Median_House_Price_of:_" + area, bbox_inches='tight', dpi=600)

    f3 = plt.figure()
    plt.bar(area_agg.index, area_agg['population'], color = 'pink', width = 0.4)
    plt.plot(area_agg['population'], marker = '*', color = 'orange', ms = 10)
    plt.title('Population of: ' + area)
    f3.savefig("Population_of:_" + area, bbox_inches='tight', dpi=600)

#     f.savefig("Trend_analysis_of:_" + area, bbox_inches='tight', dpi=600)
