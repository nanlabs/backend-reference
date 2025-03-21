from sqlalchemy import Engine

import geopandas as gpd

def save_bus_stop(gdf: gpd.GeoDataFrame, conn: Engine ) -> bool:
    """Saves the bus stop GeoDataFrame to PostGIS."""
    try:
        gdf.to_postgis("bus_stops",conn, if_exists="replace", index=False)
        print(f"Successfully saved bus stops to PostGIS.")
        return True
    except Exception as e:
        print(f"Error saving bus stops: {e}")
        return