import geopandas as gpd
from config import EPSG_TARGET

def reproject_shapefile(gdf: gpd.GeoDataFrame):
    """Transform the data to the target CRS."""
    return gdf.to_crs(epsg=EPSG_TARGET)