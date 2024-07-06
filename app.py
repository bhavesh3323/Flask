from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize SQLite database
conn = sqlite3.connect('gps_data.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS gps_data (
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        latitude REAL,
        longitude REAL,
        speed REAL,
        distance REAL
    )
''')
conn.commit()

@app.route('/gps', methods=['POST'])
def receive_gps_data():
    data = request.json
    timestamp = data['timestamp']
    latitude = data['latitude']
    longitude = data['longitude']
    speed = data['speed']
    distance = data['distance']

    cursor.execute('''
        INSERT INTO gps_data (timestamp, latitude, longitude, speed, distance)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, latitude, longitude, speed, distance))
    conn.commit()

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)