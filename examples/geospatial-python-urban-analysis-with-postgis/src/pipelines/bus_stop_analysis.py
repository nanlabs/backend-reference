from src.etl.extract.postgis.fetch_bus_stop import fetch_bus_stops
from src.etl.extract.bsas_data.fetch_district import fetch_districts
from src.etl.transform.district import reproject_data, spatial_join, count_stops_per_district, get_extreme_district
from src.visualization.bus_stops_map import plot_bus_stops

def run_bus_stop_analysis(line_number: str = None):
    """Executes the bus stop distribution analysis pipeline for a specific line number."""
    
    try: 
        print("🔄 Fetching data...")
        bus_stops = fetch_bus_stops(line_number)
        districts = fetch_districts()

        print("🔄 Processing data...")
        bus_stops = reproject_data(bus_stops)
        districts = reproject_data(districts)
        bus_stops_in_district = spatial_join(bus_stops, districts)

        # Count the number of stops per district
        stops_by_district = count_stops_per_district(bus_stops_in_district)
        # Get the district with the most and least bus stops
        district_max, district_min = get_extreme_district(stops_by_district)

        print("📊 Generating visualization...")
        plot_bus_stops(bus_stops, districts, stops_by_district, district_max, district_min)
    except Exception as e:
        print(f"❌ Pipeline failed: {str(e)}")
        return
    
if __name__ == "__main__":    
    run_bus_stop_analysis("68")
    run_bus_stop_analysis()
