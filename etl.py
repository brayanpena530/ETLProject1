import psycopg2
from configuration import conf
import os 
import glob
from sql_queries import *
import pandas as pd

def main():
    """
    Description: this is the main method where the connection of to the database is made and the other methods are called from this point.
    First the connection is started and then the song data is processed followed by the log data. After that the connection to the db is closed. 
    The configurations to connect to the database is taken from the configuration.py file, where the variable conf hold the necessary values

    Arguments: 
        None
    
    Returns:
        None
    """

    #Connecting to the database, conf variable taken from file configuration.py
    conn = psycopg2.connect(
        host=conf["host"],
        database=conf["database"],
        user=conf["user"],
        password=conf["password"]
    )
    cur = conn.cursor()

    #processing data
    process_data(cur, conn, filepath='data/data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/data/log_data', func=process_log_file)

    #closing the database connection
    cur.close()
    conn.close()


def get_files(filepath):
    """
     Description: This function is responsible for obtaining all the files that are found under a given directory

    Arguments:
        filepath: log data or song data file path.
        
    Returns:
        all_files: list of files 
    
    """
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))
    
    return all_files


def process_song_file(cur, filepath):
    """
    Description: This function is responsible for processing the song data and then execiting the ingestion process 
    for each file and saves it in the database 

    Arguments:
        cur: the cursor object 
        filepath: song data filepath 

    Returns:
        None
    """
    # open song file
    df =  pd.read_json(filepath, lines=True)

    song_data = df[["song_id","title","artist_id","year","duration"]].values[0].tolist()

    # insert song record
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    #artist ID, name, location, latitude, and longitude
    artist_data = df[["artist_id","artist_name","artist_location","artist_latitude","artist_longitude"]].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_data(cur, conn, filepath, func):
    """
    Description: This function is responsible for listing the files in a directory,
    and then executing the ingest process for each file according to the function
    that performs the transformation to save it to the database.

    Arguments:
        cur: the cursor object.
        conn: connection to the database.
        filepath: log data or song data file path.
        func: function that transforms the data and inserts it into the database.

    Returns:
        None
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def process_log_file(cur, filepath):
    """
    Description: This function is responsible for processing the log data and then execiting the ingestion process 
    for each file and saves it in the database 

    Arguments:
        cur: the cursor object 
        filepath: log data filepath 

    Returns:
        None
    """

    # open log file
    df =pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df["ts"], unit="ms")
    
    # insert time data records
    time_data = [t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday, t]
    #column_labels = ["hour","day","week of the year", "month", "year", "weekday"]
    time_df = pd.DataFrame.from_dict({"hour":time_data[0], "day":time_data[1], "week of the year":time_data[2], "month of the year":time_data[3],"year":time_data[4],"weekday":time_data[5], "start_time": time_data[6]})

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user data
    user_df = df[["userId","firstName","lastName","gender","level"]]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, [row.song, row.artist])
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [pd.to_datetime(row.ts, unit="ms"), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)


if __name__ == "__main__":
    main()