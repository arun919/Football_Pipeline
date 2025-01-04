from read_api import get_top_scorer,check_rate_limits
from process_api import process_top_scorers,create_dataframe
from db_coonect import ps_connect1,create_table,truncate_table,insert_table
import numpy
import os
import requests
import pandas as pd
import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":

# Define API KEY
    RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
    host="127.0.0.1"
    database="postgres"
    user="postgres"
    password="postgres"
    port="5432"

# Set up request header and authentication
    headers = {
        'X-RapidAPI-Key': RAPIDAPI_KEY,
        'X-RapidAPI-Host': 'api-football-v1.p.rapidapi.com'
    }
# Setup API URL and parameters
    url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"
    params = {"league":"39","season":"2023"}

# Query to Create Final Table
    create_table_query = """
      CREATE TABLE IF NOT EXISTS top_scorers (
        position INT,
        player VARCHAR(255),
        club VARCHAR(255),
        total_goals INT,
        penalty_goals INT,
        assists INT,
        matches INT,
        mins INT,
        PRIMARY KEY (player, club)
    );
    """

# Query to trucate the table
    truncate_table_query = """
        TRUNCATE TABLE top_scorers
    """
# Query to load data into final table
    insert_table_query = """
      INSERT INTO top_scorers (position,player,club,total_goals,penalty_goals,assists,matches,mins)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    data= get_top_scorer(url,headers,params)
    #print(data)
    if data and 'response' in data and data['response']:
        top_scorers = process_top_scorers(data)
        #print(top_scorers)
        df = create_dataframe(top_scorers)
        print(df.to_string(index=False))
    else:
         print("No data available or an error occurred ❌")

    db_connection = ps_connect1()
    #If connection is successful, proceed with creating table and inserting data
    if db_connection is not None:
        create_table(db_connection,create_table_query)
        df = create_dataframe(top_scorers)
        truncate_table(db_connection,truncate_table_query)
        insert_table(db_connection,insert_table_query,df)