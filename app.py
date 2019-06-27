import pandas as pd
from flask import Flask, jsonify
import datetime as dt
import time
from data import wiki_fire_df

#Designning a Flask API based on the queries that you have just developed
app = Flask(__name__)


# Flask Routes 
#"""List all available api routes."""


if __name__ == "__main__":
    app.run(debug=True)