from src.etl.extract import fetch_bus_stops, load_population_density
from src.ml.clustering import extract_high_density_points, find_optimal_stops
from src.visualization.optimization_map import plot_optimal_stops

def run_optimal_stop_pipeline():
    """
    Full pipeline: Identify optimal bus stop locations.
    """
    print("🔄 Fetching bus stop locations...")
    bus_stops = fetch_bus_stops()

    print("🔄 Loading population density data...")
    population_data, transform, crs = load_population_density()

    print("📊 Identifying high-density areas...")
    high_density_gdf = extract_high_density_points(population_data, transform)

    print("📍 Finding optimal bus stop locations...")
    optimal_stops = find_optimal_stops(high_density_gdf, bus_stops)

    print("🗺️ Generating visualization...")
    plot_optimal_stops(bus_stops, optimal_stops, districts=None)

if __name__ == "__main__":
    run_optimal_stop_pipeline()
