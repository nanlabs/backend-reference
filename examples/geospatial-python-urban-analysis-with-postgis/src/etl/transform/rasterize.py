import rasterio
import numpy as np
import shapefile

from rasterio.features import rasterize
from shapely.geometry import mapping

def rasterize_shapefile(gdf, output_path, resolution = 100):
    """
    Converts a GeoDataFrame into a raster (.tif) using the specified value column.
    
    Args:
        gdf (gpd.GeoDataFrame): The input GeoDataFrame to rasterize.
        output_path (str): Path where the output raster will be saved.
        value_column (str, optional): Column to use for raster values. Defaults to "TOT_POB".
        resolution (int, optional): Spatial resolution in map units. Defaults to 100.
    
    Returns:
        None
    """
    
    try:
        xmin, ymin, xmax, ymax = gdf.total_bounds
        width = int((xmax - xmin) / resolution)
        height = int((ymax - ymin) / resolution)
        
        transform = rasterio.transform.from_bounds(xmin, ymin, xmax, ymax, width, height)

        raster_data = rasterize(
            [(mapping(geom), 1) for geom, value in zip(gdf.geometry, gdf["TOT_POB"])],
            out_shape=(height, width),
            transform=transform,
            fill=0,
            dtype="float32",
        )
        
        with rasterio.open(
            output_path, "w", driver="GTiff", height=height, width=width, count=1, dtype="float32", crs=gdf.crs, transform=transform
        ) as dst:
            dst.write(raster_data, 1)
            
        print(f"Raster saved to {output_path}")
        
    except Exception as e:
        print(f"Error rasterizing shapefile: {e}")
