import geopandas as gpd
from src.database.connection import get_db_connection
from src.database.queries import get_bus_stops_query

def fetch_bus_stops(line_number: str | None = None) -> gpd.GeoDataFrame:
    """Fetches bus stops from PostGIS."""
    """Fetches bus stops data from PostGIS database.
    
    Args:
        line_number (str | None, optional): Bus line number to filter results.
            If None, returns all bus stops. Defaults to None.
    
    Returns:
        gpd.GeoDataFrame: A GeoDataFrame containing bus stop data with geometry.
    
    Raises:
        ValueError: If line_number is provided but invalid.
        Exception: If database connection or query fails.
    """
    if line_number is not None and not line_number.strip():
        raise ValueError("line_number cannot be empty")
    
    engine = None
    try:
        engine = get_db_connection()
        query = get_bus_stops_query()
        
        # If a line number is provided, filter the query
        params = {"line_number": line_number}
           
        return gpd.read_postgis(query, con=engine, geom_col="geometry", params=params)
    except Exception as e:
        raise Exception(f"Failed to fetch bus stops: {str(e)}") from e
    finally:
        if engine is not None:
            engine.dispose()
