import configparser
import psycopg2

# Load configuration from the dwh.cfg file
config = configparser.ConfigParser()
config.read('dwh.cfg')

# Retrieve the connection parameters from the config file
HOST = config.get('CLUSTER', 'HOST')
DB_NAME = config.get('CLUSTER', 'DB_NAME')
DB_USER = config.get('CLUSTER', 'DB_USER')
DB_PASSWORD = config.get('CLUSTER', 'DB_PASSWORD')
DB_PORT = config.get('CLUSTER', 'DB_PORT')

# Test the connection
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=HOST,
        port=DB_PORT
    )
    print("Connected to Redshift!")
    conn.close()
except Exception as e:
    print(f"Error while connecting to Redshift: {e}")
