import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "drop table if exists staging_events"
staging_songs_table_drop = "drop table if exists staging_songs"
songplay_table_drop = "drop table if exists songplays"
user_table_drop = "drop table if exists users"
song_table_drop = "drop table if exists songs "
artist_table_drop = "drop table if exists artists"
time_table_drop = "drop table if exists time"

# CREATE TABLES

staging_events_table_create= ("""
create table if not exists staging_events
    (
        artist varchar,
        auth varchar,
        firstName varchar,
        gender varchar,
        itemInSession varchar,
        lastName varchar,
        length float, 
        level varchar,
        location varchar,
        method varchar,    
        page varchar,
        registration float,
        sessionId integer,
        song varchar,
        status integer,
        ts TIMESTAMP,
        userAgent varchar,
        userId integer
        
    )
""")

staging_songs_table_create = ("""
    create table if not exists staging_songs
    (
        num_songs integer,
        artist_id varchar,
        artist_latitude float,
        artist_longitude float,
        artist_location varchar,
        artist_name varchar,
        song_id varchar,
        title varchar,
        duration float,
        year integer
        
    )
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays
    (
        songplay_id integer IDENTITY(0,1) primary key,
        start_time timestamp ,
        user_id integer,
        level varchar,
        song_id varchar,
        artist_id varchar,
        session_id integer,
        location varchar,
        user_agent varchar
    )
""")

user_table_create = ("""
    create table if not exists users
    (
        user_id integer primary key, 
        first_name varchar, 
        last_name varchar, 
        gender varchar,
        level varchar
    )
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs
    (
        song_id varchar primary key,
        title varchar not null, 
        artist_id varchar not null, 
        year integer,
        duration float not null 
    )
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists
    (
        artist_id varchar primary key,
        name varchar, 
        location varchar, 
        latitude float, 
        longitude float
    )
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time
    (
        start_time TIMESTAMP PRIMARY KEY,
        hour integer, 
        day integer, 
        week integer, 
        month integer, 
        year integer, 
        weekday varchar
    )
""")

# STAGING TABLES

staging_events_copy = ("""
    copy staging_events from {data_bucket}
    credentials 'aws_iam_role={role_arn}'
    region 'us-west-2' format as JSON {log_json_path}
    timeformat as 'epochmillisecs';
""").format(data_bucket=config['S3']['LOG_DATA'], 
            role_arn=config['IAM_ROLE']['ARN'], 
            log_json_path=config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""
    copy staging_songs from {data_bucket}
    credentials 'aws_iam_role={role_arn}'
    region 'us-west-2' format as JSON 'auto';
""").format(data_bucket=config['S3']['SONG_DATA'], 
            role_arn=config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT  DISTINCT(se.ts) as start_time, 
    se.userId as user_id, 
    se.level as level, 
    ss.song_id as song_id, 
    ss.artist_id as artist_id, 
    se.sessionId as session_id, 
    se.location as location, 
    se.userAgent as user_agent
    FROM staging_events se
    JOIN staging_songs  ss   ON (se.song = ss.title AND se.artist = ss.artist_name)
    where se.page  =  'NextSong'
""")

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT  DISTINCT(userId) as user_id,
    firstName as first_name,
    lastName as last_name,
    gender,
    level
    FROM staging_events where page = 'NextSong';
""")

song_table_insert = ("""
    INSERT INTO songs (song_id, title, artist_id, year, duration)
    SELECT  DISTINCT(song_id) AS song_id,
    title,
    artist_id,
    year,
    duration
    FROM staging_songs;
""")

artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
    SELECT  DISTINCT(artist_id) AS artist_id,
    artist_name         AS name,
    artist_location     AS location,
    artist_latitude     AS latitude,
    artist_longitude    AS longitude
    FROM staging_songs;
""")

time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT  DISTINCT(start_time) as start_time,
    EXTRACT(hour FROM start_time) as hour,
    EXTRACT(day FROM start_time)  as day,
    EXTRACT(week FROM start_time) as week,
    EXTRACT(month FROM start_time) as month,
    EXTRACT(year FROM start_time) as year,
    EXTRACT(dayofweek FROM start_time) as weekday
    FROM songplays;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
