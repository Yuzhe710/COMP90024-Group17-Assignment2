# ====================================
# COMP90024 Cluster and Cloud Computing
# Group 17 - Assignment 2
# Xunye Tian 1021181
# Kechen Zhao 957398
# Yuzhe Jie 1189869
# Qingyang Feng 980940
# Wentian Ding 1048673
# Last Updated: 2022-05-12
# Description: Data process and plot generate for real-time stream twitter data
# ====================================

# In[3]:


import couchdb
import numpy as np
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud


# In[4]:


couch_client = couchdb.Server('http://admin:admin@172.26.132.32:5984/')
db1 = couch_client['twitter']
data = db1.view('_all_docs', include_docs=True)
twitter = pd.DataFrame(data)


# In[5]:


gen_emo = []
top_emo = []

for i in range(len(twitter)):
    instance = twitter['doc'][i]
    if len(instance) == 9:
        gen_emo.append(instance['general_emotion'])
        top_emo.append(instance['top_emotion'])


# In[6]:


sentiment = pd.DataFrame()
sentiment['general_emotion'] = gen_emo
sentiment['top_emotion'] = top_emo


# In[7]:


def sentiment_percentage(labels):
    counts = Counter(labels)
    neg = counts['Negative']
    pos = counts['Positive']
    neu = counts['Neutral']
    s = len(labels)
    return np.round(np.array([pos, neu, neg])/s*100, 2)


# In[8]:


ratio = sentiment_percentage(sentiment['general_emotion'])


# In[9]:


f = plt.figure()
plt.pie(ratio, labels = ["Negative", 'Positive', 'Neutral'], autopct = '%1.1f%%')
plt.title('Percentage of attitude in the Melbourne')
f.savefig('Percentage_of_attitude_in_Mel', bbox_inches='tight', dpi=600)


# In[10]:


negative = sentiment[sentiment['general_emotion'] == "Negative"]
positive = sentiment[sentiment['general_emotion'] == "Positive"]
neutral = sentiment[sentiment['general_emotion'] == "Neutral"]


# In[11]:


sentiment['top_emotion'].unique()


# In[12]:


def sentiment_percentage(labels):
    counts = Counter(labels)
    fear = counts['Fear']
    sad = counts['Sad']
    happy = counts['Happy']
    surprise = counts['Surprise']
    angry = counts['Angry']
    s = len(labels)
    return np.round(np.array([fear, sad, happy, surprise, angry])/s*100, 2)


# In[13]:


all_ratio = sentiment_percentage(sentiment['top_emotion'])
f = plt.figure()
plt.pie(all_ratio, labels = ['Fear', 'Sad', 'Happy', 'Surprise', 'Angry'], autopct = '%1.1f%%')
plt.title('For all attitude Percentage of top emotions in Melbourne')
f.savefig('For_all_attitude_Percentage_of_top_emotions_in_Mel', bbox_inches='tight', dpi=600)


# In[14]:


neg_ratio = sentiment_percentage(negative['top_emotion'])
pos_ratio = sentiment_percentage(positive['top_emotion'])
neu_ratio = sentiment_percentage(neutral['top_emotion'])


# In[15]:


f = plt.figure()
plt.pie(neg_ratio, labels = ['Fear', 'Sad', 'Happy', 'Surprise', 'Angry'], autopct = '%1.1f%%')
plt.title('For negative attitude Percentage of top emotions in Melbourne')
f.savefig('For_neg_attitude_Percentage_of_top_emotions_in_Mel', bbox_inches='tight', dpi=600)


# In[16]:


f = plt.figure()
plt.pie(pos_ratio, labels = ['Fear', 'Sad', 'Happy', 'Surprise', 'Angry'], autopct = '%1.1f%%')
plt.title('For positive attitude Percentage of top emotions in Melbourne')
f.savefig('For_pos_attitude_Percentage_of_top_emotions_in_Mel', bbox_inches='tight', dpi=600)


# In[17]:


f = plt.figure()
plt.pie(neu_ratio, labels = ['Fear', 'Sad', 'Happy', 'Surprise', 'Angry'], autopct = '%1.1f%%')
plt.title('For neutral attitude Percentage of top emotions in Melbourne')
f.savefig('For_neu_attitude_Percentage_of_top_emotions_in_Mel', bbox_inches='tight', dpi=600)


# In[18]:


from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

text = ' '.join(sentiment['top_emotion'])

wordcloud = WordCloud(stopwords=STOPWORDS,
                        background_color='white',
                        #width=1000,
                        #height=1000,
                        max_words=300,
                        contour_width=3,
                        contour_color='steelblue',
                    ).generate(text)

#image_colors = ImageColorGenerator(np.array(image))
#wordcloud.recolor(color_func=image_colors)
f = plt.figure()
plt.figure(figsize=[15, 15])
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Most Pervelent Emotions Towards Housing Price', fontsize=30)
plt.show()
f.savefig('WordCloud_of_Most_Pervelent_Emotions_Towards_Housing_Price', bbox_inches='tight', dpi=600)
