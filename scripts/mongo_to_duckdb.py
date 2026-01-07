import duckdb
import pandas as pd
from pymongo import MongoClient
import os

# --------------------------
# CONFIG
# --------------------------
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "weather_db"
COLLECTION_NAME = "weather_readings"

DUCKDB_FOLDER = "./duckdb"
DUCKDB_FILE = os.path.join(DUCKDB_FOLDER, "weather.duckdb")
TABLE_NAME = "weather_readings"

# Create folder if not exists
os.makedirs(DUCKDB_FOLDER, exist_ok=True)

# --------------------------
# Connect to MongoDB
# --------------------------
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# --------------------------
# Load data from MongoDB
# --------------------------
df = pd.DataFrame(list(collection.find()))
if df.empty:
    print("No data in MongoDB to sync.")
    exit()

# Convert _id to string if needed
if "_id" in df.columns:
    df["_id"] = df["_id"].astype(str)

# --------------------------
# Connect to DuckDB
# --------------------------
conn = duckdb.connect(DUCKDB_FILE)

# --------------------------
# Create table if not exists
# --------------------------
conn.execute(f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    _id VARCHAR,
    city VARCHAR,
    country VARCHAR,
    temperature DOUBLE,
    humidity DOUBLE,
    weather VARCHAR,
    wind_speed DOUBLE,
    timestamp TIMESTAMP,
    updatedAt TIMESTAMP
)
""")

# --------------------------
# Insert data (overwrite duplicates)
# --------------------------
# DuckDB doesn't support UPSERT natively, so we drop existing IDs and append
for index, row in df.iterrows():
    conn.execute(f"""
    DELETE FROM {TABLE_NAME} WHERE _id='{row['_id']}';
    """)
    conn.execute(f"""
    INSERT INTO {TABLE_NAME} VALUES (
        '{row['_id']}',
        '{row['city']}',
        '{row['country']}',
        {row['temperature']},
        {row['humidity']},
        '{row['weather']}',
        {row['wind_speed']},
        TIMESTAMP '{row['timestamp']}',
        TIMESTAMP '{row['updatedAt']}'
    )
    """)

print(f"Synced {len(df)} records from MongoDB → DuckDB.")

conn.close()
