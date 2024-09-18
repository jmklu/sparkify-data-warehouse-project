# Sparkify Data Warehouse and ETL Pipeline

## Project Overview

This project builds an ETL pipeline for a music streaming startup called Sparkify. The pipeline extracts data from S3, stages it in Redshift, and transforms it into a star schema optimized for analysis. The data consists of JSON logs tracking user activity on the app and metadata on the songs in the app.

This data warehouse and pipeline enable Sparkify's analytics team to answer business questions, such as identifying the most played songs, busiest times, and most active users.

## Database Schema

The database follows a **star schema** with the fact table `songplays` and several dimension tables, including `users`, `songs`, `artists`, and `time`.

### Fact Table

- **songplays**: Records in event data associated with song plays (records with `page` = 'NextSong').
  - **Columns**:
    - `songplay_id`: Serial primary key.
    - `start_time`: Timestamp of the song play.
    - `user_id`: ID of the user who listened to the song.
    - `level`: User's subscription level (free/paid).
    - `song_id`: ID of the song.
    - `artist_id`: ID of the artist.
    - `session_id`: ID of the user's session.
    - `location`: User's location.
    - `user_agent`: User's device and browser information.

### Dimension Tables

- **users**: Users in the app.
  - **Columns**: `user_id`, `first_name`, `last_name`, `gender`, `level`
  
- **songs**: Songs in the music database.
  - **Columns**: `song_id`, `title`, `artist_id`, `year`, `duration`
  
- **artists**: Artists in the music database.
  - **Columns**: `artist_id`, `name`, `location`, `latitude`, `longitude`
  
- **time**: Timestamps of records in `songplays` broken down into specific units.
  - **Columns**: `start_time`, `hour`, `day`, `week`, `month`, `year`, `weekday`

## ETL Pipeline

The ETL process extracts data from two sources in S3:
1. **Song data**: Metadata about songs and artists.
2. **Log data**: Records of user interactions with the app.

The ETL pipeline is implemented in Python and consists of several key steps:
- **Staging**: Loads raw JSON data from S3 into staging tables (`staging_events`, `staging_songs`) in Redshift.
- **Fact and Dimension Table Insertions**: Extracts and transforms data from the staging tables into the fact (`songplays`) and dimension tables (`users`, `songs`, `artists`, `time`).

### Files and Functions:

- **`create_tables.py`**: 
  - Drops and creates staging, fact, and dimension tables in Redshift.
  - Functions:
    - `drop_tables`: Drops existing tables.
    - `create_tables`: Creates new tables.

- **`etl.py`**: 
  - Executes the ETL pipeline.
  - Functions:
    - `load_staging_tables`: Loads data from S3 to Redshift staging tables using `COPY` commands.
    - `insert_tables`: Inserts data from staging tables into fact and dimension tables.

- **`sql_queries.py`**: 
  - Contains all the SQL queries used in the project.
  - Query types:
    - **CREATE TABLE** queries: Define table structures.
    - **COPY** queries: Load data from S3 into staging tables.
    - **INSERT** queries: Populate fact and dimension tables from staging data.

- **`test_db_connection.py`**: 
  - Tests the connection to the Redshift cluster.

- **`analysis_test_queries.py`**:
  - Runs sample analysis queries (e.g., most played songs, most active users).

## Sample Queries for Analysis

Here are some example queries that can be run on the data warehouse for analysis purposes:

### Top 5 Most Played Songs
```sql
SELECT s.title, COUNT(*) AS play_count
FROM songplays sp
JOIN songs s ON sp.song_id = s.song_id
GROUP BY s.title
ORDER BY play_count DESC
LIMIT 5;

### Top 5 Most Active Users
```sql
SELECT u.first_name, u.last_name, COUNT(*) AS activity_count
FROM songplays sp
JOIN users u ON sp.user_id = u.user_id
GROUP BY u.first_name, u.last_name
ORDER BY activity_count DESC
LIMIT 5;

### Top 5 Busiest Times for Playing Songs (by Hour)
```sql
SELECT t.hour, COUNT(*) AS play_count
FROM songplays sp
JOIN time t ON sp.start_time = t.start_time
GROUP BY t.hour
ORDER BY play_count DESC
LIMIT 5;



## How to Run the Project

### Prerequisites
- **Amazon Redshift**: A Redshift cluster must be created with appropriate IAM roles for reading from S3.
- **AWS S3**: Data is hosted on S3 (`s3://udacity-dend/`).
- **Python Libraries**: `psycopg2`, `configparser`.

### Steps:

1. **Create the Redshift Cluster**:

   - Launch a Redshift cluster using the AWS Console and configure your IAM roles.
   - Ensure the Redshift cluster can access the S3 bucket.

2. **Run `create_tables.py`:**

   This will drop and create all necessary tables in Redshift.

   **Command:**
   ```bash
   python create_tables.py
   
3. **Run `etl.py`:**

   This will load data into the staging tables from S3 and insert data into the fact and dimension tables.

   **Command:**
   ```bash
   python etl.py


## Run Sample Queries:

To verify that the data has been loaded correctly, you can run `analysis_test_queries.py` or use a SQL client (e.g., Redshift Query Editor) to run the sample queries provided above.



## Project Configuration

`dwh.cfg`: This file contains the Redshift cluster details and S3 bucket paths.


[CLUSTER]
- HOST=your-cluster-endpoint
- DB_NAME=dev
- DB_USER=awsuser
- DB_PASSWORD=yourpassword
- DB_PORT=5439

[IAM_ROLE]
- ARN=arn:aws:iam::your-iam-role-arn

[S3]
- LOG_DATA='s3://udacity-dend/log_data'
- LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
- SONG_DATA='s3://udacity-dend/song_data'
