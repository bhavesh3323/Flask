import folium
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('gps_data.db')
cursor = conn.cursor()

# Fetch all GPS data
cursor.execute('SELECT latitude, longitude FROM gps_data')
gps_data = cursor.fetchall()

# Check if there is any data
if gps_data:
    # Create a map centered around the first data point
    map_center = gps_data[0]
    mymap = folium.Map(location=map_center, zoom_start=12)

    # Add markers for each data point
    for data in gps_data:
        folium.Marker(location=data).add_to(mymap)

    # Save the map as an HTML file
    mymap.save('gps_tracking_map.html')
else:
    print("No GPS data available to generate the map.")

# Close the database connection
conn.close()


#curl -X POST http://127.0.0.1:5000/gps -H "Content-Type: application/json" -d '{"timestamp": "2024-07-05T12:34:56Z", "latitude": 37.7749, "longitude": -122.4194, "speed": 50.0, "distance": 10.0}'
