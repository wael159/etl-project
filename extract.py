import pandas as pd
import json
import configparser
from sqlalchemy import create_engine

# Read DB config from app.properties
config = configparser.ConfigParser()
config.read('app.properties')

src = config['DEFAULT'] if 'DEFAULT' in config else config['app'] if 'app' in config else config

def get_prop(key):
    return src.get(key, src.get('DEFAULT', {}).get(key, ''))

db_type = get_prop('source_db_type')
user = get_prop('source_db_user')
password = get_prop('source_db_password')
host = get_prop('source_db_host')
port = get_prop('source_db_port')
database = get_prop('source_db_database')

# Build SQLAlchemy connection string
conn_str = f"{db_type}://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(conn_str)

# Read SQL query from extract_config.json
with open('extract_config.json') as f:
    extract_conf = json.load(f)
query = extract_conf['query']

# Execute query and fetch data
df = pd.read_sql_query(query, engine)

# Save to CSV for next step
df.to_csv('extracted_data.csv', index=False)
print("Extraction complete. Data saved to extracted_data.csv") 