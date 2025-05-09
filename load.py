import pandas as pd
import configparser
from sqlalchemy import create_engine

# Read DB config from app.properties
config = configparser.ConfigParser()
config.read('app.properties')

tgt = config['DEFAULT'] if 'DEFAULT' in config else config['app'] if 'app' in config else config

def get_prop(key):
    return tgt.get(key, tgt.get('DEFAULT', {}).get(key, ''))

db_type = get_prop('target_db_type')
user = get_prop('target_db_user')
password = get_prop('target_db_password')
host = get_prop('target_db_host')
port = get_prop('target_db_port')
database = get_prop('target_db_database')
target_table = get_prop('target_table')

# Build SQLAlchemy connection string
conn_str = f"{db_type}://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(conn_str)

# Load cleaned data
df = pd.read_csv('cleaned_data.csv')

# Load data to target table (replace if exists)
df.to_sql(target_table, engine, if_exists='replace', index=False)
print(f"Loaded data to table '{target_table}' in target database.") 