# ====================================
# COMP90024 Cluster and Cloud Computing
# Group 17 - Assignment 2
# Xunye Tian 1021181
# Kechen Zhao 957398
# Yuzhe Jie 1189869
# Qingyang Feng 980940
# Wentian Ding 1048673
# Last Updated: 2022-05-15
# Description: Exploring the correlation between emotions of twitter data and the languages used
# ====================================

import pandas as pd
import matplotlib.pyplot as plt
import couchdb
from collections import Counter
import numpy as np

# Piechart of Language Spoken at Home
couch_client = couchdb.Server('http://admin:admin@172.26.132.32:5984/')
db1 = couch_client['lang_spoken_at_home']
rows = db1.view('_all_docs', include_docs=True)
lang = pd.DataFrame([row['doc'] for row in rows])
lang = lang.drop(['_id', '_rev'], axis = 1).astype(int).set_index('sa4_code16')

# tidy up attribute names
attr_name = dict({'spks_eng_on_p': 'English', 'spks_other_lang_italian_p': 'Italian ', 'spks_other_lang_maltese_p': 'Maltese ',
'spks_other_lang_other_p': 'Other', 
'spks_other_lang_russian_p': 'Russian', 'spks_other_lang_samoan_p': 'Samoan',
'spks_other_lang_serbian_p': 'Serbian','spks_other_lang_spanish_p': 'Spanish','spks_other_lang_tamil_p': 'Tamil',
'spks_other_lang_thai_p': 'Thai','spks_other_lang_turkish_p': 'Turkish','spks_other_lang_vietnamese_p': 'Vietnamese',
#'spks_othr_lan_chin_lan_cant_p': 'Chinese languages Cantonese','spks_othr_lan_chin_lan_othr_p': 'Chinese languages Other',
#'spks_othr_lan_chin_lan_mand_p': 'Chinese languages Mandarin',
'spks_othr_lan_chin_lan_tot_p': 'Chinese languages',
 'spks_othr_lang_afrikaans_p': 'Afrikaans','spks_othr_lang_arabic_p': 'Arabic',
 'spks_othr_lang_aus_ind_lang_p': 'Australian Indigenous Languages','spks_othr_lang_croatian_p': 'Croatian',
 'spks_othr_lang_dutch_p': 'Dutch','spks_othr_lang_french_p': 'French','spks_othr_lang_german_p': 'German','spks_othr_lang_greek_p': 'Greek',
 'spks_othr_lang_japanese_p': 'Japanese','spks_othr_lang_korean_p': 'Korean',
 'spks_othr_lang_macedonian_p': 'Macedonian','spks_othr_lang_polish_p': 'Polish',
 #'sp_oth_lan_ind_ary_lan_punj_p': 'Indo Aryan Languages Punjabi','sp_oth_lan_ind_ary_lan_sinh_p': 'Indo Aryan Languages Sinhalese',
 #'sp_oth_lan_indo_ary_lan_ben_p': 'Indo Aryan Languages Bengali','sp_oth_lan_indo_ary_lan_hin_p': 'Indo Aryan Languages Hindi',
 #'sp_oth_lan_indo_ary_lan_oth_p': 'Indo Aryan Languages Other',
 'sp_oth_lan_indo_ary_lan_tot_p': 'Indo Aryan Languages',
 #'sp_oth_lan_indo_ary_lan_urd_p': 'Indo Aryan Languages Urdu',
 'sp_oth_lan_persian_ex_dari_p': 'Persian excluding Dari',
 #'sp_oth_la_se_as_au_la_fili_p': 'Southeast Asian Austronesian Languages Filipino',
 #'sp_oth_la_se_as_au_la_indo_p': 'Southeast Asian Austronesian Languages Indonesian',
 #'sp_oth_la_se_as_au_la_oth_p': 'Southeast Asian Austronesian Languages Other',
 #'sp_oth_la_se_as_au_la_tag_p': 'Southeast Asian Austronesian Languages Tagalog',
 #'tot_p': 'Total',
 'sp_oth_la_se_as_au_la_tot_p': 'Southeast Asian Austronesian Languages'
 })
 # number of people speaking each language
lang_sum = lang.sum(axis=0)
lang_counts = lang_sum[[l for l in lang_sum.index if l in attr_name]].sort_values(ascending=False)

# pie chart of english vs. top 8 langue and other
# top 8 languages spoken other than english
top_ex_english = lang_counts[[l for l in lang_counts.index if l != 'spks_other_lang_other_p' and l !='spks_eng_on_p']][:8]
labels = ['English'] + [attr_name[l] for l in top_ex_english.index] + ['Other']
sizes = [lang_counts['spks_eng_on_p']] + top_ex_english.values.tolist() + [lang_counts.sum()-top_ex_english.sum()-lang_counts['spks_eng_on_p']]
fig, ax = plt.subplots(figsize = (10,10), dpi=100)
_, labels, autopcts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax.set_title('Language Spoken at Home', fontdict={'fontsize': 18})
plt.setp(labels, **{'weight':'bold', 'fontsize':12})
plt.setp(autopcts, **{'color':'white', 'weight':'bold', 'fontsize':12})
plt.tight_layout()
plt.savefig('language_spoken_home_pie.png')

# twitter data
couch_client = couchdb.Server('http://admin:admin@172.26.132.32:5984/')
db1 = couch_client['twitter']
rows = db1.view('_all_docs', include_docs=True)
twitter = pd.DataFrame([row['doc'] for row in rows])

# language name abbreviations
LANG_ABBR = {'en': 'English', 'ar': 'Arabic', 'bn': 'Bengali', 'cs': 'Czech', 'da': 'Danish', 'de': 'German',
             'el': 'Greek', 'es': 'Spanish', 'fa': 'Persian', 'fi': 'Finnish', 'fil': 'Filipino', 'fr': 'French',
             'he': 'Hebrew', 'hi': 'Hindi', 'hu': 'Hungarian', 'in': 'Indonesian', 'id': 'Indonesian', 'it': 'Italian', 'ja': 'Japanese',
             'ko': 'Korean', 'msa': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese',
             'ro': 'Romanian', 'ru': 'Russian', 'sv': 'Swedish', 'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian',
             'ur': 'Urdu', 'vi': 'Vietnamese', 'zh-cn': 'Chinese (Simplified)', 'zh-tw': 'Chinese (Traditional)',
             'zh': 'Chinese', 'tl': 'Tagalog', 'ug': 'Uyghur', 'te':'Telugu', 'ta': 'Tamil', 'sr': 'Serbian', 'sl': 'Slovenian',
             'sd': 'Sindhi', 'si': 'Sinhala', 'sk': 'Slovak', 'ps': 'Pashto', 'pa': 'Panjabi', 'ne': 'Nepali', 'my': 'Burmese', 'ms': 'Malay',
             'zh-CN': 'Simplified Chinese', 'zh-TW': 'Traditional Chinese', 'am':'Amharic', 'ar':'Arabic', 'bg':'Bulgarian',
             'bo': 'Tibetan', 'bs': 'Bosnian', 'ca': 'Catalan', 'ckb': 'Sorani Kurdish', 'cy': 'Welsh', 'dv': 'Maldivian',
             'et': 'Estonian', 'eu': 'Basque', 'gu': 'Gujarati', 'hi-Latn': 'Latinized Hindi', 'hr': 'Croatian', 'ht': 'Haitian Creole', 
             'hy': 'Armenian', 'is': 'Icelandic', 'ka': 'Georgian', 'km': 'Khmer',
             'kn': 'Kannada', 'lo': 'Lao', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ml': 'Malayalam', 'mr':' Marathi', 'ms': 'Malay'}

twitter_lang = pd.Series(Counter(twitter['lang'])).sort_values(ascending=False)

# pie chart of language used for tweets
labels = ['English', 'Other']
sizes = [twitter_lang['en'], twitter_lang.sum()-twitter_lang['en']]
fig, ax = plt.subplots(figsize = (10,10), dpi=100)
_, labels, autopcts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', explode = (0, 0.1),
        shadow=True, startangle=90)
ax.set_title('Language used For Tweets', fontdict={'fontsize': 30})
plt.setp(labels, **{'weight':'bold', 'fontsize':20})
plt.setp(autopcts, **{'color':'white', 'weight':'bold', 'fontsize':20})
plt.tight_layout()
plt.savefig('twitter_language.png')

# barplot of languages used other than english
# top 8 languages spoken other than english
top_ex_english = twitter_lang[[l for l in twitter_lang.index if l != 'en' and l in LANG_ABBR]][:10]
fig, ax = plt.subplots(figsize = (10, 8), dpi=100)
labels = [LANG_ABBR[l] for l in top_ex_english.index]
sizes = top_ex_english.values.tolist()
plt.bar(labels, sizes)
plt.xticks(rotation=45, ha="right", fontsize=20)
plt.yticks(fontsize=20)
ax.set_ylabel('Number of Tweets', fontsize = 20)
ax.set_title('Language (Other than English) used For Tweets', fontdict={'fontsize': 30})
plt.tight_layout()
plt.savefig('twitter_language_ex_en.png', bbox_inches='tight')

# sentiment of each language
# group by language
groupedSemtiment = pd.DataFrame(twitter.groupby('lang')['general_emotion'].apply(list))
# only keep section with more than 50 data points
min_data_point = 50
groupedSemtiment= groupedSemtiment[groupedSemtiment['general_emotion'].map(lambda d: len(d)) > min_data_point]

def sentiment_percentage(labels):
    counts = Counter(labels)
    neg = counts['Negative']
    pos = counts['Positive']
    neu = counts['Neutral']
    s = len(labels)
    return np.round(np.array([pos, neu, neg])/s*100, 2)

percentages = []
for code, row in groupedSemtiment.iterrows():
    percentages.append(sentiment_percentage(row['general_emotion']))
groupedSemtiment['pos_pctg'] = [p[0] for p in percentages]
groupedSemtiment['neu_pctg'] = [p[1] for p in percentages]
groupedSemtiment['neg_pctg'] = [p[2] for p in percentages]

top_pos = groupedSemtiment['pos_pctg'].sort_values(ascending=False)[:10]
top_neg = groupedSemtiment['neg_pctg'].sort_values(ascending=False)[:10]

# barplot of percentage of positivw tweets
fig, ax = plt.subplots(figsize = (10, 8), dpi=100)
labels = [LANG_ABBR[l] for l in top_pos.index]
sizes = top_pos.values.tolist()
plt.bar(labels, sizes, color = 'maroon')
plt.xticks(rotation=45, ha="right", fontsize=20)
plt.yticks(fontsize=20)
ax.set_ylabel('% of Positve Pweets', fontsize = 20)
ax.set_title('Top 10 Lanuages With the Highest % Positive tweets', fontdict={'fontsize': 30})
plt.tight_layout()
plt.savefig('lang_top_pos.png', bbox_inches='tight')

# barplot of percentage of positivw tweets
fig, ax = plt.subplots(figsize = (10, 8), dpi=100)
labels = [LANG_ABBR[l] for l in top_neg.index]
sizes = top_neg.values.tolist()
plt.bar(labels, sizes, color = 'darkblue')
plt.xticks(rotation=45, ha="right", fontsize=20)
plt.yticks(fontsize=20)
ax.set_ylabel('% of Negative Pweets', fontsize = 20)
ax.set_title('Top 10 Lanuages With the Highest % Negative tweets', fontdict={'fontsize': 30})
plt.tight_layout()
plt.savefig('lang_top_neg.png', bbox_inches='tight')

