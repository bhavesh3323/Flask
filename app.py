from flask import Flask, request, jsonify, render_template, redirect, url_for
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

@app.route('/gps', methods=['GET', 'POST'])
def receive_gps_data():
    if request.method == 'POST':
        data = request.form  # For form data
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

        return redirect(url_for('show_gps_data'))

    return render_template('submit_data.html')

@app.route('/show_gps_data')
def show_gps_data():
    cursor.execute('SELECT timestamp, latitude, longitude, speed, distance FROM gps_data')
    gps_data = cursor.fetchall()
    # Convert the data into a list of dictionaries for easier handling in the template
    gps_data_dicts = [dict(timestamp=row[0], latitude=row[1], longitude=row[2], speed=row[3], distance=row[4]) for row in gps_data]
    return render_template('gps_data.html', gps_data=gps_data_dicts)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
