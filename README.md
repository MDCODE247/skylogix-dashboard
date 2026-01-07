# SkyLogix Weather Dashboard

A real-time weather monitoring dashboard for SkyLogix operations. The project captures weather data from MongoDB, stores it in DuckDB, and visualizes it with Streamlit, all within a Dockerized environment.

---

## Features

- Real-time weather monitoring for multiple cities
- KPIs: Cities Monitored, Avg Temperature (°C), Avg Humidity (%)
- Live table of latest weather readings
- Temperature bar chart by city
- Automatic refresh as new data is ingested
- End-to-end ETL: MongoDB → DuckDB → Streamlit
- Fully Dockerized for easy deployment

---

## Project Structure

```
skylogix-weather-pipeline/
├── dashboard/
│   └── app.py               # Streamlit dashboard
├── duckdb/
│   └── weather.duckdb       # DuckDB database storing weather readings
├── scripts/
│   ├── weather_ingestor.py  # Simulates live weather ingestion
│   └── mongo_to_duckdb.py  # ETL: loads data from MongoDB to DuckDB
├── docker/
│   ├── Dockerfile           # Dockerfile for dashboard service
│   └── docker-compose.yml   # Orchestrates MongoDB, ETL scripts, and Streamlit
└── README.md
```

---

## Installation (Dockerized)

1. Clone the repository:
```bash
git clone https://github.com/MDCODE247/skylogix-dashboard.git
cd skylogix-weather-pipeline
```

2. Install Docker and Docker Compose if not already installed.

---

## Running the Project with Docker

1. Navigate to the `docker` folder:
```bash
cd docker
```

2. Start all services:
```bash
docker compose up -d
```

3. Services included:
- MongoDB – stores live weather data
- ETL scripts – load data from MongoDB to DuckDB
- Streamlit dashboard – visualizes weather data at http://localhost:8501

4. Stop services:
```bash
docker compose down
```

---

## Running the Dashboard Locally (Optional)

```bash
cd dashboard
pip install streamlit duckdb pandas pymongo
streamlit run app.py
```
Open in your browser: http://localhost:8501

---

## MongoDB Setup

- Ensure MongoDB service is running (via Docker or local installation)
- Update `scripts/mongo_to_duckdb.py` with your MongoDB connection string:
```python
from pymongo import MongoClient

client = MongoClient("mongodb://mongo:27017")  # Use Docker service name if Dockerized
db = client["weather_db"]
collection = db["weather_readings"]
```
- This script extracts weather data from MongoDB and loads it into DuckDB.

---

## Deployment to Streamlit Community Cloud

1. Push your project to GitHub:
```bash
git init
git add .
git commit -m "Initial commit - SkyLogix dashboard with MongoDB & Docker"
git branch -M main
git remote add origin https://github.com/MDCODE247/skylogix-dashboard.git
git push -u origin main
```

2. Create `requirements.txt`:
```
streamlit
duckdb
pandas
pymongo
```

3. Deploy on Streamlit Cloud:
   - New App → Connect GitHub → Select repo → App path: `dashboard/app.py` → Deploy

---

## Future Improvements

- Add more weather metrics: wind speed, pressure, rainfall
- Include historical trends and forecast charts
- City filtering, search, and sorting
- Secure authentication for dashboard
- Fully Dockerize the ETL schedule (Airflow) for production


## License

MIT License © 2026 Mohammed Abubakar

---

## Contact

Mohammed Abubakar  
Email: ammedabubakard500@gmail.com
GitHub: [MDCODE247](https://github.com/MDCODE247)

