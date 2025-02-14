import os

from pathlib import Path
from src.etl.transform.fix_shapefile import load_and_fix_shapefile
from src.etl.transform.rasterize import rasterize_shapefile
from src.etl.transform.reproject import reproject_shapefile


def run_shapefile_to_raster_pipeline():
    """
        Full pipeline to convert a shapefile to a raster.
    """
    
    script_dir = Path(__file__).resolve().parent.parent.parent
    
    shapefile_path = os.path.join(script_dir, "data/census/caba/cabaxrdatos.shp")
    output_raster = os.path.join(script_dir, "data/census/caba/census.tif")

    gdf = load_and_fix_shapefile(shapefile_path)
    
        
    if gdf is not None:
        gdf = reproject_shapefile(gdf)
        
        if gdf is not None:
            rasterize_shapefile(gdf, output_raster)
            
if __name__ == "__main__":
    run_shapefile_to_raster_pipeline()
