from src.database.connection import get_db_connection
from src.etl.extract.bsas_data.fetch_bus_stop import fetch_bus_stops
from src.etl.load.postgis.save_bus_stop import save_bus_stop

def save_bus_stop_pipeline():
    """Saves the bus stop GeoDataFrame to PostGIS."""
    try:
       # Fetch bus stops from the API
       bus_stops = fetch_bus_stops()
       # Get a connection to the database
       db_connection = get_db_connection()
       # Save the bus stops to PostGIS
       save_bus_stop(bus_stops, db_connection)
    except Exception as e:
        print(f"Error saving bus stops: {e}")
        pass

if __name__ == "__main__":
    save_bus_stop_pipeline()