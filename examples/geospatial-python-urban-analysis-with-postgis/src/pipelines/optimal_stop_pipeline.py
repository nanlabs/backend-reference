from src.etl.extract.bsas_data.fetch_bus_stop import fetch_bus_stops
from src.etl.extract.rasterio.population import load_population_density
from src.ml.clustering import extract_high_density_points, find_optimal_stops
from src.visualization.optimization_map import plot_optimal_stops

def run_optimal_stop_pipeline():
    """
    Full pipeline: Identify optimal bus stop locations.
    Raises:
        Exception: If any step in the pipeline fails
    """
    try:
        print("🔄 Step 1/5: Fetching bus stop locations...")
        bus_stops = fetch_bus_stops()
        print("🔄 Step 2/5: Loading population density data...")
        population_data, transform, crs = load_population_density()
        print("📊 Step 3/5: Identifying high-density areas...")
        high_density_gdf = extract_high_density_points(population_data, transform)
        print("📍 Step 4/5: Finding optimal bus stop locations...")
        optimal_stops = find_optimal_stops(high_density_gdf, bus_stops)
        print("🗺️ Step 5/5: Generating visualization...")
        plot_optimal_stops(bus_stops, optimal_stops, districts=None)
        print("✅ Pipeline completed successfully!")
    except Exception as e:
        print(f"❌ Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_optimal_stop_pipeline()
