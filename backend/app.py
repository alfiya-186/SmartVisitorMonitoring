
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "visitor_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "visitor123"),
        port=5432
    )

@app.route("/")
def home():
    return jsonify({
        "message": "Smart Visitor Monitoring Backend is running"
    })

@app.route("/api/readings", methods=["POST"])
def receive_readings():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data received"}), 400

    required = [
        "entry_count",
        "exit_count",
        "people_inside",
        "sensor_a",
        "sensor_b"
    ]

    if not all(key in data for key in required):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO visitor_readings
            (entry_count, exit_count, people_inside, sensor_a, sensor_b)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data["entry_count"],
            data["exit_count"],
            data["people_inside"],
            data["sensor_a"],
            data["sensor_b"]
        ))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Reading saved successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/latest", methods=["GET"])
def latest_reading():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT entry_count, exit_count, people_inside,
                   sensor_a, sensor_b, created_at
            FROM visitor_readings
            ORDER BY id DESC
            LIMIT 1
        """)

        row = cur.fetchone()
        cur.close()
        conn.close()

        if row is None:
            return jsonify({"message": "No readings available"}), 404

        return jsonify({
            "entry_count": row[0],
            "exit_count": row[1],
            "people_inside": row[2],
            "sensor_a": row[3],
            "sensor_b": row[4],
            "created_at": row[5].isoformat()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
