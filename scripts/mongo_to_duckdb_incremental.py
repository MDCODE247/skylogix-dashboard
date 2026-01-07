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
# Connect to DuckDB
# --------------------------
conn = duckdb.connect(DUCKDB_FILE)

# --------------------------
# Create table if not exists
# --------------------------
conn.execute(f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    _id VARCHAR PRIMARY KEY,
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
# Get last synced timestamp from DuckDB
# --------------------------
result = conn.execute(f"SELECT MAX(updatedAt) FROM {TABLE_NAME}").fetchone()
last_sync = result[0] if result[0] is not None else pd.Timestamp("1970-01-01")

print(f"Last synced updatedAt: {last_sync}")

# --------------------------
# Fetch incremental data from MongoDB
# --------------------------
query = {"updatedAt": {"$gt": last_sync}}
cursor = collection.find(query)

df = pd.DataFrame(list(cursor))
if df.empty:
    print("No new records to sync.")
    conn.close()
    exit()

# Convert _id to string for DuckDB
df["_id"] = df["_id"].astype(str)

# --------------------------
# Insert / Upsert into DuckDB
# --------------------------
for index, row in df.iterrows():
    # Delete old record with same _id if exists
    conn.execute(f"DELETE FROM {TABLE_NAME} WHERE _id='{row['_id']}'")
    # Insert new record
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

print(f"Synced {len(df)} new records from MongoDB → DuckDB.")

conn.close()
