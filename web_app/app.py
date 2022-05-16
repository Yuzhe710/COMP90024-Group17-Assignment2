# ====================================
# COMP90024 Cluster and Cloud Computing
# Group 17 - Assignment 2
# Xunye Tian 1021181
# Kechen Zhao 957398
# Yuzhe Jie 1189869
# Qingyang Feng 980940
# Wentian Ding 1048673
# Last Updated: 2022-05-14
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
    return render_template('main.html')

@app.route("/aboutUs.html")
def aboutUs():
    return render_template('aboutUs.html')

@app.route("/general.html")
def general():
    return render_template('general.html')

@app.route("/house_price.html")
def housePrice():
    return render_template('house_price.html')

@app.route("/income.html")
def income():
    return render_template('income.html')

@app.route("/population.html")
def population():
    return render_template('population.html')

# --------------------------------------------
