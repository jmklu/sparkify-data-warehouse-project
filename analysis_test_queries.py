import configparser
import psycopg2

def run_query(cur, query, description):
    """
    Executes a SQL query and prints the result with a description.
    """
    print(f"\nRunning Query: {description}")
    cur.execute(query)
    rows = cur.fetchall()
    
    for row in rows:
        print(row)

def main():
    # Load DWH configuration from dwh.cfg file
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    # Connect to Redshift
    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(
            *config['CLUSTER'].values()
        )
    )
    cur = conn.cursor()

    print("Running Sample Analysis Queries...\n")

    # Query 1: Top 5 most played songs
    most_played_songs_query = """
    SELECT s.title, COUNT(*) AS play_count
    FROM songplays sp
    JOIN songs s ON sp.song_id = s.song_id
    GROUP BY s.title
    ORDER BY play_count DESC
    LIMIT 5;
    """
    run_query(cur, most_played_songs_query, "Top 5 Most Played Songs")

    # Query 2: Top 5 most active users
    most_active_users_query = """
    SELECT u.first_name, u.last_name, COUNT(*) AS activity_count
    FROM songplays sp
    JOIN users u ON sp.user_id = u.user_id
    GROUP BY u.first_name, u.last_name
    ORDER BY activity_count DESC
    LIMIT 5;
    """
    run_query(cur, most_active_users_query, "Top 5 Most Active Users")

    # Query 3: Top 5 busiest times for playing songs (by hour)
    busiest_times_query = """
    SELECT t.hour, COUNT(*) AS play_count
    FROM songplays sp
    JOIN time t ON sp.start_time = t.start_time
    GROUP BY t.hour
    ORDER BY play_count DESC
    LIMIT 5;
    """
    run_query(cur, busiest_times_query, "Top 5 Busiest Times for Playing Songs (by Hour)")

    # Close connection
    cur.close()
    conn.close()

    print("\nAnalysis Queries Completed.")

if __name__ == "__main__":
    main()
