import pandas as pd
import pyodbc 
import json
import logging
import os

def retrieve_songs(duration,genre,mood):
    try:
        logging.info("Reading DB settings...")
        my_app_setting_db_cred_value = os.environ["DB_CREDENTIALS"]

        logging.info("Connecting to SQL Server...")
        conn = pyodbc.connect(my_app_setting_db_cred_value)

        #Prepare SQL Query to retrive data based on Genre and Mood
        sql_query = f"SELECT * FROM SONG WHERE GENRE = '{genre}' AND +\
                      MOOD = '{mood}' ORDER BY DURATION DESC;"

        #Execute the query on SONG table
        df = pd.read_sql_query(sql_query, conn)

        #CALCULATE CUMMULATIVE SUM FOR ALL SONGS
        df['duration_cummulsum'] = df['duration'].cumsum()

        #FILTER BASED ON DURATION
        logging.info(f"Filtering the records for {duration} seconds...")
        filtered_df = df[df['duration_cummulsum']<=duration] 

        # Removed unwanted columns
        filtered_df = filtered_df[['id','title','song_url','duration']]
        result = filtered_df.to_json(orient="records")
        logging.info("Fetched result successfully")
        parsed = json.loads(result)

        return (200,json.dumps(parsed,indent=4))

    except (KeyError,TypeError,NameError) as er:
        keyerror = f'Error while reading App Setting: {er}'
        logging.error(keyerror)
        return(500,keyerror)

    except pyodbc.Error as ex:
        sqlstate = ex.args[1]
        logging.error(sqlstate)
        return(500,sqlstate)


