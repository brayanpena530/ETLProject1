import psycopg2
from configuration import conf
import os 
import glob
from sql_queries import *
import pandas as pd

#Connects to the database. Inputs are in the configurations.py file in the conf variable



def main():
    conn = psycopg2.connect(
        host=conf["host"],
        database=conf["database"],
        user=conf["user"],
        password=conf["password"]
    )
    cur = conn.cursor()
    conn.set_session(autocommit=True)

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    cur.close()
    conn.close()


def get_files(filepath):
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))
    
    return all_files


def process_song_file(cur, filepath):
    # open song file
    df =  pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[["song_id","title","artist_id","year","duration"]].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    #artist ID, name, location, latitude, and longitude
    artist_data = df[["artist_id","artist_name","artist_location","artist_latitude","artist_longitude"]].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_data(cur, conn, filepath, func):
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
    # open log file
    df =pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df["ts"], unit="ms").tolist()
    
    # insert time data records
    time_data = [t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday]
    #column_labels = ["hour","day","week of the year", "month", "year", "weekday"]
    time_df = {"hour":time_data[0], "day":time_data[1], "week of the year":time_data[2], "month of the year":time_data[3],"year":time_data[4],"weekday":time_data[5]}

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId","firstName","lastName","gender","level"]].values[0].tolist()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = []
        cur.execute(songplay_table_insert, songplay_data)


if __name__ == "__main__":
    main()