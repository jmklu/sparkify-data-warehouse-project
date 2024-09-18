import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES to ensure that the tanles are not already existing runing the script again.

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

# Staging Events Table
staging_events_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_events (
    artist        VARCHAR,
    auth          VARCHAR,
    firstName     VARCHAR,
    gender        CHAR(1),
    itemInSession INTEGER,
    lastName      VARCHAR,
    length        FLOAT,
    level         VARCHAR,
    location      VARCHAR,
    method        VARCHAR,
    page          VARCHAR,
    registration  BIGINT,
    sessionId     INTEGER,
    song          VARCHAR,
    status        INTEGER,
    ts            BIGINT,
    userAgent     VARCHAR,
    userId        INTEGER
);
""")


# Staging Songs Table
staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
    num_songs        INTEGER,
    artist_id        VARCHAR,
    artist_latitude  FLOAT,
    artist_longitude FLOAT,
    artist_location  VARCHAR,
    artist_name      VARCHAR,
    song_id          VARCHAR,
    title            VARCHAR,
    duration         FLOAT,
    year             INTEGER
);
""")


# Fact Table: Songplays
songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id   INTEGER IDENTITY(0,1) PRIMARY KEY,
    start_time    TIMESTAMP NOT NULL,
    user_id       INTEGER NOT NULL,
    level         VARCHAR,
    song_id       VARCHAR NOT NULL,
    artist_id     VARCHAR NOT NULL,
    session_id    INTEGER,
    location      VARCHAR,
    user_agent    VARCHAR
);
""")


# Dimension Table: Users
user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id    INTEGER PRIMARY KEY,
    first_name VARCHAR,
    last_name  VARCHAR,
    gender     CHAR(1),
    level      VARCHAR
);
""")


# Dimension Table: Songs
song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id   VARCHAR PRIMARY KEY,
    title     VARCHAR,
    artist_id VARCHAR NOT NULL,
    year      INTEGER,
    duration  FLOAT
);
""")


# Dimension Table: Artists
artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id   VARCHAR PRIMARY KEY,
    name        VARCHAR,
    location    VARCHAR,
    latitude    FLOAT,
    longitude   FLOAT
);
""")


# Dimension Table: Time
time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time TIMESTAMP PRIMARY KEY,
    hour       INTEGER,
    day        INTEGER,
    week       INTEGER,
    month      INTEGER,
    year       INTEGER,
    weekday    INTEGER
);
""")


# STAGING TABLES
#copying staging events...
staging_events_copy = ("""
COPY staging_events
FROM '{}'
IAM_ROLE '{}'
REGION 'us-west-2'
JSON '{}';
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])


#copying staging songs...
staging_songs_copy = ("""
COPY staging_songs
FROM '{}'
IAM_ROLE '{}'
REGION 'us-west-2'
JSON 'auto';
""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])


# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT 
    TIMESTAMP 'epoch' + se.ts/1000 * INTERVAL '1 second' AS start_time,
    se.userId,
    se.level,
    ss.song_id,
    ss.artist_id,
    se.sessionId,
    se.location,
    se.userAgent
FROM staging_events se
JOIN staging_songs ss
ON se.song = ss.title AND se.artist = ss.artist_name
WHERE se.page = 'NextSong';
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
SELECT DISTINCT userId, firstName, lastName, gender, level
FROM staging_events
WHERE userId IS NOT NULL;
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
SELECT DISTINCT song_id, title, artist_id, year, duration
FROM staging_songs
WHERE song_id IS NOT NULL;
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
FROM staging_songs
WHERE artist_id IS NOT NULL; 
""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
SELECT DISTINCT start_time,
    EXTRACT(hour FROM start_time),
    EXTRACT(day FROM start_time),
    EXTRACT(week FROM start_time),
    EXTRACT(month FROM start_time),
    EXTRACT(year FROM start_time),
    EXTRACT(weekday FROM start_time)
FROM songplays;
""")


# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

copy_table_queries = [staging_events_copy, staging_songs_copy]

insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
