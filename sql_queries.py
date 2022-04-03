# DROP TABLES
songplay_table_drop = "DROP TABLE IF EXISTS songplay;"
user_table_drop = "DROP TABLE IF EXISTS user_table;"
song_table_drop = "DROP TABLE IF EXISTS song;"
artist_table_drop = "DROP TABLE IF EXISTS artist;"
time_table_drop = "DROP TABLE IF EXISTS time;"


#Create tables 
songplay_table_create = (
    """
    CREATE TABLE IF NOT EXISTS songplay (songplay_id serial primary key, start_time timestamp, user_id int, 
level varchar, song_id varchar, artist_id varchar, session_id int, location varchar, user_agent varchar,
foreign key (user_id) references user_table (user_id),
foreign key (song_id) references song (song_id),
foreign key (artist_id) references artist (artist_id))
"""
)

user_table_create = ("CREATE TABLE IF NOT EXISTS user_table (user_id int primary key, first_name varchar, last_name varchar, gender varchar, level varchar);")

song_table_create = ("CREATE TABLE IF NOT EXISTS song (song_id varchar primary key, title varchar, artist_id varchar, year int, duration int);")

artist_table_create = ("CREATE TABLE IF NOT EXISTS artist (artist_id varchar primary key, name varchar, location varchar, latitude varchar, longitude varchar);")

time_table_create = ("CREATE TABLE IF NOT EXISTS time (start_time timestamp, hour int, day int, week_of_year int, month int, year int, weekday int);")

# INSERT RECORDS

songplay_table_insert = ("INSERT INTO songplay(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);")

user_table_insert = ("INSERT INTO user_table (user_id, first_name, last_name, gender, level) VALUES (%s,%s,%s,%s,%s);")

song_table_insert = ("INSERT INTO song (song_id, title, artist_id, year, duration) VALUES (%s,%s,%s,%s,%s);")

artist_table_insert = ("INSERT INTO artist (artist_id, name, location, latitude, longitude) VALUES (%s,%s,%s,%s,%s);")

time_table_insert = ("INSERT INTO time (hour, day, week_of_year, month, year, weekday, start_time) VALUES (%s,%s,%s,%s,%s,%s,%s);")

# FIND SONGS

song_select = ("select song_id, song.artist_id from song join artist on song.artist_id = artist.artist_id where title=%s and name=%s;")

# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

#Check if song has already been added
song_check=("select * from song where song_id=%s")
artist_check=("select * from artist where artist_id=%s")
user_check=("select * from user_table where user_id=%s")