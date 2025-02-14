import geopandas as gpd

import rasterio
from src.database.connection import get_db_connection
from src.database.queries import get_bus_stops_query
from config import DISTRICTS_URL, POPULATION_DENSITY_RASTER

def fetch_bus_stops(line_number: str = None):
    """Fetches bus stops from PostGIS."""
    engine = get_db_connection()
    query = get_bus_stops_query()
    
    # If a line number is provided, filter the query
    params = {"line_number": line_number}
       
    return gpd.read_postgis(query, con=engine, geom_col="geometry",params=params)

def fetch_districts():
    """Fetches district data from Buenos Aires' open data API."""
    return gpd.read_file(DISTRICTS_URL)

def load_population_density():
    """Loads population density raster"""
    with rasterio.open(POPULATION_DENSITY_RASTER) as src:
        return src.read(1). src.transform , src.crs