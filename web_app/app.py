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

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"