from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from datetime import datetime
import folium
import openrouteservice

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

# Replace 'your-api-key' with your actual OpenRouteService API key
ors_api_key = '5b3ce3597851110001cf624891ebe95abe0b4b919148871a0034d027'
ors_client = openrouteservice.Client(key=ors_api_key)

@app.route('/gps', methods=['GET', 'POST'])
def receive_gps_data():
    if request.method == 'POST':
        data = request.form
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        speed = float(data.get('speed', 0.0))
        distance = float(data.get('distance', 0.0))

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
    gps_data_dicts = [dict(timestamp=row[0], latitude=row[1], longitude=row[2], speed=row[3], distance=row[4]) for row in gps_data]
    return render_template('gps_data.html', gps_data=gps_data_dicts)

@app.route('/map')
def show_map():
    cursor.execute('SELECT latitude, longitude FROM gps_data')
    gps_data = cursor.fetchall()

    if gps_data:
        map_center = gps_data[0]
        mymap = folium.Map(location=map_center, zoom_start=12)

        if len(gps_data) == 1:
            # Add marker for the single data point
            folium.Marker(location=gps_data[0]).add_to(mymap)
        else:
            # Add markers for each data point
            for data in gps_data:
                folium.Marker(location=data).add_to(mymap)

            # Generate the route using OpenRouteService
            coords = [(data[1], data[0]) for data in gps_data]  # (longitude, latitude) pairs
            route = ors_client.directions(coords, profile='driving-car', format='geojson')
            folium.GeoJson(route).add_to(mymap)

        map_html = mymap._repr_html_()
    else:
        map_html = "<p>No GPS data available to generate the map.</p>"

    return render_template('gps_map.html', map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
