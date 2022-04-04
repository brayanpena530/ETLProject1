# Data Modeling with Postgres

## Introduction

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

I have been tasked to create a postgres database with tables to optimize queries on song play analysis. My role being to create a database schema and ETL pipeline for the analysis. 

## Database design

For the database design I will using a star schema design with 5 tables. 

### Fact Table
__songplays__ - records in log data associated with song plays i.e. records with page NextSong
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

### Dimension Tables
__users__ - users in the app
user_id, first_name, last_name, gender, level

__songs__ - songs in music database
song_id, title, artist_id, year, duration

__artists__ - artists in music database
artist_id, name, location, latitude, longitude

__time__ - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday


## Files in the repository

There are 3 main python files in the repository. The first being the configuration file which stores the configuration details to connect to the database under a variable
called conf so that it can be referenced later on. The second is the create_tables file which drops the tables in the database if they exist and recreates them. Lastly is the ETL 
file which is where the ingestion logic is executed. Additionally the data is stored under the file path data/data.

## How to run python script

First ensure that the database name sparkify is already been created in your local enviroment. Additionally modify the conf variable in configuration.py with the 
necessary details.

```python
conf={
    "host":"localhost",
    "database":"sparkifydb",
    "user":"", #put user name here
    "password":"" #put password here
}
```

After that, the create_table.py can be run to create or reset the database. Lastly, the ETL.py script can be ran to process the data.
