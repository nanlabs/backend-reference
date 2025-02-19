import numpy as np
import geopandas as gpd
from sklearn.cluster import DBSCAN 
from shapely.geometry import Point

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
                
    return gpd.GeoDataFrame(geometry=high_density_points, crs="EPSG:3857")

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
    
    # Convert high-density points to numpy array
    high_density_points = np.array([[p.x, p.y] for p in high_density_gdf.geometry])
    
    # Perform clustering
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(high_density_points)
    high_density_gdf["cluster"] = clustering.labels_
    
    # Filter out noise (-1 cluster)
    clustered_gdf = high_density_gdf[high_density_gdf["cluster"] != -1]
    
    # Compute centroids for each cluster
    cluster_centroids = clustered_gdf.dissolve(by="cluster").centroid
    
    # Convert centroids to GeoDataFrame
    optimal_stops = gpd.GeoDataFrame(geometry=cluster_centroids, crs=high_density_gdf.crs)
    
    # Remove centroids that are too close to existing bus stops
    optimal_stops = optimal_stops[~optimal_stops.geometry.intersects(bus_stops.unary_union)]
    
    return optimal_stops
    