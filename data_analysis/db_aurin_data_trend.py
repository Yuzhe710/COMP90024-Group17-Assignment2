# ====================================
# COMP90024 Cluster and Cloud Computing
# Group 17 - Assignment 2
# Xunye Tian 1021181
# Kechen Zhao 957398
# Yuzhe Jie 1189869
# Qingyang Feng 980940
# Wentian Ding 1048673
# Last Updated: 2022-05-15
# Description: Aurin data processing
# ====================================


# In[131]:


import couchdb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[132]:


mean_income = pd.read_csv('2014-2018 mean_income.csv')
median_house_price = pd.read_csv('2014-2018 median_house_price.csv')
pop_density = pd.read_csv('2014-2018 population and density.csv')


# In[133]:


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

# In[134]:


mean_income = pd.DataFrame.transpose(mean_income)
area_name = mean_income.iloc[1]
mean_income = mean_income.rename(columns = area_name)
mean_income.columns = mean_income.iloc[3]
mean_income = mean_income.drop(['_id', '_rev', 'name', 'code'], 0)


# In[135]:


median_house_price = pd.DataFrame.transpose(median_house_price)
area_name = median_house_price.iloc[1]
median_house_price = median_house_price.rename(columns = area_name)
median_house_price.columns = median_house_price.iloc[3]
median_house_price = median_house_price.drop(['_id', '_rev', 'name', 'code'], 0)


# In[136]:


median_house_price


# In[137]:


pop_density = pd.DataFrame.transpose(pop_density)
area_name = pop_density.iloc[1]
pop_density = pop_density.rename(columns = area_name)
pop_density.columns = pop_density.iloc[3]
pop_density = pop_density.drop(['_id', '_rev', 'name', 'code'], 0)


# In[138]:


total_population = pop_density.loc[['population_2014',
                                    'population_2015',
                                    'population_2016',
                                    'population_2017',
                                    'population_2018']]


# In[139]:


density = pop_density.loc[['population_den_2014_personkm2',
                           'population__den_2015_personkm2',
                           'population_den_2016_personkm2',
                           'population_den_2017_personkm2',
                           'population_den_2018_personkm2']]


# ## Trend Analysis

# In[147]:


area = "Yarra"
area_agg = pd.DataFrame()
area_agg['mean income'] = list(mean_income[area])
area_agg['median house price'] = list(median_house_price[area])
area_agg['total population'] = list(total_population[area])
#area_agg['population density'] = list(density[area])
area_agg.index = ['2014', '2015', '2016', '2017', '2018']
area_agg = area_agg.astype(str).astype(float).astype(int)


# In[148]:


normalized_agg = (area_agg - area_agg.mean())/area_agg.std()


# In[149]:


f = plt.figure()
plt.plot(normalized_agg)
plt.ylabel('Standardized Score')
plt.xlabel('Year')
plt.title("Trend analysis of area:" + area)
plt.legend(list(normalized_agg.columns))


# In[150]:


for location in density.columns:
    area = location
    area_agg = pd.DataFrame()
    area_agg['mean income'] = list(mean_income[area])
    area_agg['median house price'] = list(median_house_price[area])
    area_agg['total population'] = list(total_population[area])
    area_agg.index = ['2014', '2015', '2016', '2017', '2018']
    area_agg = area_agg.astype(str).astype(float).astype(int)

    normalized_agg = (area_agg - area_agg.mean())/area_agg.std()

    f = plt.figure()
    plt.plot(normalized_agg)
    plt.ylabel('Standardized Score')
    plt.xlabel('Year')
    plt.title("Trend analysis of :" + area)
    plt.legend(list(normalized_agg.columns))

    f.savefig("Trend_analysis_of:_" + area, bbox_inches='tight', dpi=600)
