import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect
import pymysql
pymysql.install_as_MySQLdb()
import pandas as pd
from flask import Flask, jsonify
import datetime as dt
from splinter import Browser
from bs4 import BeautifulSoup
import time


Base = automap_base()
engine = create_engine('sqlite:///./data/FPA_FOD_20170508.sqlite')
Base.metadata.create_all(engine)
session = Session(engine)


# Store data in dataframe
df = pd.read_sql('SELECT fire_year,fire_name, fips_name, fire_size, stat_cause_descr, latitude, longitude, fips_code, DISCOVERY_DATE, CONT_DATE FROM Fires WHERE state == "CA" AND fire_year >= 2010 and fire_year <= 2014 and fire_size > 1000 and county <> "none"', engine)

merge_df = df.rename(index=str,columns={"FIRE_YEAR":"Fire Year","FIRE_NAME":"Fire Name","FIRE_SIZE":"Acres Burned",
                                        "STAT_CAUSE_DESCR":"Fire Cause","LATITUDE":"Latitude","LONGITUDE":"Longitude",
                                        "FIPS_CODE":"FIPS Code","FIPS_NAME":"County","DISCOVERY_DATE":"Start Date",
                                        "CONT_DATE":"Containment Date"})

merge_df = merge_df[["Fire Year","Fire Name","Acres Burned","Fire Cause","Latitude","Longitude","FIPS Code","County","Start Date","Containment Date"]]
merge_df["Number of Days"] = ""

# Web Scrapping
browser = Browser("chrome", executable_path='chromedriver.exe', headless=True)
# 2015 data
url = "https://en.wikipedia.org/wiki/2015_California_wildfires"
url = "https://en.wikipedia.org/wiki/2015_California_wildfires"
df_2015_list = pd.read_html(url)
df_2015_clean = df_2015_list[1].columns=df_2015_list[1].iloc[0]
df_2015_clean = df_2015_list[1]
df_2015_clean.drop(0,axis=0,inplace=True)
df_2015_clean.reset_index(inplace=True)
df_2015_clean.drop(["index","Notes","Ref","Km2"],axis=1,inplace=True)
df_2015_clean["Fire Year"] = 2015
df_2015_clean = df_2015_clean.rename(index=str,columns={"Name":"Fire Name","Acres":"Acres Burned"})
df_2015_clean["Fire Cause"] = ""
df_2015_clean["Latitude"] = ""
df_2015_clean["Longitude"] = ""
df_2015_clean["FIPS Code"] = ""
df_2015_clean["Number of Days"] = (pd.to_datetime(df_2015_clean["Containment Date"]) - pd.to_datetime(df_2015_clean["Start Date"])).dt.days


# 2016 data
url = "https://en.wikipedia.org/wiki/2016_California_wildfires"
df_2016_list = pd.read_html(url)
df_2016_clean = df_2016_list[1].columns=df_2016_list[1].iloc[0]
df_2016_clean = df_2016_list[1]
df_2016_clean.drop(0,axis=0,inplace=True)
df_2016_clean.reset_index(inplace=True)
df_2016_clean.drop(["index","Notes","Ref"],axis=1,inplace=True)
df_2016_clean["Fire Year"] = 2016
df_2016_clean = df_2016_clean.rename(index=str,columns={"Name":"Fire Name","Acres":"Acres Burned"})
df_2016_clean["Fire Cause"] = ""
df_2016_clean["Latitude"] = ""
df_2016_clean["Longitude"] = ""
df_2016_clean["FIPS Code"] = ""
df_2016_clean["Number of Days"] = (pd.to_datetime(df_2016_clean["Containment Date"]) - pd.to_datetime(df_2016_clean["Start Date"])).dt.days

# 2017 data
url = "https://en.wikipedia.org/wiki/2017_California_wildfires"
df_2017_list = pd.read_html(url)
df_2017_clean = df_2017_list[3].columns=df_2017_list[3].iloc[0]
df_2017_clean = df_2017_list[3]
df_2017_clean.drop(0,axis=0,inplace=True)
df_2017_clean["Start Date"] = df_2017_clean["Start Date"].astype(str) + ", 2017"
df_2017_clean["Containment Date"] = df_2017_clean["Containment Date"].astype(str) + ", 2017"
df_2017_clean.reset_index(inplace=True)
df_2017_clean.drop(["index","Notes","Ref"],axis=1,inplace=True)
df_2017_clean["Fire Year"] = 2017
df_2017_clean = df_2017_clean.rename(index=str,columns={"Name":"Fire Name","Acres":"Acres Burned"})
df_2017_clean["Fire Cause"] = ""
df_2017_clean["Latitude"] = ""
df_2017_clean["Longitude"] = ""
df_2017_clean["FIPS Code"] = ""
df_2017_clean = df_2017_clean.dropna()
df_2017_clean["Number of Days"] = (pd.to_datetime(df_2017_clean["Containment Date"]) - pd.to_datetime(df_2017_clean["Start Date"])).dt.days

# 2018 data
url = "https://en.wikipedia.org/wiki/2018_California_wildfires"
df_2018_list = pd.read_html(url)
df_2018_clean = df_2018_list[5].columns=df_2018_list[5].iloc[0]
df_2018_clean = df_2018_list[5]
df_2018_clean.drop(0,axis=0,inplace=True)
df_2018_clean.reset_index(inplace=True)
df_2018_clean.drop(["index","Notes","Ref","Status"],axis=1,inplace=True)
df_2018_clean["Fire Year"] = 2018
df_2018_clean["Fire Cause"] = ""
df_2018_clean["Latitude"] = ""
df_2018_clean["Longitude"] = ""
df_2018_clean["FIPS Code"] = ""
df_2018_clean["Number of Days"] = (pd.to_datetime(df_2018_clean["Containment date"]) - pd.to_datetime(df_2018_clean["Start date"])).dt.days

df_2018_clean = df_2018_clean.dropna()
df_2018_clean = df_2018_clean.rename(index=str,columns={"Name":"Fire Name","Acres":"Acres Burned","Containment date":"Containment Date","Start date":"Start Date"})

# merge all dataframes
wiki_fire_df = pd.concat([merge_df,df_2015_clean,df_2016_clean,df_2017_clean,df_2018_clean], ignore_index=True)

df_us_fires = pd.read_sql('SELECT FIRE_NAME, FIRE_YEAR, FIRE_SIZE, STAT_CAUSE_DESCR, LONGITUDE, LATITUDE, FIPS_CODE, FIPS_NAME FROM Fires WHERE FIRE_SIZE > 1000 AND FIPS_CODE <> "None"', engine)

def getCarolynData(fire_year):
    df_fire_season = df_us_fires[df_us_fires['FIRE_YEAR'] == int(fire_year)]
    df_fire_season.sort_values(by=["FIRE_SIZE"], ascending=False, inplace=True)
    df_fire_season['text'] = df_fire_season['FIRE_NAME'] + '<br>Fire Size ' + (df_fire_season['FIRE_SIZE']).astype(str)+' acres'

    return df_fire_season

