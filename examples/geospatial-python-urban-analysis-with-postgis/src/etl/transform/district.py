import pandas as pd
import geopandas as gpd
from config import EPSG_TARGET

def spatial_join(bus_stops: gpd.GeoDataFrame, comunas: gpd.GeoDataFrame):
    """Join bus stops with districts based on spatial location."""
    if bus_stops.crs != comunas.crs:
        raise ValueError(f"CRS mismatch: bus_stops CRS is {bus_stops.crs}, comunas CRS is {comunas.crs}")
    return gpd.sjoin(bus_stops, comunas, how="inner", predicate="within")

def count_stops_per_district(bus_stops_in_district: gpd.GeoDataFrame):
    """Count the number of stops per district."""
    return bus_stops_in_district.groupby("comuna").size().reset_index(name="cantidad_paradas")

def get_extreme_district(stops_by_comuna: pd.DataFrame) -> tuple:
    """
    Get the district with the most and least bus stops.
    Args:
        stops_by_comuna (pd.DataFrame): DataFrame with bus stop counts by district
    Returns:
        tuple: (district with most stops, district with least stops)
    Raises:
        ValueError: If DataFrame is empty
    """
    if stops_by_comuna.empty:
        raise ValueError("No districts data available")
    
    comuna_max = stops_by_comuna.loc[stops_by_comuna["cantidad_paradas"].idxmax()]
    comuna_min = stops_by_comuna.loc[stops_by_comuna["cantidad_paradas"].idxmin()]
    
    return comuna_max, comuna_min