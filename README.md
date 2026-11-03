# Smart Visitor Monitoring System

An end-to-end IoT-ready Smart Visitor Monitoring System designed to track footfall, monitor room or building occupancy in real time, and visualize visitor analytics.

---

## 📌 Features

- **Real-Time Occupancy Tracking**: Accurate tracking of total entries, exits, and current people inside.
- **Dual-Sensor Direction Detection**: Designed for dual-sensor setups (Sensor A & Sensor B) to reliably infer movement direction (entry vs. exit).
- **RESTful API Backend**: Flask backend with endpoints to ingest sensor telemetry and serve live data.
- **Persistent Storage**: PostgreSQL database with automated table initialization and historical data logging.
- **Interactive Web Dashboard**: Clean, responsive frontend served via Nginx that polls live stats every 2 seconds with status indicators and alert warnings.
- **Containerized Deployment**: Fully orchestrated with Docker Compose for one-command startup.

---

## 🏗️ Architecture & Tech Stack

```
+--------------------+           POST /api/readings         +---------------------+
|  IoT / Sensors     | -----------------------------------> |   Flask Backend     |
| (ESP32/ESP8266/etc)|                                      |     (Port 5000)     |
+--------------------+                                      +----------+----------+
                                                                       |
                                                     Reads/Writes Data |
                                                                       v
+--------------------+           GET /api/latest            +---------------------+
|   Web Dashboard    | <----------------------------------- |     PostgreSQL      |
|    (Nginx:8080)    |                                      |     (Port 5432)     |
+--------------------+                                      +---------------------+
```

- **Backend**: Python 3.11, Flask, Flask-CORS, Psycopg2
- **Database**: PostgreSQL 16
- **Frontend / Web Server**: HTML5, CSS3, JavaScript (Fetch API), Nginx
- **Orchestration**: Docker & Docker Compose

---

## 📁 Project Structure

```
SmartVisitorMonitoring/
├── backend/
│   ├── app.py             # Flask application & API routes
│   ├── Dockerfile         # Python backend container specification
│   └── requirements.txt   # Python dependencies
├── dashboard/
│   └── index.html         # Responsive live monitoring web dashboard
├── database/
│   └── init.sql           # Database schema & table initialization script
├── docker-compose.yml     # Multi-container service definitions
├── render.yaml            # Render Blueprint Infrastructure-as-Code
├── .gitignore             # Git ignore configuration
└── README.md              # Project documentation
```

---

## ☁️ Deploy to Render (Blueprint)

This repository includes a [`render.yaml`](render.yaml) blueprint specification that automatically provisions:
1. **Managed PostgreSQL Database** (`visitor-db`)
2. **Flask Web Service** (`visitor-backend`) connected automatically via `DATABASE_URL`
3. **Static Dashboard Site** (`visitor-dashboard`)

### 1-Click Setup on Render:
1. Go to your [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** > **Blueprint**.
3. Connect and select the repository: `alfiya-186/SmartVisitorMonitoring`.
4. Render will detect `render.yaml` and display the resources to create.
5. Click **Apply**.
6. Once deployed:
   - Your backend will be live at `https://visitor-backend.onrender.com` (or your assigned subdomain).
   - Your dashboard will be live at `https://visitor-dashboard.onrender.com`.
   - On the dashboard, verify the Backend API URL or update it via the **Change** button if needed.

---

## 🚀 Getting Started Locally

### Prerequisites

Ensure you have the following installed:
- [Docker](https://www.docker.com/get-started/) and [Docker Compose](https://docs.docker.com/compose/)

*(Optional for manual local development without Docker: Python 3.10+, PostgreSQL)*

### 1. Run with Docker Compose (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/alfiya-186/SmartVisitorMonitoring.git
   cd SmartVisitorMonitoring
   ```

2. **Start the services:**
   ```bash
   docker compose up --build -d
   ```

3. **Verify running containers:**
   ```bash
   docker compose ps
   ```

4. **Access the application:**
   - **Dashboard**: [http://localhost:8080](http://localhost:8080)
   - **Backend API**: [http://localhost:5000](http://localhost:5000)
   - **Database**: `localhost:5432` (`visitor_db`)

5. **Stop the services:**
   ```bash
   docker compose down
   ```

---

## 🔌 API Reference

### 1. Health Check
- **Endpoint**: `GET /`
- **Response**:
  ```json
  {
    "message": "Smart Visitor Monitoring Backend is running"
  }
  ```

### 2. Ingest Sensor Readings
- **Endpoint**: `POST /api/readings`
- **Headers**: `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "entry_count": 12,
    "exit_count": 4,
    "people_inside": 8,
    "sensor_a": 1,
    "sensor_b": 0
  }
  ```
- **Response** (`201 Created`):
  ```json
  {
    "message": "Reading saved successfully"
  }
  ```

### 3. Fetch Latest Reading
- **Endpoint**: `GET /api/latest`
- **Response** (`200 OK`):
  ```json
  {
    "entry_count": 12,
    "exit_count": 4,
    "people_inside": 8,
    "sensor_a": 1,
    "sensor_b": 0,
    "created_at": "2026-11-03T11:00:00"
  }
  ```

---

## 📟 Hardware / IoT Integration Example

If using an ESP32 or ESP8266 microcontroller with ultrasonic or IR sensors, you can send HTTP POST requests directly to the backend:

```cpp
#include <WiFi.h>
#include <HTTPClient.h>

const char* serverUrl = "http://<BACKEND_IP>:5000/api/readings";

void sendReading(int entries, int exits, int inside, int sensorA, int sensorB) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    String payload = "{\"entry_count\":" + String(entries) +
                     ",\"exit_count\":" + String(exits) +
                     ",\"people_inside\":" + String(inside) +
                     ",\"sensor_a\":" + String(sensorA) +
                     ",\"sensor_b\":" + String(sensorB) + "}";

    int httpResponseCode = http.POST(payload);
    http.end();
  }
}
```

---

## 📊 Dashboard Preview

The dashboard automatically refreshes every 2 seconds and displays:
- **People Inside**: Real-time room occupancy count.
- **Total Entries**: Aggregate entry count.
- **Total Exits**: Aggregate exit count.
- **Sensor A & Sensor B Status**: Active / Inactive states of infrared or beam sensors.
- **Live System Status**: Backend connectivity indicator and timestamp of latest reading.

---

## 👤 Author

- **alfiya-186** - [GitHub Profile](https://github.com/alfiya-186)

