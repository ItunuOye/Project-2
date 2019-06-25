import pandas as pd
from flask import Flask, jsonify
import datetime as dt
import time
from data import wiki_fire_df

#Designning a Flask API based on the queries that you have just developed
app = Flask(__name__)


# Flask Routes 
#"""List all available api routes."""
@app.route("/routes") 
def routes():
    return ( 
         f"<h3>Routes:</h3></br>"
         f"- Full list of fires: /api/v1.0/wild-fires/<br/>" 
         f"- List of fires by year: /api/v1.0/wild-fires/<year><br/>"
         f"- List of fires greater from year provided to date: /api/v1.0/wildfires/greaterthan/<year><br/>"
                  ) 

@app.route("/api/v1.0/wildfires/")
def wildfires():
    data = wiki_fire_df[["Fire Year","Fire Name","County","Acres Burned"]]

    formatted_data = data.to_dict('records')
    return jsonify(formatted_data)

@app.route("/api/v1.0/wildfires/<year>")
def wildfiresbyyear(year):
    data = wiki_fire_df.loc[wiki_fire_df["Fire Year"] == int(year),["Fire Year","Fire Name","County","Acres Burned"]]

    formatted_data = data.to_dict('records')
    return jsonify(formatted_data)

@app.route("/api/v1.0/wildfires/greaterthan/<year>")
def wildfiresgreaterthanyear(year):
    data = wiki_fire_df.loc[wiki_fire_df["Fire Year"] >= int(year),["Fire Year","Fire Name","County","Acres Burned","Number of Days"]]

    formatted_data = data.to_dict('records')
    return jsonify(formatted_data)



if __name__ == "__main__":
    app.run(debug=True)