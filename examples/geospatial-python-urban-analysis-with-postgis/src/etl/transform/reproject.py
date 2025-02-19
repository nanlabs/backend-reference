import geopandas as gpd
from config import EPSG_TARGET

def reproject_shapefile(gdf: gpd.GeoDataFrame):
    """Transform the data to the target CRS."""
    try:
        return gdf.to_crs(epsg=EPSG_TARGET)
    except Exception as e:
        print(f"Error reprojecting shapefile: {e}")
        return None