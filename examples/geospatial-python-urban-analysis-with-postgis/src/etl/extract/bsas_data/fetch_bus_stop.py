
import requests
import io

import geopandas as gpd
from config import BUS_STOPS_URL

def fetch_bus_stops():
    """Fetches bus stops from the Buenos Aires open data API."""
    try:
        response = requests.get(BUS_STOPS_URL, timeout=10)  # Set a timeout to prevent hanging
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        
        # Convert JSON response into a GeoDataFrame
        gdf = gpd.read_file(io.BytesIO(response.content))
        print(f"Successfully fetched {len(gdf)} bus stops from API.")
        return gdf

    except requests.exceptions.RequestException as e:
        print(f"Error fetching bus stops: {e}")
        return None 