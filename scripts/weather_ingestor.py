import requests
from pymongo import MongoClient
from datetime import datetime
import os

# =====================
# CONFIGURATION
# =====================
API_KEY = "YOUR_API_KEY_HERE"

CITIES = [
    {"city": "Lagos", "country": "NG"},
    {"city": "Accra", "country": "GH"},
    {"city": "Johannesburg", "country": "ZA"},
    {"city": "Nairobi", "country": "KE"}
]

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "weather_db"
COLLECTION_NAME = "weather_readings"

# =====================
# CONNECT TO MONGODB
# =====================
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Index for incremental sync
collection.create_index("updatedAt")

# =====================
# FETCH WEATHER DATA
# =====================
def fetch_weather(city, country):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city},{country}&appid={"c317bfee549711a5f1a9fddd16bb79fd"}&units=metric"
    )
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# =====================
# INGEST DATA
# =====================
for location in CITIES:
    data = fetch_weather(location["city"], location["country"])

    document = {
        "_id": data["id"],
        "city": data["name"],
        "country": location["country"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
        "timestamp": datetime.utcfromtimestamp(data["dt"]),
        "updatedAt": datetime.utcnow()
    }

    collection.update_one(
        {"_id": document["_id"]},
        {"$set": document},
        upsert=True
    )

    print(f"Upserted weather data for {document['city']}")

print("Weather ingestion completed successfully.")
