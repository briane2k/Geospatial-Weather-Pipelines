import geopandas as gpd
import folium

# 1. Fetch real-time USGS GeoJSON data
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
gdf = gpd.read_file(url)

# 2. Inititialize a global interactive map centered at 0, 0)
# 'tiles' sets a dark, clean background theme
m = folium.Map(location=[0, 0], zoom_start=2, tiles="CartoDB Dark Matter")

print("Building interactive map layers...")

# 3. Interate through our spatial data table and inject markers onto the map
for idx, row in gdf.iterrows():
    # Extract coordinates from the Shapely Point object
    # Note: Shapely Point objects store coordinates as (longitude, latitude)
    # Folium expects [latitude, longitude]
    lon, lat = row['geometry'].x, row['geometry'].y
    magnitude = row['mag']
    location_name = row['place']

    # Set marker color base on earthquake intensity (magnitude)
    if magnitude >= 6.0:
        color = '#ff3333' # Bright red for major quakes
        radius = 12
    elif magnitude >= 5.0:
        color = 'orange' # Orange for moderate quakes
        radius = 8
    else:
        color = '#ffff33' # Yellow for minor quakes
        radius = 5

    # Create a vector circle marker for each earthquake
    folium.CircleMarker(
        location=[lat, lon],
        radius=radius,
        popup=f"<strong>{location_name}</strong><br>Magnitude: {magnitude}",
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
    ).add_to(m)


# 4. Export the compiled visulation as a standalone HTML file
output_file = "earthquake_map.html"
m.save(output_file)
print(f"Success! Interactive map saved as '{output_file}'")
