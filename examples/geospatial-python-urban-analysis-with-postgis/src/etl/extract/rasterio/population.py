import rasterio
import numpy as np
from config import POPULATION_DENSITY_RASTER

def load_population_density() -> tuple[np.ndarray, rasterio.Affine, rasterio.CRS]:
    """Loads population density raster data from the configured file.
    
    Returns:
        tuple: A tuple containing:
            - population_data (np.ndarray): The raster data as a NumPy array
            - transform (rasterio.Affine): The transform metadata
            - crs (rasterio.CRS): The coordinate reference system
    
    Raises:
        FileNotFoundError: If the raster file does not exist
        rasterio.errors.RasterioIOError: If there is an error reading the raster file
    """
    try:
        with rasterio.open(POPULATION_DENSITY_RASTER) as src:
            population_data = src.read(1)
            transform = src.transform
            crs = src.crs
            return population_data, transform, crs
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Population density raster not found at {POPULATION_DENSITY_RASTER}") from e
    except rasterio.errors.RasterioIOError as e:
        raise rasterio.errors.RasterioIOError(f"Error reading raster file: {str(e)}") from e