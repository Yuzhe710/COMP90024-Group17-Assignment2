# ====================================
# COMP90024 Cluster and Cloud Computing
# Group 17 - Assignment 2
# Xunye Tian 1021181
# Kechen Zhao 957398
# Yuzhe Jie 1189869
# Qingyang Feng 980940
# Wentian Ding 1048673
# Last Updated: 2022-05-16
# Description: main flask web app to visiualize data
# ====================================

from flask import Flask
from flask import render_template
from flask import request
from datetime import timedelta

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds = 1)

# --------------------------------------------

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/main.html", methods = ['GET', 'POST'])
def main():
    # greater_melbourne
    return render_template('main.html')

# pie chart
@app.route("/general.html")
def general():
    # db_stream_data 5 images
    return render_template('general.html')

# map
@app.route("/region.html")
def region():
    # db_historial_house_data 4 images
    return render_template('region.html')

@app.route("/house_price.html")
def housePrice():
    # aurin_sentiment 1/3 images 
    # db_aurin_data_trend 3 images
    return render_template('house_price.html')

@app.route("/income.html")
def income():
    # aurin_sentiment 1/3 images 
    # db_aurin_data_trend 3 images
    return render_template('income.html')

@app.route("/population.html")
def population():
    # aurin_sentiment 1/3 images 
    # db_aurin_data_trend 3 images
    return render_template('population.html')

@app.route("/language.html")
def language():
    # language.py
    return render_template('language.html')

# --------------------------------------------
