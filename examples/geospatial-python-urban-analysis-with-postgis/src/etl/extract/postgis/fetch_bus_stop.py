import geopandas as gpd

from src.database.connection import get_db_connection
from src.database.queries import get_bus_stops_query

def fetch_bus_stops(line_number: str = None):
    """Fetches bus stops from PostGIS."""
    try:
        engine = get_db_connection()
        query = get_bus_stops_query()
        
        # If a line number is provided, filter the query
        params = {"line_number": line_number}
           
        return gpd.read_postgis(query, con=engine, geom_col="geometry", params=params)
    except Exception as e:
        raise Exception(f"Failed to fetch bus stops: {str(e)}") from e
