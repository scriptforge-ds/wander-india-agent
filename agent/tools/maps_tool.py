import folium
from agent.tools.weather_tool import DESTINATION_COORDS


def generate_trip_map(
    destination_key: str,
    destination_name: str,
    origin_coords: dict = None,
    waypoints: list[dict] = None
) -> folium.Map:
    """
    Generates a Folium map for a trip.
    origin_coords: {"lat": float, "lon": float, "name": str}
    waypoints: [{"lat": float, "lon": float, "name": str, "note": str}]
    """
    dest_coords = DESTINATION_COORDS.get(destination_key)
    if not dest_coords:
        return None

    # Center map on destination
    m = folium.Map(
        location=[dest_coords["lat"], dest_coords["lon"]],
        zoom_start=8,
        tiles="CartoDB positron"
    )

    # Add destination marker
    folium.Marker(
        location=[dest_coords["lat"], dest_coords["lon"]],
        popup=folium.Popup(f"<b>{destination_name}</b>", max_width=200),
        tooltip=destination_name,
        icon=folium.Icon(color="green", icon="flag")
    ).add_to(m)

    # Add origin marker
    if origin_coords:
        folium.Marker(
            location=[origin_coords["lat"], origin_coords["lon"]],
            popup=folium.Popup(f"<b>Start: {origin_coords['name']}</b>", max_width=200),
            tooltip=f"Start: {origin_coords['name']}",
            icon=folium.Icon(color="blue", icon="home")
        ).add_to(m)

        # Draw a line from origin to destination
        folium.PolyLine(
            locations=[
                [origin_coords["lat"], origin_coords["lon"]],
                [dest_coords["lat"], dest_coords["lon"]]
            ],
            color="#FF6B35",
            weight=2,
            dash_array="5"
        ).add_to(m)

    # Add waypoints
    if waypoints:
        for i, wp in enumerate(waypoints):
            folium.Marker(
                location=[wp["lat"], wp["lon"]],
                popup=folium.Popup(
                    f"<b>Day {i+1}: {wp['name']}</b><br>{wp.get('note', '')}",
                    max_width=200
                ),
                tooltip=wp["name"],
                icon=folium.Icon(color="orange", icon=str(i+1), prefix="fa")
            ).add_to(m)

    return m


# Common city coordinates for origin mapping
CITY_COORDS = {
    "bangalore":  {"lat": 12.97, "lon": 77.59, "name": "Bangalore"},
    "mumbai":     {"lat": 19.07, "lon": 72.87, "name": "Mumbai"},
    "delhi":      {"lat": 28.61, "lon": 77.20, "name": "Delhi"},
    "chennai":    {"lat": 13.08, "lon": 80.27, "name": "Chennai"},
    "hyderabad":  {"lat": 17.38, "lon": 78.48, "name": "Hyderabad"},
    "kolkata":    {"lat": 22.57, "lon": 88.36, "name": "Kolkata"},
    "pune":       {"lat": 18.52, "lon": 73.85, "name": "Pune"},
    "rishikesh":  {"lat": 30.08, "lon": 78.26, "name": "Rishikesh"},
    "dehradun":   {"lat": 30.31, "lon": 78.03, "name": "Dehradun"},
    "shimla":     {"lat": 31.10, "lon": 77.17, "name": "Shimla"},
    "manali":     {"lat": 32.24, "lon": 77.18, "name": "Manali"},
    "jorhat":     {"lat": 26.75, "lon": 94.20, "name": "Jorhat"},
    "hubli":      {"lat": 15.36, "lon": 75.12, "name": "Hubli"},
    "mangalore":  {"lat": 12.87, "lon": 74.84, "name": "Mangalore"},
}