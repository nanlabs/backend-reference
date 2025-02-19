import numpy as np
import geopandas as gpd

from sklearn.cluster import DBSCAN 
from shapely.geometry import Point
from rasterio.features import shapes

def extract_high_density_points(
    population_data: np.ndarray,
    transform: np.ndarray
) -> gpd.GeoDataFrame:
    """
        Converts high-density raster pixels to point geometries.
        
        Args:
            population_data: 2D numpy array of population density values
            transform: Affine transformation matrix
        Returns:
            GeoDataFrame containing high-density points
    """
    # Calculate the threshold for high-density pixels 
    threshold = np.mean(population_data)
    high_density_points = []
    
    # Iterate over the raster data and convert high-density pixels to points
    for row in range(population_data.shape[0]):
        for col in range(population_data.shape[1]):
            if population_data[row, col] > threshold:
                x, y = transform * (col, row)
                high_density_points.append(Point(x, y))
                
    return gpd.GeoDataFrame(geometry=high_density_points, crs="EPSG:4326")

def find_optimal_stops(
    high_density_gdf: gpd.GeoDataFrame,
    bus_stops: gpd.GeoDataFrame,
    eps: float = 500,
    min_samples: int = 5
) -> gpd.GeoDataFrame:
    """
        Finds optimal bus stops based on high-density clusters.
        
        Args:
            high_density_gdf: GeoDataFrame of high-density points
            bus_stops: GeoDataFrame of existing bus stops
            eps: DBSCAN epsilon parameter (meters)
            min_samples: DBSCAN minimum samples parameter
        Returns:
            GeoDataFrame of optimal bus stop locations
    """
    if eps <= 0:
        raise ValueError("eps must be positive")
    if min_samples < 1:
        raise ValueError("min_samples must be at least 1")
        
    high_density_points = np.array([[p.x, p.y] for p in high_density_gdf.geometry])
     
    # Cluster high-density points
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(high_density_points)
     
    # Extract cluster centers 
    cluster_centers = high_density_gdf.iloc[np.unique(clustering.labels_)]
     
    # Remove bus stops that are close to cluster centers
    optimal_stops = cluster_centers[~cluster_centers.geometry.intersects(bus_stops.unary_union)]
    return optimal_stops
    