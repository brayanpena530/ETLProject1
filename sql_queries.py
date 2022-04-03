# DROP TABLES
songplay_table_drop = "DROP TABLE IF EXISTS songplay;"
user_table_drop = "DROP TABLE IF EXISTS user_table;"
song_table_drop = "DROP TABLE IF EXISTS song;"
artist_table_drop = "DROP TABLE IF EXISTS artist;"
time_table_drop = "DROP TABLE IF EXISTS time;"


#Create tables 
songplay_table_create = ("CREATE TABLE IF NOT EXISTS songplay (songplay_id int not null unique, start_time);")

user_table_create = ("CREATE TABLE IF NOT EXISTS user_table (user_id int primary key, first_name varchar, last_name varchar, gender varchar, level varchar);")

song_table_create = ("CREATE TABLE IF NOT EXISTS song (song_id varchar primary key, title varchar, artist varchar, year int, duration int);")

artist_table_create = ("CREATE TABLE IF NOT EXISTS artist (artist_id varchar primary key, name varchar, location varchar, latitude varchar, longitude varchar);")

time_table_create = ("CREATE TABLE IF NOT EXISTS time (hour int, day int, week_of_year int, month int, year int, weekday int);")

# INSERT RECORDS

songplay_table_insert = ("INSERT INTO songplay(timestamp, user_id, level, song_id, artist_id, session_id, location, user_agent) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);")

user_table_insert = ("INSERT INTO user_table (user_id, first_name, last_name, gender, level) VALUES (%s,%s,%s,%s,%s);")

song_table_insert = ("INSERT INTO song (song_id, title, artist_id, year, duration) VALUES (%s,%s,%s,%s,%s);")

artist_table_insert = ("INSERT INTO artist (artist_id, name, location, latitude, longitude) VALUES (%s,%s,%s,%s,%s);")


time_table_insert = ("INSERT INTO time (hour, day, week_of_year, month, year, weekday) VALUES (%s,%s,%s,%s,%s,%s);")

# FIND SONGS

song_select = ("SELECT ")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]