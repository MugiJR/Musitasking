import pandas as pd
import pyodbc 
import json
import logging
import os

def retrieve_songs(duration=300):
    try:
        logging.info("Reading DB settings...")
        #my_app_setting_db_cred_value = os.environ["DB_CREDENTIALS"]
        my_app_setting_db_cred_value = "Driver={SQL Server};Server=tcp:musitasking.database.windows.net,1433;Database=musitaskingdb;Uid=elte;Pwd=admin@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        logging.info("Retrived Settings...")
        conn = pyodbc.connect(my_app_setting_db_cred_value)
        df = pd.read_sql_query('SELECT * FROM SONG ORDER BY DURATION', conn)
        #CALCULATE CUMMULATIVE SUM FOR ALL SONGS
        df['duration_cummulsum'] = df['duration'].cumsum()
        print(df)
        #FILTER BASED ON DURATION
        logging.info(f"Filtering the records for {duration} seconds...")
        filtered_df = df[df['duration_cummulsum']<=duration]
        
        # IGNORE DURATION_CUMSUM COLUMN
        #filtered_df = filtered_df[['id','title','song_url','duration']]
        filtered_df = filtered_df[['song_url']]
        print(filtered_df)
        result = filtered_df.to_json(orient="records")
        logging.info("Fetched result successfully")
        parsed = json.loads(result)
        print(json.dumps(parsed,indent=4))
        return (200,json.dumps(parsed,indent=4))

    except (KeyError,TypeError,NameError) as er:
        keyerror = f'Error while reading App Setting: {er}'
        logging.error(keyerror)
        return(500,keyerror)

    except pyodbc.Error as ex:
        sqlstate = ex.args[1]
        logging.error(sqlstate)
        return(500,sqlstate)

if __name__ == "__main__":
    retrieve_songs(900)



