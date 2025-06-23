import geopandas as gpd 
from shapely.geometry import MultiPolygon

def load_and_fix_shapefile(filepath):
    """Loads a Superfile, detects invalid geometries and fixes them.

    Args:
        filepath (_type_): Filepath to the shapefile.
    """
    
    try:  
        gdf = gpd.read_file(filepath)
        # Convert invalid Polygons to MultiPolygons
        gdf["geometry"] = gdf["geometry"].apply(
            lambda geom: MultiPolygon([geom]) if geom.geom_type == "Polygon" else geom
        )
        
        gdf = gdf[gdf.is_valid]
        
        return gdf
    except Exception as e:
        print(f"Error loading shapefile: {e}")
        return None