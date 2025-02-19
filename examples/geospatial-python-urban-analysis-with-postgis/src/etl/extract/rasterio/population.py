import rasterio
from config import POPULATION_DENSITY_RASTER

def load_population_density():
    """Loads population density raster"""
    with rasterio.open(POPULATION_DENSITY_RASTER) as src:
        print(f"✅ Successfully loaded {POPULATION_DENSITY_RASTER}")  # Debugging
        population_data = src.read(1)  # ✅ Extract raster data (NumPy array)
        transform = src.transform  # ✅ Extract transform metadata
        crs = src.crs  # ✅ Extract coordinate reference system
        
        return population_data, transform, crs  # ✅ Return values separately